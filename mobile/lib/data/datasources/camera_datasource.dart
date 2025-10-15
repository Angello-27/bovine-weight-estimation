/// DataSource: CameraDataSource
///
/// DataSource para acceso a la cámara del dispositivo.
/// Implementa captura de fotogramas y evaluación de calidad.
///
/// Data Layer - Clean Architecture
library;

import 'dart:io';
import 'dart:typed_data';

import 'package:camera/camera.dart' as camera;
import 'package:image/image.dart' as img;
import 'package:path_provider/path_provider.dart';
import 'package:uuid/uuid.dart';

import '../../core/errors/exceptions.dart';
import '../../domain/entities/frame.dart';
import '../models/frame_model.dart';

/// DataSource para operaciones de cámara
abstract class CameraDataSource {
  /// Inicializa la cámara
  Future<camera.CameraController> initializeCamera();

  /// Captura un fotograma desde el stream de la cámara
  Future<FrameModel> captureFrame(camera.CameraController controller);

  /// Evalúa la calidad de un fotograma
  Future<FrameQuality> evaluateFrameQuality(String imagePath);

  /// Libera recursos de la cámara
  Future<void> dispose(camera.CameraController controller);
}

/// Implementación del CameraDataSource
class CameraDataSourceImpl implements CameraDataSource {
  final Uuid _uuid = const Uuid();

  @override
  Future<camera.CameraController> initializeCamera() async {
    try {
      // Obtener cámaras disponibles
      final cameras = await camera.availableCameras();
      if (cameras.isEmpty) {
        throw const CameraException(
          message: 'No hay cámaras disponibles en el dispositivo',
        );
      }

      // Usar la cámara trasera (índice 0 generalmente)
      final cameraDescription = cameras.first;

      // Crear y configurar controller
      final controller = camera.CameraController(
        cameraDescription,
        camera.ResolutionPreset.high, // Alta resolución para mejor calidad
        enableAudio: false, // No necesitamos audio
        imageFormatGroup: camera.ImageFormatGroup.jpeg,
      );

      // Inicializar controller
      await controller.initialize();

      return controller;
    } on camera.CameraException catch (e) {
      throw CameraException(
        message: 'Error al inicializar cámara: ${e.description}',
      );
    } catch (e) {
      throw CameraException(
        message: 'Error desconocido al inicializar cámara: $e',
      );
    }
  }

  @override
  Future<FrameModel> captureFrame(camera.CameraController controller) async {
    try {
      if (!controller.value.isInitialized) {
        throw const CameraException(message: 'Cámara no inicializada');
      }

      // Capturar imagen
      final camera.XFile imageFile = await controller.takePicture();

      // Guardar en directorio temporal con nombre único
      final directory = await getTemporaryDirectory();
      final frameId = _uuid.v4();
      final imagePath = '${directory.path}/frame_$frameId.jpg';

      // Copiar imagen al path permanente
      await File(imageFile.path).copy(imagePath);

      // Evaluar calidad del fotograma
      final quality = await evaluateFrameQuality(imagePath);

      // Calcular score global
      final globalScore = Frame.calculateGlobalScore(quality);

      // Crear FrameModel
      return FrameModel(
        id: frameId,
        timestamp: DateTime.now(),
        imagePath: imagePath,
        quality: quality,
        globalScore: globalScore,
      );
    } on CameraException {
      rethrow;
    } catch (e) {
      throw CameraException(message: 'Error al capturar fotograma: $e');
    }
  }

  @override
  Future<FrameQuality> evaluateFrameQuality(String imagePath) async {
    try {
      // Leer imagen
      final imageFile = File(imagePath);
      if (!await imageFile.exists()) {
        throw StorageException(message: 'Imagen no encontrada: $imagePath');
      }

      final Uint8List imageBytes = await imageFile.readAsBytes();
      final img.Image? image = img.decodeImage(imageBytes);

      if (image == null) {
        throw const FormatException(
          message: 'No se pudo decodificar la imagen',
        );
      }

      // Calcular métricas de calidad
      final sharpness = _calculateSharpness(image);
      final brightness = _calculateBrightness(image);
      final contrast = _calculateContrast(image);
      final silhouetteVisibility = _calculateSilhouetteVisibility(image);
      final angleScore = _calculateAngleScore(image);

      return FrameQuality(
        sharpness: sharpness,
        brightness: brightness,
        contrast: contrast,
        silhouetteVisibility: silhouetteVisibility,
        angleScore: angleScore,
      );
    } catch (e) {
      throw CameraException(message: 'Error al evaluar calidad: $e');
    }
  }

  /// Calcula nitidez usando Laplacian variance
  double _calculateSharpness(img.Image image) {
    // Simplificación: Usar varianza de gradientes
    // En producción, usar algoritmo Laplacian más robusto
    final grayscale = img.grayscale(image);

    double sumVariance = 0.0;
    int count = 0;

    for (int y = 1; y < grayscale.height - 1; y++) {
      for (int x = 1; x < grayscale.width - 1; x++) {
        final center = grayscale.getPixel(x, y).r;
        final left = grayscale.getPixel(x - 1, y).r;
        final right = grayscale.getPixel(x + 1, y).r;
        final top = grayscale.getPixel(x, y - 1).r;
        final bottom = grayscale.getPixel(x, y + 1).r;

        final laplacian = ((4 * center) - left - right - top - bottom).abs();
        sumVariance += laplacian;
        count++;
      }
    }

    final avgVariance = count > 0 ? sumVariance / count : 0.0;

    // Normalizar a 0.0-1.0 (valores típicos: 0-100, usamos 50 como referencia)
    return (avgVariance / 50).clamp(0.0, 1.0);
  }

  /// Calcula iluminación promedio
  double _calculateBrightness(img.Image image) {
    final grayscale = img.grayscale(image);

    double sumBrightness = 0.0;
    int count = 0;

    for (int y = 0; y < grayscale.height; y++) {
      for (int x = 0; x < grayscale.width; x++) {
        sumBrightness += grayscale.getPixel(x, y).r;
        count++;
      }
    }

    final avgBrightness = count > 0 ? sumBrightness / count : 0.0;

    // Normalizar a 0.0-1.0 (rango: 0-255)
    return avgBrightness / 255.0;
  }

  /// Calcula contraste usando desviación estándar
  double _calculateContrast(img.Image image) {
    final grayscale = img.grayscale(image);
    final brightness = _calculateBrightness(image) * 255;

    double sumSquaredDiff = 0.0;
    int count = 0;

    for (int y = 0; y < grayscale.height; y++) {
      for (int x = 0; x < grayscale.width; x++) {
        final pixelValue = grayscale.getPixel(x, y).r;
        final diff = pixelValue - brightness;
        sumSquaredDiff += diff * diff;
        count++;
      }
    }

    final variance = count > 0 ? sumSquaredDiff / count : 0.0;
    final stdDev = variance > 0 ? (variance).abs() : 0.0;

    // Normalizar a 0.0-1.0 (desviación típica: 0-80)
    return (stdDev / 80).clamp(0.0, 1.0);
  }

  /// Calcula visibilidad de silueta usando detección de bordes
  double _calculateSilhouetteVisibility(img.Image image) {
    // Simplificación: Usar detección básica de bordes
    // En producción, usar algoritmos más avanzados (Canny, Sobel)
    final edges = img.sobel(image);

    double edgeStrength = 0.0;
    int count = 0;

    for (int y = 0; y < edges.height; y++) {
      for (int x = 0; x < edges.width; x++) {
        edgeStrength += edges.getPixel(x, y).r;
        count++;
      }
    }

    final avgEdgeStrength = count > 0 ? edgeStrength / count : 0.0;

    // Normalizar a 0.0-1.0
    return (avgEdgeStrength / 128).clamp(0.0, 1.0);
  }

  /// Calcula score de ángulo (simplificado)
  /// TODO: Implementar detección de ángulo real usando pose estimation
  double _calculateAngleScore(img.Image image) {
    // Simplificación: Usar ratio aspect de la imagen
    // En producción, usar ML pose estimation para detectar ángulo del animal
    final aspectRatio = image.width / image.height;

    // Score alto si aspect ratio es ~1.5-2.0 (animal de lado)
    if (aspectRatio >= 1.5 && aspectRatio <= 2.0) {
      return 0.8;
    } else if (aspectRatio >= 1.2 && aspectRatio <= 2.5) {
      return 0.6;
    } else {
      return 0.4;
    }
  }

  @override
  Future<void> dispose(camera.CameraController controller) async {
    await controller.dispose();
  }
}

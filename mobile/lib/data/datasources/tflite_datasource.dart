/// DataSource: TFLiteDataSource
///
/// DataSource para inferencia con modelos TensorFlow Lite.
/// Single Responsibility: Ejecutar inferencia ML con modelos por raza.
///
/// Data Layer - Clean Architecture
library;

import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:image/image.dart' as img;
import 'package:uuid/uuid.dart';

import '../../core/constants/breeds.dart';
import '../../core/errors/exceptions.dart';
import '../../domain/entities/weight_estimation.dart';
import '../models/weight_estimation_model.dart';

/// DataSource para operaciones de TFLite
abstract class TFLiteDataSource {
  /// Carga los modelos TFLite de las razas especificadas
  Future<void> loadModels(List<BreedType> breeds);

  /// Verifica si los modelos están cargados
  Future<bool> areModelsLoaded();

  /// Ejecuta inferencia de peso
  Future<WeightEstimationModel> runInference({
    required String imagePath,
    required BreedType breed,
    String? cattleId,
  });

  /// Libera recursos de los modelos
  Future<void> dispose();
}

/// Implementación del TFLiteDataSource
class TFLiteDataSourceImpl implements TFLiteDataSource {
  final Uuid _uuid = const Uuid();

  /// Modelos cargados por raza
  /// TODO: Implementar carga real de modelos TFLite
  /// Por ahora, usamos Map para tracking
  final Map<BreedType, bool> _loadedModels = {};

  /// Tamaño de entrada del modelo (224x224x3 según ML Training Standards)
  static const int inputSize = 224;

  @override
  Future<void> loadModels(List<BreedType> breeds) async {
    try {
      for (final breed in breeds) {
        // TODO: Cargar modelo TFLite real
        // final modelPath = await _getModelPath(breed);
        // final interpreter = await Interpreter.fromAsset(modelPath);

        // Por ahora, marcar como cargado (mock)
        _loadedModels[breed] = true;

        debugPrint('✅ Modelo cargado: ${breed.modelFilename}');
      }
    } catch (e) {
      throw ModelException(message: 'Error al cargar modelos TFLite: $e');
    }
  }

  @override
  Future<bool> areModelsLoaded() async {
    // Verificar si al menos un modelo está cargado
    return _loadedModels.isNotEmpty;
  }

  @override
  Future<WeightEstimationModel> runInference({
    required String imagePath,
    required BreedType breed,
    String? cattleId,
  }) async {
    final startTime = DateTime.now();

    try {
      // Verificar que el modelo de la raza esté cargado
      if (_loadedModels[breed] != true) {
        throw ModelException(
          message: 'Modelo de raza ${breed.displayName} no está cargado',
        );
      }

      // 1. Cargar y preprocesar imagen
      final inputTensor = await _preprocessImage(imagePath);

      // 2. Ejecutar inferencia
      // TODO: Implementar inferencia real con TFLite
      // final output = await _interpreter.run(inputTensor);
      // final estimatedWeight = _postprocessOutput(output);

      // Por ahora, simular inferencia (mock)
      final estimatedWeight = await _mockInference(breed, inputTensor);

      // 3. Calcular confidence score (simulado)
      final confidenceScore = _calculateConfidenceScore(breed, estimatedWeight);

      // 4. Calcular tiempo de procesamiento
      final processingTime = DateTime.now().difference(startTime);

      // 5. Crear estimación
      return WeightEstimationModel(
        id: _uuid.v4(),
        cattleId: cattleId,
        breed: breed,
        estimatedWeight: estimatedWeight,
        confidenceScore: confidenceScore,
        frameImagePath: imagePath,
        timestamp: DateTime.now(),
        gpsCoordinates: null, // TODO: Obtener coordenadas GPS reales
        method: EstimationMethod.tflite,
        modelVersion: '1.0.0',
        processingTimeMs: processingTime.inMilliseconds,
      );
    } on ModelException {
      rethrow;
    } catch (e) {
      throw ModelException(message: 'Error en inferencia: $e');
    }
  }

  /// Preprocesa imagen para input del modelo
  /// Input: 224x224x3 (RGB)
  Future<Float32List> _preprocessImage(String imagePath) async {
    try {
      // Leer imagen
      final imageFile = File(imagePath);
      if (!await imageFile.exists()) {
        throw StorageException(message: 'Imagen no encontrada: $imagePath');
      }

      final Uint8List imageBytes = await imageFile.readAsBytes();
      final img.Image? image = img.decodeImage(imageBytes);

      if (image == null) {
        throw const FormatException(message: 'No se pudo decodificar imagen');
      }

      // Resize a 224x224
      final resized = img.copyResize(
        image,
        width: inputSize,
        height: inputSize,
      );

      // Convertir a Float32List normalizado (0.0-1.0)
      final inputTensor = Float32List(inputSize * inputSize * 3);
      int pixelIndex = 0;

      for (int y = 0; y < inputSize; y++) {
        for (int x = 0; x < inputSize; x++) {
          final pixel = resized.getPixel(x, y);

          // Normalizar RGB a 0.0-1.0
          inputTensor[pixelIndex++] = pixel.r / 255.0;
          inputTensor[pixelIndex++] = pixel.g / 255.0;
          inputTensor[pixelIndex++] = pixel.b / 255.0;
        }
      }

      return inputTensor;
    } catch (e) {
      throw ModelException(message: 'Error en preprocesamiento: $e');
    }
  }

  /// Simula inferencia (MOCK temporal)
  /// TODO: Reemplazar con inferencia real de TFLite
  Future<double> _mockInference(
    BreedType breed,
    Float32List inputTensor,
  ) async {
    // Simular delay de procesamiento (<3s)
    await Future.delayed(const Duration(milliseconds: 500));

    // Pesos simulados por raza (alineados con entrenamiento ML)
    final Map<BreedType, double> mockWeights = {
      BreedType.nelore: 420.0, // Carne tropical dominante
      BreedType.brahman: 450.0, // Cebuino versátil
      BreedType.guzerat: 400.0, // Doble propósito
      BreedType.senepol: 380.0, // Carne premium
      BreedType.girolando: 380.0, // Lechera tropical
      BreedType.gyrLechero: 350.0, // Lechera pura
      BreedType.sindi: 280.0, // Lechera compacta
    };

    // Agregar variación aleatoria ±20kg
    final baseWeight = mockWeights[breed] ?? 400.0;
    final variation = (DateTime.now().millisecond % 40) - 20; // -20 a +20

    return baseWeight + variation;
  }

  /// Calcula confidence score (simulado)
  /// TODO: Obtener del output real del modelo TFLite
  double _calculateConfidenceScore(BreedType breed, double estimatedWeight) {
    // Confidence simulado: 85-98%
    final baseConfidence = 0.85;
    final variation = (DateTime.now().millisecond % 13) / 100; // 0.00-0.13

    return (baseConfidence + variation).clamp(0.80, 0.98);
  }

  @override
  Future<void> dispose() async {
    // TODO: Liberar intérpretes de TFLite
    _loadedModels.clear();
  }
}

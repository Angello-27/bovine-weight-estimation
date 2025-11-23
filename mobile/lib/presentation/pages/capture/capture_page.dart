/// Capture Page - Template
///
/// US-001: Captura Continua de Fotogramas
///
/// Pantalla refactorizada con Atomic Design + SOLID.
/// Single Responsibility: Orquestar componentes de captura.
///
/// Presentation Layer - Pages
library;

import 'package:flutter/material.dart';
import 'package:permission_handler/permission_handler.dart'
    as permission_handler;
import 'package:provider/provider.dart';
import 'package:camera/camera.dart' as camera;

import '../../../core/config/dependency_injection.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../providers/capture_provider.dart';
import '../../widgets/molecules/dialogs/permission_rationale_dialog.dart';
import '../../widgets/organisms/capture/camera_preview_section.dart';
import 'widgets/capture_action_button.dart';
import 'widgets/capture_content.dart';
import 'widgets/capture_status_card.dart';

/// Pantalla de captura de fotogramas
///
/// Usa composición de componentes siguiendo Atomic Design:
/// - Organisms: CaptureStatusCard, CaptureContent, CameraPreviewSection
/// - Molecules: CaptureActionButton
/// - Atoms: (usados internamente por los organisms)
class CapturePage extends StatefulWidget {
  const CapturePage({super.key});

  @override
  State<CapturePage> createState() => _CapturePageState();
}

class _CapturePageState extends State<CapturePage> {
  camera.CameraController? _cameraController;
  bool _isInitializing = false;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    // Solicitar permisos e inicializar cámara al entrar
    _requestPermissionAndInitializeCamera();
  }

  @override
  void dispose() {
    _disposeCamera();
    super.dispose();
  }

  /// Solicita permisos e inicializa la cámara
  Future<void> _requestPermissionAndInitializeCamera() async {
    final di = DependencyInjection();

    // 1. Verificar si ya tiene permiso
    final hasPermission = await di.permissionService.isPermissionGranted(
      permission_handler.Permission.camera,
    );

    if (hasPermission) {
      // Ya tiene permiso, inicializar cámara
      await _initializeCamera();
      return;
    }

    // 2. Solicitar permiso sin diálogo (solo si no está montado aún)
    if (!mounted) return;

    final status = await di.permissionService.requestPermission(
      permission_handler.Permission.camera,
    );

    if (status.isGranted) {
      // Permiso otorgado, inicializar cámara
      await _initializeCamera();
    } else if (status.isPermanentlyDenied) {
      // Permiso denegado permanentemente - mostrar mensaje
      if (!mounted) return;
      setState(() {
        _errorMessage =
            'Permiso de cámara denegado. Por favor, habilítalo en configuración.';
      });
    } else {
      // Permiso denegado temporalmente
      if (!mounted) return;
      setState(() {
        _errorMessage =
            'Se necesita permiso de cámara para mostrar el preview.';
      });
    }
  }

  /// Inicializa la cámara
  Future<void> _initializeCamera() async {
    if (_isInitializing) return;

    setState(() {
      _isInitializing = true;
      _errorMessage = null;
    });

    try {
      final di = DependencyInjection();
      final controller = await di.cameraDataSource.initializeCamera();

      if (!mounted) {
        await di.cameraDataSource.dispose(controller);
        return;
      }

      setState(() {
        _cameraController = controller;
        _isInitializing = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _errorMessage = 'Error al inicializar cámara: $e';
        _isInitializing = false;
      });
    }
  }

  /// Libera recursos de la cámara
  Future<void> _disposeCamera() async {
    if (_cameraController != null) {
      final di = DependencyInjection();
      await di.cameraDataSource.dispose(_cameraController!);
      _cameraController = null;
    }
  }

  /// Solicita permiso manualmente (desde botón)
  Future<void> _requestPermissionManually() async {
    final di = DependencyInjection();

    if (!mounted) return;

    // Mostrar diálogo explicativo
    final shouldRequest = await PermissionRationaleDialog.showCameraPermission(
      context,
    );

    if (shouldRequest != true) {
      return;
    }

    final status = await di.permissionService.requestPermission(
      permission_handler.Permission.camera,
    );

    if (status.isGranted) {
      await _initializeCamera();
    } else if (status.isPermanentlyDenied) {
      if (!mounted) return;

      final openSettings =
          await PermissionRationaleDialog.showPermissionDeniedDialog(
            context,
            'Cámara',
          );

      if (openSettings == true) {
        await di.permissionService.openAppSettings();
      }
    } else {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text(
            'Se necesita permiso de cámara para capturar fotogramas',
          ),
          backgroundColor: AppColors.warning,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Captura de Fotogramas')),
      body: Consumer<CaptureProvider>(
        builder: (context, provider, child) {
          return SafeArea(
            child: Padding(
              padding: const EdgeInsets.all(AppSpacing.screenPadding),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  // Estado actual
                  CaptureStatusCard(provider: provider),

                  const SizedBox(height: AppSpacing.lg),

                  // Preview de cámara con manejo de estados (Organism)
                  CameraPreviewSection(
                    cameraController: _cameraController,
                    isInitializing: _isInitializing,
                    errorMessage: _errorMessage,
                    onRequestPermission: _requestPermissionManually,
                  ),

                  const SizedBox(height: AppSpacing.lg),

                  // Contenido principal (scrollable)
                  Expanded(child: CaptureContent(provider: provider)),

                  const SizedBox(height: AppSpacing.md),

                  // Botón de acción
                  CaptureActionButton(provider: provider),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}

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
import '../../../l10n/app_localizations.dart';
import '../../providers/capture_provider.dart';
import '../../providers/settings_provider.dart';
import '../../widgets/molecules/app_bar_gradient.dart';
import '../../widgets/molecules/dialogs/permission_rationale_dialog.dart';
import 'widgets/fullscreen_camera_preview.dart';
import 'widgets/capture_overlay.dart';
import 'widgets/capture_floating_controls.dart';
import 'widgets/best_frame_thumbnail.dart';
import 'widgets/camera_framing_guides.dart';

/// Pantalla de captura de fotogramas a pantalla completa
///
/// Vista principal: Cámara a pantalla completa con overlay y controles flotantes
/// Vista fallback: Mensaje simple cuando la cámara no está lista
///
/// Componentes principales:
/// - FullScreenCameraPreview: Cámara a pantalla completa
/// - CameraFramingGuides: Guías de encuadre
/// - CaptureOverlay: Overlay con estadísticas
/// - BestFrameThumbnail: Miniatura del mejor frame
/// - CaptureFloatingControls: Controles flotantes
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
        _errorMessage = AppLocalizations.of(context)!.cameraPermissionDenied;
      });
    } else {
      // Permiso denegado temporalmente
      if (!mounted) return;
      setState(() {
        _errorMessage = AppLocalizations.of(context)!.cameraPermissionRequired;
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
      // Obtener configuración de flash desde settings
      final settingsProvider = Provider.of<SettingsProvider>(
        context,
        listen: false,
      );
      final enableFlash = settingsProvider.settings.flashEnabled;
      final controller = await di.cameraDataSource.initializeCamera(
        enableFlash: enableFlash,
      );

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
    // Si la cámara está inicializada, mostrar vista a pantalla completa
    if (_cameraController != null && _cameraController!.value.isInitialized) {
      return Consumer<CaptureProvider>(
        builder: (context, provider, child) {
          return Scaffold(
            backgroundColor: Colors.black,
            // Sin AppBar para pantalla completa
            body: Stack(
              children: [
                // Cámara a pantalla completa
                FullScreenCameraPreview(controller: _cameraController!),

                // Guías de encuadre
                const CameraFramingGuides(),

                // Overlay con información
                CaptureOverlay(),

                // Miniatura del mejor frame
                const BestFrameThumbnail(),

                // Controles flotantes
                Align(
                  alignment: Alignment.bottomCenter,
                  child: CaptureFloatingControls(),
                ),
              ],
            ),
          );
        },
      );
    }

    // Vista de fallback mientras se inicializa o hay error
    return Scaffold(
      appBar: AppBarGradient(
        title: AppLocalizations.of(context)!.captureFrames,
      ),
      body: SafeArea(
        child: Center(
          child: Padding(
            padding: const EdgeInsets.all(AppSpacing.screenPadding),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Indicador de estado
                if (_isInitializing)
                  const Column(
                    children: [
                      CircularProgressIndicator(),
                      SizedBox(height: AppSpacing.lg),
                      Text(
                        'Inicializando cámara...',
                        style: TextStyle(fontSize: 16),
                      ),
                    ],
                  )
                else if (_errorMessage != null)
                  Column(
                    children: [
                      const Icon(
                        Icons.error_outline,
                        size: 64,
                        color: AppColors.error,
                      ),
                      const SizedBox(height: AppSpacing.md),
                      Text(
                        _errorMessage!,
                        textAlign: TextAlign.center,
                        style: const TextStyle(
                          fontSize: 16,
                          color: AppColors.error,
                        ),
                      ),
                      const SizedBox(height: AppSpacing.lg),
                      ElevatedButton.icon(
                        onPressed: _requestPermissionManually,
                        icon: const Icon(Icons.settings),
                        label: Text(
                          AppLocalizations.of(context)!.configurePermissions,
                        ),
                      ),
                    ],
                  )
                else
                  const Column(
                    children: [
                      Icon(
                        Icons.camera_alt,
                        size: 64,
                        color: AppColors.primary,
                      ),
                      SizedBox(height: AppSpacing.md),
                      Text(
                        'Preparando cámara...',
                        style: TextStyle(fontSize: 16),
                      ),
                    ],
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

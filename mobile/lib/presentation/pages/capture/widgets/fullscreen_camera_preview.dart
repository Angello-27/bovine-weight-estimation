/// Full Screen Camera Preview - Atom
///
/// Preview de cámara a pantalla completa (como app nativa).
/// Single Responsibility: Mostrar cámara ocupando toda la pantalla.
///
/// Presentation Layer - Atoms
library;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:camera/camera.dart' as camera;

import '../../../../domain/entities/weight_estimation.dart';
import '../../../providers/capture_provider.dart';

/// Preview de cámara a pantalla completa
class FullScreenCameraPreview extends StatelessWidget {
  /// Controller de la cámara
  final camera.CameraController controller;

  const FullScreenCameraPreview({required this.controller, super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<CaptureProvider>(
      builder: (context, provider, child) {
        return Stack(
          children: [
            // Preview de la cámara
            _buildCameraPreview(),

            // Overlay con resultados de estimación (si hay)
            if (provider.lastEstimation != null)
              _buildEstimationOverlay(context, provider.lastEstimation!),

            // Indicador de estimación en progreso
            if (provider.isEstimating) _buildEstimatingIndicator(context),
          ],
        );
      },
    );
  }

  Widget _buildCameraPreview() {
    if (!controller.value.isInitialized) {
      return Container(
        color: Colors.black,
        child: const Center(
          child: CircularProgressIndicator(color: Colors.white),
        ),
      );
    }

    return Builder(
      builder: (context) {
        // Obtener tamaño de pantalla
        final screenSize = MediaQuery.of(context).size;
        final aspectRatio = controller.value.aspectRatio;

        return SizedBox(
          width: screenSize.width,
          height: screenSize.height,
          child: FittedBox(
            fit: BoxFit.cover,
            child: SizedBox(
              width: screenSize.width,
              height: screenSize.width / aspectRatio,
              child: camera.CameraPreview(controller),
            ),
          ),
        );
      },
    );
  }

  Widget _buildEstimationOverlay(
    BuildContext context,
    WeightEstimation estimation,
  ) {
    return Positioned(
      top: 120, // Debajo del overlay superior
      left: 16,
      right: 16,
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: Colors.black.withValues(alpha: 0.8),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: _getConfidenceColor(estimation.confidenceLevel),
            width: 2,
          ),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisSize: MainAxisSize.min,
          children: [
            Row(
              children: [
                Icon(
                  Icons.scale,
                  color: _getConfidenceColor(estimation.confidenceLevel),
                  size: 24,
                ),
                const SizedBox(width: 8),
                Text(
                  'Peso Estimado',
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 8),
            Text(
              '${estimation.estimatedWeight.toStringAsFixed(1)} kg',
              style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                color: _getConfidenceColor(estimation.confidenceLevel),
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 4),
            Row(
              children: [
                Text(
                  'Confianza: ${(estimation.confidenceScore * 100).toStringAsFixed(0)}%',
                  style: Theme.of(
                    context,
                  ).textTheme.bodySmall?.copyWith(color: Colors.white70),
                ),
                const SizedBox(width: 16),
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 8,
                    vertical: 4,
                  ),
                  decoration: BoxDecoration(
                    color: _getConfidenceColor(
                      estimation.confidenceLevel,
                    ).withValues(alpha: 0.3),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Text(
                    estimation.confidenceLevel.displayName.toUpperCase(),
                    style: Theme.of(context).textTheme.bodySmall?.copyWith(
                      color: _getConfidenceColor(estimation.confidenceLevel),
                      fontWeight: FontWeight.bold,
                      fontSize: 10,
                    ),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildEstimatingIndicator(BuildContext context) {
    return Positioned(
      top: 120,
      left: 16,
      right: 16,
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: Colors.black.withValues(alpha: 0.8),
          borderRadius: BorderRadius.circular(12),
        ),
        child: Row(
          children: [
            const SizedBox(
              width: 24,
              height: 24,
              child: CircularProgressIndicator(
                strokeWidth: 2,
                color: Colors.white,
              ),
            ),
            const SizedBox(width: 16),
            Text(
              'Estimando peso...',
              style: Theme.of(
                context,
              ).textTheme.bodyMedium?.copyWith(color: Colors.white),
            ),
          ],
        ),
      ),
    );
  }

  Color _getConfidenceColor(ConfidenceLevel level) {
    switch (level) {
      case ConfidenceLevel.high:
        return Colors.green;
      case ConfidenceLevel.medium:
        return Colors.orange;
      case ConfidenceLevel.low:
        return Colors.red;
    }
  }
}

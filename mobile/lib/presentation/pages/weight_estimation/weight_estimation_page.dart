/// Page: WeightEstimationPage
///
/// US-002: Estimación de Peso por Raza con IA
///
/// Pantalla para seleccionar raza y estimar peso usando TFLite.
/// Single Responsibility: Coordinar estimación de peso.
///
/// Presentation Layer - Pages
library;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../providers/weight_estimation_provider.dart';
import '../../widgets/organisms/breed/breed_selector_grid.dart';
import 'widgets/estimation_action_button.dart';
import 'widgets/frame_preview_card.dart';
import 'widgets/weight_estimation_result_card.dart';

/// Pantalla de estimación de peso
class WeightEstimationPage extends StatelessWidget {
  /// Path de la imagen del fotograma seleccionado
  final String framePath;

  /// ID del animal (opcional)
  final String? cattleId;

  const WeightEstimationPage({
    super.key,
    required this.framePath,
    this.cattleId,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Estimación de Peso')),
      body: Consumer<WeightEstimationProvider>(
        builder: (context, provider, child) {
          // Establecer imagen al iniciar
          if (provider.imagePath != framePath) {
            WidgetsBinding.instance.addPostFrameCallback((_) {
              provider.setImagePath(framePath);
            });
          }

          return SafeArea(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(AppSpacing.screenPadding),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  // Preview de la imagen
                  FramePreviewCard(imagePath: framePath),

                  const SizedBox(height: AppSpacing.lg),

                  // Selector de raza (si no ha estimado)
                  if (!provider.hasResult && !provider.isEstimating)
                    BreedSelectorGrid(
                      selectedBreed: provider.selectedBreed,
                      onBreedSelected: provider.selectBreed,
                    ),

                  // Indicador de progreso (si está estimando)
                  if (provider.isEstimating)
                    Center(
                      child: Container(
                        padding: const EdgeInsets.all(AppSpacing.xl),
                        decoration: BoxDecoration(
                          color: AppColors.primary.withValues(alpha: 0.05),
                          borderRadius: BorderRadius.circular(
                            AppSpacing.borderRadiusLarge,
                          ),
                        ),
                        child: const Column(
                          children: [
                            SizedBox(
                              width: 60,
                              height: 60,
                              child: CircularProgressIndicator(
                                strokeWidth: 6,
                                color: AppColors.primary,
                              ),
                            ),
                            SizedBox(height: AppSpacing.lg),
                            Text(
                              'Estimando peso con IA...',
                              style: TextStyle(
                                fontSize: AppSpacing.fontSizeNormal,
                                fontWeight: FontWeight.w500,
                                color: AppColors.grey800,
                              ),
                            ),
                            SizedBox(height: AppSpacing.sm),
                            Text(
                              'Analizando características del animal',
                              style: TextStyle(
                                fontSize: AppSpacing.fontSizeSmall,
                                color: AppColors.grey600,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),

                  // Resultado (si completó)
                  if (provider.hasResult && provider.estimation != null)
                    WeightEstimationResultCard(
                      estimation: provider.estimation!,
                    ),

                  // Error (si hay error)
                  if (provider.hasError)
                    Card(
                      color: AppColors.errorLight,
                      child: Padding(
                        padding: const EdgeInsets.all(AppSpacing.cardPadding),
                        child: Text(
                          provider.errorMessage ?? 'Error desconocido',
                          style: const TextStyle(color: AppColors.error),
                        ),
                      ),
                    ),

                  const SizedBox(height: AppSpacing.lg),

                  // Botón de acción
                  EstimationActionButton(
                    provider: provider,
                    framePath: framePath,
                    cattleId: cattleId,
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}

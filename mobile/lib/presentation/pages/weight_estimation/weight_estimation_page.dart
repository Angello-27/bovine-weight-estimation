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
import '../../widgets/atoms/buttons/primary_button.dart';
import '../../widgets/organisms/breed/breed_selector_grid.dart';
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
                  _buildImagePreview(framePath),

                  const SizedBox(height: AppSpacing.lg),

                  // Selector de raza (si no ha estimado)
                  if (!provider.hasResult && !provider.isEstimating)
                    BreedSelectorGrid(
                      selectedBreed: provider.selectedBreed,
                      onBreedSelected: provider.selectBreed,
                    ),

                  // Indicador de progreso (si está estimando)
                  if (provider.isEstimating)
                    const Center(
                      child: Column(
                        children: [
                          CircularProgressIndicator(),
                          SizedBox(height: AppSpacing.md),
                          Text('Estimando peso con IA...'),
                        ],
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
                  _buildActionButton(context, provider),
                ],
              ),
            ),
          );
        },
      ),
    );
  }

  /// Preview de la imagen
  Widget _buildImagePreview(String imagePath) {
    return Card(
      elevation: AppSpacing.elevationMedium,
      clipBehavior: Clip.antiAlias,
      child: AspectRatio(
        aspectRatio: 16 / 9,
        child: Image.asset(
          imagePath,
          fit: BoxFit.cover,
          errorBuilder: (context, error, stackTrace) {
            return Container(
              color: AppColors.grey300,
              child: const Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    Icons.image,
                    size: AppSpacing.iconSizeXXLarge,
                    color: AppColors.grey500,
                  ),
                  SizedBox(height: AppSpacing.sm),
                  Text('Fotograma seleccionado'),
                ],
              ),
            );
          },
        ),
      ),
    );
  }

  /// Botón de acción
  Widget _buildActionButton(
    BuildContext context,
    WeightEstimationProvider provider,
  ) {
    if (provider.isEstimating) {
      return const SizedBox.shrink();
    }

    if (provider.hasResult) {
      return PrimaryButton(
        text: 'Estimar Otra Vez',
        icon: Icons.refresh,
        onPressed: () {
          provider.reset();
        },
      );
    }

    return PrimaryButton(
      text: 'Estimar Peso',
      icon: Icons.calculate,
      onPressed: provider.selectedBreed != null
          ? () async {
              await provider.estimateWeight(
                imagePath: framePath,
                breed: provider.selectedBreed,
                cattleId: cattleId,
              );
            }
          : null, // Deshabilitado si no hay raza seleccionada
    );
  }
}

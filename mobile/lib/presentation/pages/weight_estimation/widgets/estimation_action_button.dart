/// Widget: EstimationActionButton
///
/// Botón de acción para estimar o reiniciar.
/// Single Responsibility: Mostrar botón correcto según estado.
///
/// Page-specific Widget (Weight Estimation)
library;

import 'package:flutter/material.dart';

import '../../../../core/constants/breeds.dart';
import '../../../../l10n/app_localizations.dart';
import '../../../providers/weight_estimation_provider.dart';
import '../../../widgets/atoms/buttons/primary_button.dart';

/// Botón de acción para estimación
class EstimationActionButton extends StatelessWidget {
  /// Provider de weight estimation
  final WeightEstimationProvider provider;

  /// Path del frame
  final String framePath;

  /// ID del cattle (opcional)
  final String? cattleId;

  const EstimationActionButton({
    required this.provider,
    required this.framePath,
    this.cattleId,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    // No mostrar nada si está estimando
    if (provider.isEstimating) {
      return const SizedBox.shrink();
    }

    final l10n = AppLocalizations.of(context)!;

    // Si ya tiene resultado, mostrar botón de reinicio
    if (provider.hasResult) {
      return PrimaryButton(
        text: l10n.estimateAgain,
        icon: Icons.refresh,
        onPressed: provider.reset,
      );
    }

    // Botón de estimar (deshabilitado si no hay raza seleccionada)
    return PrimaryButton(
      text: l10n.estimateWeight,
      icon: Icons.calculate,
      onPressed: provider.selectedBreed != null
          ? () => _onEstimatePressed(provider.selectedBreed!)
          : null,
    );
  }

  /// Handler para estimar peso
  Future<void> _onEstimatePressed(BreedType breed) async {
    await provider.estimateWeight(
      imagePath: framePath,
      breed: breed,
      cattleId: cattleId,
    );
  }
}

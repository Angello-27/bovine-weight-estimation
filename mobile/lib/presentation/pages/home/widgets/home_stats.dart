/// Home Stats - Organism
///
/// Panel de estadísticas rápidas del dashboard.
/// Atomic Design: Organism
///
/// Presentation Layer - Organisms
library;

import 'package:flutter/material.dart';

import '../../../../core/theme/app_spacing.dart';
import '../../../../l10n/app_localizations.dart';
import 'home_stat_card.dart';

/// Panel de estadísticas rápidas
class HomeStats extends StatelessWidget {
  const HomeStats({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    return Row(
      children: [
        Expanded(
          child: HomeStatCard(
            icon: Icons.pets,
            value: '500',
            label: l10n.animals,
          ),
        ),
        const SizedBox(width: AppSpacing.sm),
        Expanded(
          child: HomeStatCard(
            icon: Icons.monitor_weight,
            value: '450 kg',
            label: l10n.averageWeight,
          ),
        ),
        const SizedBox(width: AppSpacing.sm),
        Expanded(
          child: HomeStatCard(
            icon: Icons.category,
            value: '7',
            label: l10n.breeds,
          ),
        ),
      ],
    );
  }
}

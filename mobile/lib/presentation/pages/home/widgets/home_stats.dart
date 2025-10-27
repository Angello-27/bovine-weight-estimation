/// Home Stats - Organism
///
/// Panel de estadísticas rápidas del dashboard.
/// Atomic Design: Organism
///
/// Presentation Layer - Organisms
library;

import 'package:flutter/material.dart';

import '../../../../core/theme/app_spacing.dart';
import 'home_stat_card.dart';

/// Panel de estadísticas rápidas
class HomeStats extends StatelessWidget {
  const HomeStats({super.key});

  @override
  Widget build(BuildContext context) {
    return const Row(
      children: [
        Expanded(
          child: HomeStatCard(
            icon: Icons.pets,
            value: '500',
            label: 'Animales',
          ),
        ),
        SizedBox(width: AppSpacing.sm),
        Expanded(
          child: HomeStatCard(
            icon: Icons.monitor_weight,
            value: '450 kg',
            label: 'Peso Prom.',
          ),
        ),
        SizedBox(width: AppSpacing.sm),
        Expanded(
          child: HomeStatCard(
            icon: Icons.category,
            value: '7',
            label: 'Razas',
          ),
        ),
      ],
    );
  }
}


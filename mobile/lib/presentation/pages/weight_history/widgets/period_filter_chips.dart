/// Widget: PeriodFilterChips
///
/// Chips para filtrar historial por período.
/// Single Responsibility: Permitir selección de período de análisis.
///
/// Page-specific Widget (Weight History)
library;

import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../l10n/app_localizations.dart';
import '../../../providers/weight_history_provider.dart';

/// Filtros de período con chips
class PeriodFilterChips extends StatelessWidget {
  /// Período seleccionado
  final HistoryPeriod selectedPeriod;

  /// Callback al cambiar período
  final ValueChanged<HistoryPeriod> onPeriodChanged;

  const PeriodFilterChips({
    required this.selectedPeriod,
    required this.onPeriodChanged,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          AppLocalizations.of(context)!.period,
          style: Theme.of(
            context,
          ).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: AppSpacing.sm),
        Wrap(
          spacing: AppSpacing.sm,
          runSpacing: AppSpacing.sm,
          children: HistoryPeriod.values
              .where(
                (p) => p != HistoryPeriod.custom,
              ) // Excluir personalizado por ahora
              .map((period) => _buildChip(context, period))
              .toList(),
        ),
      ],
    );
  }

  /// Chip individual
  Widget _buildChip(BuildContext context, HistoryPeriod period) {
    final isSelected = period == selectedPeriod;

    return FilterChip(
      label: Text(period.displayName),
      selected: isSelected,
      onSelected: (_) => onPeriodChanged(period),
      backgroundColor: Colors.white,
      selectedColor: AppColors.secondary.withValues(alpha: 0.15),
      checkmarkColor: AppColors.secondary,
      side: BorderSide(
        color: isSelected ? AppColors.secondary : AppColors.grey300,
        width: isSelected ? 2 : 1,
      ),
      labelStyle: Theme.of(context).textTheme.bodyMedium?.copyWith(
        color: isSelected ? AppColors.secondary : AppColors.grey700,
        fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
      ),
    );
  }
}

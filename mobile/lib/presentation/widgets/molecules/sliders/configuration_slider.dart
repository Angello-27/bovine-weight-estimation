/// Molecule: ConfigurationSlider
///
/// Slider de configuración con label y valor actual.
/// Single Responsibility: Permitir ajuste de valor numérico.
///
/// Atomic Design - Molecules Layer
library;

import 'package:flutter/material.dart';

import '../../../../core/theme/app_spacing.dart';

/// Slider de configuración
class ConfigurationSlider extends StatelessWidget {
  final String label;
  final double value;
  final double min;
  final double max;
  final int divisions;
  final String Function(double) valueFormatter;
  final ValueChanged<double> onChanged;

  const ConfigurationSlider({
    super.key,
    required this.label,
    required this.value,
    required this.min,
    required this.max,
    required this.divisions,
    required this.valueFormatter,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.md),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              '$label: ${valueFormatter(value)}',
              style: Theme.of(context).textTheme.titleSmall,
            ),
            const SizedBox(height: AppSpacing.xs),
            Slider(
              value: value,
              min: min,
              max: max,
              divisions: divisions,
              label: valueFormatter(value),
              onChanged: onChanged,
            ),
          ],
        ),
      ),
    );
  }
}

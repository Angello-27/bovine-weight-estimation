/// Molecule: GenderDropdown
///
/// Dropdown para seleccionar género del animal.
/// Single Responsibility: Selector de género con validación.
///
/// Atomic Design - Molecules Layer
library;

import 'package:flutter/material.dart';

import '../../../../../domain/entities/cattle.dart';
import '../../../../core/theme/app_spacing.dart';

/// Dropdown de selección de género
class GenderDropdown extends StatelessWidget {
  final Gender? selectedGender;
  final ValueChanged<Gender> onChanged;
  final bool enabled;

  const GenderDropdown({
    super.key,
    this.selectedGender,
    required this.onChanged,
    this.enabled = true,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surface,
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusMedium),
        border: Border.all(
          color: Theme.of(context).colorScheme.outline.withValues(alpha: 0.2),
          width: 1,
        ),
      ),
      child: DropdownButtonFormField<Gender>(
        key: ValueKey(selectedGender),
        initialValue: selectedGender,
        decoration: InputDecoration(
          labelText: 'Género *',
          hintText: 'Selecciona el género',
          prefixIcon: Icon(
            Icons.wc_rounded,
            color: Theme.of(context).colorScheme.primary,
          ),
          border: InputBorder.none,
          enabledBorder: InputBorder.none,
          focusedBorder: InputBorder.none,
          errorBorder: InputBorder.none,
          focusedErrorBorder: InputBorder.none,
          contentPadding: const EdgeInsets.symmetric(
            horizontal: AppSpacing.md,
            vertical: AppSpacing.sm,
          ),
        ),
        items: Gender.values.map((gender) {
          return DropdownMenuItem<Gender>(
            value: gender,
            child: Text(
              gender.displayName,
              style: Theme.of(context).textTheme.bodyMedium,
            ),
          );
        }).toList(),
        onChanged: enabled
            ? (gender) {
                if (gender != null) {
                  onChanged(gender);
                }
              }
            : null,
        validator: (value) {
          if (value == null) {
            return 'El género es obligatorio';
          }
          return null;
        },
        style: Theme.of(context).textTheme.bodyMedium,
        dropdownColor: Theme.of(context).colorScheme.surface,
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusMedium),
      ),
    );
  }
}

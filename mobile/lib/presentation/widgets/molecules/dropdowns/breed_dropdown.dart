/// Molecule: BreedDropdown
///
/// Dropdown para seleccionar raza bovina (7 razas exactas).
/// Single Responsibility: Selector de raza con validación.
///
/// Atomic Design - Molecules Layer
library;

import 'package:flutter/material.dart';

import '../../../../core/constants/breeds.dart';
import '../../../../core/theme/app_spacing.dart';

/// Dropdown de selección de raza
class BreedDropdown extends StatelessWidget {
  final BreedType? selectedBreed;
  final ValueChanged<BreedType> onChanged;
  final bool enabled;

  const BreedDropdown({
    super.key,
    this.selectedBreed,
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
      child: DropdownButtonFormField<BreedType>(
        key: ValueKey(selectedBreed),
        initialValue: selectedBreed,
        decoration: InputDecoration(
          labelText: 'Raza *',
          hintText: 'Selecciona la raza',
          prefixIcon: Icon(
            Icons.pets_rounded,
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
        items: allBreeds.map((breed) {
          return DropdownMenuItem<BreedType>(
            value: breed,
            child: Text(
              breed.displayName,
              style: Theme.of(context).textTheme.bodyMedium,
            ),
          );
        }).toList(),
        onChanged: enabled
            ? (breed) {
                if (breed != null) {
                  onChanged(breed);
                }
              }
            : null,
        validator: (value) {
          if (value == null) {
            return 'La raza es obligatoria';
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

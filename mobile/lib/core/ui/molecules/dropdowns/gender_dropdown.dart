/// Molecule: GenderDropdown
///
/// Dropdown para seleccionar género del animal.
/// Single Responsibility: Selector de género con validación.
///
/// Atomic Design - Molecules Layer
library;

import 'package:flutter/material.dart';

import '../../../../domain/entities/cattle.dart';

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
    return DropdownButtonFormField<Gender>(
      initialValue: selectedGender,
      decoration: const InputDecoration(
        labelText: 'Género *',
        hintText: 'Selecciona el género',
        prefixIcon: Icon(Icons.wc),
      ),
      items: Gender.values.map((gender) {
        return DropdownMenuItem<Gender>(
          value: gender,
          child: Text(gender.displayName),
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
    );
  }
}

/// Molecule: BreedDropdown
/// 
/// Dropdown para seleccionar raza bovina (7 razas exactas).
/// Single Responsibility: Selector de raza con validación.
///
/// Atomic Design - Molecules Layer
library;

import 'package:flutter/material.dart';

import '../../../constants/breeds.dart';

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
    return DropdownButtonFormField<BreedType>(
      value: selectedBreed,
      decoration: const InputDecoration(
        labelText: 'Raza *',
        hintText: 'Selecciona la raza',
        prefixIcon: Icon(Icons.pets),
      ),
      items: allBreeds.map((breed) {
        return DropdownMenuItem<BreedType>(
          value: breed,
          child: Text(breed.displayName),
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
    );
  }
}


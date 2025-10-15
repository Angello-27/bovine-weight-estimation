/// Organism: BreedSelectorGrid
/// 
/// Grid de selección de raza bovina (7 razas).
/// Single Responsibility: Permitir selección visual de raza.
///
/// Atomic Design - Organisms Layer
library;

import 'package:flutter/material.dart';

import '../../../constants/breeds.dart';
import '../../theme/app_colors.dart';
import '../../theme/app_spacing.dart';

/// Grid de selección de raza
class BreedSelectorGrid extends StatelessWidget {
  final BreedType? selectedBreed;
  final ValueChanged<BreedType> onBreedSelected;

  const BreedSelectorGrid({
    super.key,
    this.selectedBreed,
    required this.onBreedSelected,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Selecciona la raza',
          style: Theme.of(context).textTheme.titleMedium,
        ),
        
        const SizedBox(height: AppSpacing.md),
        
        // Grid 3x3 de razas (7 razas + 2 espacios)
        GridView.builder(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 3,
            mainAxisSpacing: AppSpacing.sm,
            crossAxisSpacing: AppSpacing.sm,
            childAspectRatio: 1.0,
          ),
          itemCount: allBreeds.length,
          itemBuilder: (context, index) {
            final breed = allBreeds[index];
            final isSelected = selectedBreed == breed;

            return _BreedCard(
              breed: breed,
              isSelected: isSelected,
              onTap: () => onBreedSelected(breed),
            );
          },
        ),
      ],
    );
  }
}

/// Card individual de raza
class _BreedCard extends StatelessWidget {
  final BreedType breed;
  final bool isSelected;
  final VoidCallback onTap;

  const _BreedCard({
    required this.breed,
    required this.isSelected,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: isSelected ? AppSpacing.elevationHigh : AppSpacing.elevationLow,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusMedium),
        side: isSelected
            ? const BorderSide(color: AppColors.primary, width: 2)
            : BorderSide.none,
      ),
      color: isSelected ? AppColors.primary.withOpacity(0.1) : null,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusMedium),
        child: Padding(
          padding: const EdgeInsets.all(AppSpacing.sm),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              // Icono de la raza
              Icon(
                Icons.pets,
                size: 40,
                color: isSelected ? AppColors.primary : Colors.grey[600],
              ),
              
              const SizedBox(height: AppSpacing.xs),
              
              // Nombre de la raza
              Text(
                breed.displayName,
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 12,
                  fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                  color: isSelected ? AppColors.primary : Colors.grey[800],
                ),
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
              
              // Checkmark si está seleccionado
              if (isSelected) ...[
                const SizedBox(height: AppSpacing.xs),
                const Icon(
                  Icons.check_circle,
                  size: 16,
                  color: AppColors.success,
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}


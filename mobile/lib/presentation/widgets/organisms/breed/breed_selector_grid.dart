/// Organism: BreedSelectorGrid
///
/// Grid de selección de raza bovina (7 razas) con animaciones.
/// Single Responsibility: Permitir selección visual de raza.
///
/// Atomic Design - Organisms Layer
library;

import 'package:flutter/material.dart';

import '../../../../core/constants/breeds.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../atoms/animated_scale_button.dart';

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
    return AnimatedScaleButton(
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        curve: Curves.easeInOut,
        decoration: BoxDecoration(
          color: isSelected
              ? AppColors.primary.withValues(alpha: 0.1)
              : AppColors.surface,
          borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
          border: Border.all(
            color: isSelected ? AppColors.primary : AppColors.grey300,
            width: isSelected ? 2.5 : 1,
          ),
          boxShadow: [
            BoxShadow(
              color: isSelected
                  ? AppColors.primary.withValues(alpha: 0.2)
                  : AppColors.grey300.withValues(alpha: 0.3),
              blurRadius: isSelected
                  ? AppSpacing.elevationHigh
                  : AppSpacing.elevationLow,
              offset: const Offset(0, 2),
            ),
          ],
        ),
        child: Padding(
          padding: const EdgeInsets.all(6.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            mainAxisSize: MainAxisSize.min,
            children: [
              // Icono de la raza
              AnimatedContainer(
                duration: const Duration(milliseconds: 200),
                padding: const EdgeInsets.all(AppSpacing.xs),
                decoration: BoxDecoration(
                  color: isSelected
                      ? AppColors.primary.withValues(alpha: 0.15)
                      : Colors.transparent,
                  borderRadius: BorderRadius.circular(
                    AppSpacing.borderRadiusMedium,
                  ),
                ),
                child: Icon(
                  Icons.pets,
                  size: AppSpacing.iconSize,
                  color: isSelected ? AppColors.primary : AppColors.grey600,
                ),
              ),

              const SizedBox(height: 2),

              // Nombre de la raza
              Flexible(
                child: Text(
                  breed.displayName,
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 11,
                    fontWeight: isSelected ? FontWeight.bold : FontWeight.w500,
                    color: isSelected ? AppColors.primary : AppColors.grey800,
                    height: 1.2,
                  ),
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
              ),

              // Checkmark si está seleccionado
              if (isSelected) ...[
                const SizedBox(height: 2),
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

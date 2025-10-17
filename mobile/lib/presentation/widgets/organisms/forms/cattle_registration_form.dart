/// Organism: CattleRegistrationForm
///
/// Formulario completo de registro de ganado.
/// Single Responsibility: Capturar datos de registro de animal.
///
/// Atomic Design - Organisms Layer
library;

import 'package:flutter/material.dart';

import '../../../../core/constants/age_categories.dart';
import '../../../../core/constants/breeds.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../domain/entities/cattle.dart';
import '../../atoms/inputs/text_input_field.dart';
import '../../molecules/dropdowns/breed_dropdown.dart';
import '../../molecules/dropdowns/gender_dropdown.dart';

/// Formulario de registro de ganado
class CattleRegistrationForm extends StatefulWidget {
  final GlobalKey<FormState> formKey;
  final TextEditingController earTagController;
  final TextEditingController nameController;
  final TextEditingController colorController;
  final TextEditingController birthWeightController;
  final TextEditingController observationsController;
  final BreedType? selectedBreed;
  final DateTime? selectedBirthDate;
  final Gender? selectedGender;
  final ValueChanged<BreedType> onBreedChanged;
  final ValueChanged<DateTime> onBirthDateChanged;
  final ValueChanged<Gender> onGenderChanged;

  const CattleRegistrationForm({
    super.key,
    required this.formKey,
    required this.earTagController,
    required this.nameController,
    required this.colorController,
    required this.birthWeightController,
    required this.observationsController,
    this.selectedBreed,
    this.selectedBirthDate,
    this.selectedGender,
    required this.onBreedChanged,
    required this.onBirthDateChanged,
    required this.onGenderChanged,
  });

  @override
  State<CattleRegistrationForm> createState() => _CattleRegistrationFormState();
}

class _CattleRegistrationFormState extends State<CattleRegistrationForm> {
  @override
  Widget build(BuildContext context) {
    return Form(
      key: widget.formKey,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Sección: Datos Obligatorios
          Container(
            padding: const EdgeInsets.symmetric(
              horizontal: AppSpacing.md,
              vertical: AppSpacing.sm,
            ),
            decoration: BoxDecoration(
              color: AppColors.primary.withValues(alpha: 0.05),
              borderRadius: BorderRadius.circular(
                AppSpacing.borderRadiusMedium,
              ),
              border: Border(
                left: BorderSide(color: AppColors.primary, width: 4),
              ),
            ),
            child: Row(
              children: [
                const Icon(
                  Icons.star,
                  color: AppColors.primary,
                  size: AppSpacing.iconSizeSmall,
                ),
                const SizedBox(width: AppSpacing.sm),
                Text(
                  'Datos Obligatorios',
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                    color: AppColors.primary,
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(height: AppSpacing.md),

          // Caravana (único, obligatorio)
          TextInputField(
            labelText: 'Número de Caravana *',
            hintText: 'Ej: A-001',
            controller: widget.earTagController,
            validator: (value) {
              if (value == null || value.trim().isEmpty) {
                return 'La caravana es obligatoria';
              }
              final regex = RegExp(r'^[A-Za-z0-9\-]+$');
              if (!regex.hasMatch(value)) {
                return 'Solo alfanuméricos y guiones';
              }
              return null;
            },
          ),

          const SizedBox(height: AppSpacing.md),

          // Raza (obligatorio)
          BreedDropdown(
            selectedBreed: widget.selectedBreed,
            onChanged: widget.onBreedChanged,
          ),

          const SizedBox(height: AppSpacing.md),

          // Fecha de nacimiento (obligatorio)
          TextInputField(
            labelText: 'Fecha de Nacimiento *',
            hintText: 'Selecciona fecha',
            readOnly: true,
            controller: TextEditingController(
              text: widget.selectedBirthDate != null
                  ? '${widget.selectedBirthDate!.day}/${widget.selectedBirthDate!.month}/${widget.selectedBirthDate!.year}'
                  : '',
            ),
            suffixIcon: const Icon(Icons.calendar_today),
            onTap: () => _selectBirthDate(context),
            validator: (value) {
              if (widget.selectedBirthDate == null) {
                return 'La fecha de nacimiento es obligatoria';
              }
              return null;
            },
          ),

          const SizedBox(height: AppSpacing.md),

          // Género (obligatorio)
          GenderDropdown(
            selectedGender: widget.selectedGender,
            onChanged: widget.onGenderChanged,
          ),

          const SizedBox(height: AppSpacing.lg),

          // Categoría de edad (calculada automáticamente)
          if (widget.selectedBirthDate != null) _buildAgeCategoryInfo(),

          const SizedBox(height: AppSpacing.lg),

          // Sección: Datos Opcionales
          Container(
            padding: const EdgeInsets.symmetric(
              horizontal: AppSpacing.md,
              vertical: AppSpacing.sm,
            ),
            decoration: BoxDecoration(
              color: AppColors.grey200,
              borderRadius: BorderRadius.circular(
                AppSpacing.borderRadiusMedium,
              ),
              border: Border(
                left: BorderSide(color: AppColors.grey500, width: 4),
              ),
            ),
            child: Row(
              children: [
                const Icon(
                  Icons.info_outline,
                  color: AppColors.grey600,
                  size: AppSpacing.iconSizeSmall,
                ),
                const SizedBox(width: AppSpacing.sm),
                Text(
                  'Datos Opcionales',
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.w600,
                    color: AppColors.grey700,
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(height: AppSpacing.md),

          // Nombre (opcional)
          TextInputField(
            labelText: 'Nombre',
            hintText: 'Ej: Brownie',
            controller: widget.nameController,
          ),

          const SizedBox(height: AppSpacing.md),

          // Color (opcional)
          TextInputField(
            labelText: 'Color',
            hintText: 'Ej: Pardo, Negro',
            controller: widget.colorController,
          ),

          const SizedBox(height: AppSpacing.md),

          // Peso al nacer (opcional)
          TextInputField(
            labelText: 'Peso al Nacer (kg)',
            hintText: 'Ej: 35',
            controller: widget.birthWeightController,
            keyboardType: TextInputType.number,
            validator: (value) {
              if (value != null && value.isNotEmpty) {
                final weight = double.tryParse(value);
                if (weight == null || weight < 10 || weight > 100) {
                  return 'Peso debe estar entre 10-100 kg';
                }
              }
              return null;
            },
          ),

          const SizedBox(height: AppSpacing.md),

          // Observaciones (opcional)
          TextInputField(
            labelText: 'Observaciones',
            hintText: 'Notas adicionales',
            controller: widget.observationsController,
            maxLines: 3,
          ),
        ],
      ),
    );
  }

  /// Widget de información de categoría de edad (calculada)
  Widget _buildAgeCategoryInfo() {
    final ageInMonths =
        DateTime.now().difference(widget.selectedBirthDate!).inDays ~/ 30;
    final category = AgeCategory.fromAgeInMonths(ageInMonths);

    return Container(
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [AppColors.infoLight, Colors.white],
        ),
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusMedium),
        border: Border.all(
          color: AppColors.info.withValues(alpha: 0.3),
          width: 1.5,
        ),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(AppSpacing.sm),
            decoration: BoxDecoration(
              color: AppColors.info.withValues(alpha: 0.15),
              borderRadius: BorderRadius.circular(AppSpacing.borderRadiusSmall),
            ),
            child: const Icon(
              Icons.cake,
              color: AppColors.info,
              size: AppSpacing.iconSize,
            ),
          ),
          const SizedBox(width: AppSpacing.md),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Categoría Automática',
                  style: Theme.of(context).textTheme.bodySmall?.copyWith(
                    color: AppColors.grey600,
                    fontWeight: FontWeight.w500,
                  ),
                ),
                const SizedBox(height: AppSpacing.xs),
                Text(
                  '${category.displayName} ($ageInMonths meses)',
                  style: Theme.of(context).textTheme.titleSmall?.copyWith(
                    color: AppColors.info,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  /// Selector de fecha de nacimiento
  Future<void> _selectBirthDate(BuildContext context) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: widget.selectedBirthDate ?? DateTime.now(),
      firstDate: DateTime(2004), // 20 años atrás
      lastDate: DateTime.now(), // No puede ser futura
      helpText: 'Selecciona fecha de nacimiento',
      cancelText: 'Cancelar',
      confirmText: 'Aceptar',
    );

    if (picked != null) {
      widget.onBirthDateChanged(picked);
    }
  }
}

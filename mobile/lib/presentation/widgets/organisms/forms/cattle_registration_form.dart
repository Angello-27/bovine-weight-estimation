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
import '../../../../core/theme/app_spacing.dart';
import '../../../../domain/entities/cattle.dart';
import '../../../../l10n/app_localizations.dart';
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
          Text(
            AppLocalizations.of(context)!.requiredData,
            style: Theme.of(context).textTheme.titleMedium?.copyWith(
              fontWeight: FontWeight.bold,
              color: Theme.of(context).colorScheme.onSurface,
            ),
          ),

          const SizedBox(height: AppSpacing.md),

          // Caravana (único, obligatorio)
          TextInputField(
            labelText: AppLocalizations.of(context)!.earTagNumber,
            hintText: AppLocalizations.of(context)!.earTagExample,
            controller: widget.earTagController,
            validator: (value) {
              if (value == null || value.trim().isEmpty) {
                return AppLocalizations.of(context)!.earTagRequired;
              }
              final regex = RegExp(r'^[A-Za-z0-9\-]+$');
              if (!regex.hasMatch(value)) {
                return AppLocalizations.of(context)!.earTagInvalid;
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
            labelText: AppLocalizations.of(context)!.birthDate,
            hintText: AppLocalizations.of(context)!.selectDate,
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
                return AppLocalizations.of(context)!.birthDateRequired;
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
          Text(
            AppLocalizations.of(context)!.optionalData,
            style: Theme.of(context).textTheme.titleMedium?.copyWith(
              fontWeight: FontWeight.bold,
              color: Theme.of(context).colorScheme.onSurface,
            ),
          ),

          const SizedBox(height: AppSpacing.md),

          // Nombre (opcional)
          TextInputField(
            labelText: AppLocalizations.of(context)!.name,
            hintText: AppLocalizations.of(context)!.nameExample,
            controller: widget.nameController,
          ),

          const SizedBox(height: AppSpacing.md),

          // Color (opcional)
          TextInputField(
            labelText: AppLocalizations.of(context)!.color,
            hintText: AppLocalizations.of(context)!.colorExample,
            controller: widget.colorController,
          ),

          const SizedBox(height: AppSpacing.md),

          // Peso al nacer (opcional)
          TextInputField(
            labelText: AppLocalizations.of(context)!.birthWeight,
            hintText: AppLocalizations.of(context)!.birthWeightExample,
            controller: widget.birthWeightController,
            keyboardType: TextInputType.number,
            validator: (value) {
              if (value != null && value.isNotEmpty) {
                final weight = double.tryParse(value);
                if (weight == null || weight < 10 || weight > 100) {
                  return AppLocalizations.of(context)!.birthWeightInvalid;
                }
              }
              return null;
            },
          ),

          const SizedBox(height: AppSpacing.md),

          // Observaciones (opcional)
          TextInputField(
            labelText: AppLocalizations.of(context)!.observations,
            hintText: AppLocalizations.of(context)!.observationsHint,
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
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [
            Theme.of(
              context,
            ).colorScheme.tertiaryContainer.withValues(alpha: 0.5),
            Theme.of(context).colorScheme.surface,
          ],
        ),
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusMedium),
        border: Border.all(
          color: Theme.of(context).colorScheme.tertiary.withValues(alpha: 0.3),
          width: 1.5,
        ),
        boxShadow: [
          BoxShadow(
            color: Theme.of(
              context,
            ).colorScheme.tertiary.withValues(alpha: 0.1),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(AppSpacing.sm),
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.tertiaryContainer,
              borderRadius: BorderRadius.circular(AppSpacing.borderRadiusSmall),
            ),
            child: Icon(
              Icons.cake_rounded,
              color: Theme.of(context).colorScheme.onTertiaryContainer,
              size: AppSpacing.iconSize,
            ),
          ),
          const SizedBox(width: AppSpacing.md),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  AppLocalizations.of(context)!.automaticCategory,
                  style: Theme.of(context).textTheme.bodySmall?.copyWith(
                    color: Theme.of(context).colorScheme.onSurfaceVariant,
                    fontWeight: FontWeight.w500,
                  ),
                ),
                const SizedBox(height: AppSpacing.xs),
                Text(
                  '${category.displayName} ($ageInMonths meses)',
                  style: Theme.of(context).textTheme.titleSmall?.copyWith(
                    color: Theme.of(context).colorScheme.tertiary,
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
    final l10n = AppLocalizations.of(context)!;
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: widget.selectedBirthDate ?? DateTime.now(),
      firstDate: DateTime(2004), // 20 años atrás
      lastDate: DateTime.now(), // No puede ser futura
      helpText: l10n.selectBirthDate,
      cancelText: l10n.cancel,
      confirmText: l10n.accept,
    );

    if (picked != null) {
      widget.onBirthDateChanged(picked);
    }
  }
}

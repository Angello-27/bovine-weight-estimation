/// Page: CattleRegistrationPage
/// 
/// US-003: Registro Automático de Animales
/// 
/// Pantalla para registrar un nuevo animal en el sistema.
/// Single Responsibility: Coordinar registro de ganado.
///
/// Presentation Layer - Pages
library;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../core/constants/breeds.dart';
import '../../../core/ui/atoms/buttons/primary_button.dart';
import '../../../core/ui/organisms/forms/cattle_registration_form.dart';
import '../../../core/ui/theme/app_colors.dart';
import '../../../core/ui/theme/app_spacing.dart';
import '../../../domain/entities/cattle.dart';
import '../../providers/cattle_provider.dart';

/// Pantalla de registro de ganado
class CattleRegistrationPage extends StatefulWidget {
  const CattleRegistrationPage({super.key});

  @override
  State<CattleRegistrationPage> createState() => _CattleRegistrationPageState();
}

class _CattleRegistrationPageState extends State<CattleRegistrationPage> {
  final _formKey = GlobalKey<FormState>();
  
  // Controllers
  final _earTagController = TextEditingController();
  final _nameController = TextEditingController();
  final _colorController = TextEditingController();
  final _birthWeightController = TextEditingController();
  final _observationsController = TextEditingController();

  // Form state
  BreedType? _selectedBreed;
  DateTime? _selectedBirthDate;
  Gender? _selectedGender;

  @override
  void dispose() {
    _earTagController.dispose();
    _nameController.dispose();
    _colorController.dispose();
    _birthWeightController.dispose();
    _observationsController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Registrar Animal'),
      ),
      body: Consumer<CattleProvider>(
        builder: (context, provider, child) {
          // Mostrar snackbar en éxito
          if (provider.state == CattleState.success &&
              provider.successMessage != null) {
            WidgetsBinding.instance.addPostFrameCallback((_) {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text(provider.successMessage!),
                  backgroundColor: AppColors.success,
                ),
              );
              provider.clearMessages();
              _clearForm();
            });
          }

          // Mostrar snackbar en error
          if (provider.hasError && provider.errorMessage != null) {
            WidgetsBinding.instance.addPostFrameCallback((_) {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text(provider.errorMessage!),
                  backgroundColor: AppColors.error,
                ),
              );
              provider.clearMessages();
            });
          }

          return SafeArea(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(AppSpacing.screenPadding),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  // Formulario
                  CattleRegistrationForm(
                    formKey: _formKey,
                    earTagController: _earTagController,
                    nameController: _nameController,
                    colorController: _colorController,
                    birthWeightController: _birthWeightController,
                    observationsController: _observationsController,
                    selectedBreed: _selectedBreed,
                    selectedBirthDate: _selectedBirthDate,
                    selectedGender: _selectedGender,
                    onBreedChanged: (breed) {
                      setState(() => _selectedBreed = breed);
                    },
                    onBirthDateChanged: (date) {
                      setState(() => _selectedBirthDate = date);
                    },
                    onGenderChanged: (gender) {
                      setState(() => _selectedGender = gender);
                    },
                  ),

                  const SizedBox(height: AppSpacing.xl),

                  // Botón de registro
                  PrimaryButton(
                    text: 'Registrar Animal',
                    icon: Icons.save,
                    isLoading: provider.isLoading,
                    onPressed: _handleRegister,
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }

  /// Maneja el registro del animal
  Future<void> _handleRegister() async {
    if (_formKey.currentState!.validate()) {
      final provider = context.read<CattleProvider>();

      await provider.registerCattle(
        earTag: _earTagController.text.trim(),
        name: _nameController.text.trim().isNotEmpty
            ? _nameController.text.trim()
            : null,
        breed: _selectedBreed!,
        birthDate: _selectedBirthDate!,
        gender: _selectedGender!,
        color: _colorController.text.trim().isNotEmpty
            ? _colorController.text.trim()
            : null,
        birthWeight: _birthWeightController.text.trim().isNotEmpty
            ? double.tryParse(_birthWeightController.text.trim())
            : null,
        observations: _observationsController.text.trim().isNotEmpty
            ? _observationsController.text.trim()
            : null,
      );
    }
  }

  /// Limpia el formulario
  void _clearForm() {
    _formKey.currentState?.reset();
    _earTagController.clear();
    _nameController.clear();
    _colorController.clear();
    _birthWeightController.clear();
    _observationsController.clear();
    setState(() {
      _selectedBreed = null;
      _selectedBirthDate = null;
      _selectedGender = null;
    });
  }
}


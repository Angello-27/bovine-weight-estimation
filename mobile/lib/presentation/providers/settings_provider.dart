/// Settings Provider
///
/// Provider para gestionar el estado de las preferencias del usuario.
/// Single Responsibility: Gestionar estado reactivo de settings.
///
/// Presentation Layer - Providers
library;

import 'package:flutter/foundation.dart';

import '../../core/usecases/usecase.dart';
import '../../domain/entities/app_settings.dart';
import '../../domain/usecases/get_settings_usecase.dart';
import '../../domain/usecases/save_settings_usecase.dart';

/// Provider de configuración
class SettingsProvider extends ChangeNotifier {
  final GetSettingsUseCase _getSettingsUseCase;
  final SaveSettingsUseCase _saveSettingsUseCase;

  AppSettings _settings = AppSettings.defaultSettings;
  bool _isLoading = false;
  String? _errorMessage;

  SettingsProvider({
    required GetSettingsUseCase getSettingsUseCase,
    required SaveSettingsUseCase saveSettingsUseCase,
  }) : _getSettingsUseCase = getSettingsUseCase,
       _saveSettingsUseCase = saveSettingsUseCase {
    _loadSettings();
  }

  // Getters
  AppSettings get settings => _settings;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;
  bool get hasError => _errorMessage != null;

  /// Carga las preferencias guardadas
  Future<void> _loadSettings() async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    final result = await _getSettingsUseCase(const NoParams());

    result.fold(
      (failure) {
        _errorMessage = failure.message;
        _isLoading = false;
        notifyListeners();
      },
      (settings) {
        _settings = settings;
        _isLoading = false;
        notifyListeners();
      },
    );
  }

  /// Actualiza y guarda las preferencias
  Future<void> updateSettings(AppSettings newSettings) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    final result = await _saveSettingsUseCase(SaveSettingsParams(newSettings));

    result.fold(
      (failure) {
        _errorMessage = failure.message;
        _isLoading = false;
        notifyListeners();
      },
      (_) {
        _settings = newSettings;
        _isLoading = false;
        notifyListeners();
      },
    );
  }

  /// Actualiza el modo de tema
  Future<void> updateThemeMode(AppThemeMode themeMode) async {
    await updateSettings(_settings.copyWith(themeMode: themeMode));
  }

  /// Actualiza el tamaño de texto
  Future<void> updateTextSize(TextSize textSize) async {
    await updateSettings(_settings.copyWith(textSize: textSize));
  }

  /// Actualiza el estado del flash
  Future<void> updateFlashEnabled(bool enabled) async {
    await updateSettings(_settings.copyWith(flashEnabled: enabled));
  }

  /// Actualiza la unidad de peso
  Future<void> updateWeightUnit(WeightUnit unit) async {
    await updateSettings(_settings.copyWith(weightUnit: unit));
  }

  /// Actualiza el formato de fecha
  Future<void> updateDateFormat(DateFormat format) async {
    await updateSettings(_settings.copyWith(dateFormat: format));
  }

  /// Actualiza el idioma
  Future<void> updateLanguage(AppLanguage language) async {
    await updateSettings(_settings.copyWith(language: language));
  }

  /// Limpia mensajes de error
  void clearError() {
    _errorMessage = null;
    notifyListeners();
  }
}

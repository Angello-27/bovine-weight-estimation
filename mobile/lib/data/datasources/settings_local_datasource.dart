/// Settings Local DataSource
///
/// DataSource para persistir y recuperar preferencias del usuario.
/// Single Responsibility: Gestionar almacenamiento local de settings.
///
/// Data Layer - DataSources
library;

import 'dart:async';

import 'package:shared_preferences/shared_preferences.dart';

import '../../domain/entities/app_settings.dart';

/// Clave de preferencias
class SettingsKeys {
  static const String themeMode = 'theme_mode';
  static const String textSize = 'text_size';
  static const String flashEnabled = 'flash_enabled';
  static const String weightUnit = 'weight_unit';
  static const String dateFormat = 'date_format';
  static const String language = 'language';
  static const String captureFps = 'capture_fps';
}

/// DataSource local para settings
abstract class SettingsLocalDataSource {
  /// Obtiene las preferencias guardadas
  Future<AppSettings> getSettings();

  /// Guarda las preferencias
  Future<void> saveSettings(AppSettings settings);
}

/// Implementación de SettingsLocalDataSource
class SettingsLocalDataSourceImpl implements SettingsLocalDataSource {
  final SharedPreferences _prefs;

  SettingsLocalDataSourceImpl({required SharedPreferences prefs})
    : _prefs = prefs;

  @override
  Future<AppSettings> getSettings() async {
    return AppSettings(
      themeMode: _getThemeMode(),
      textSize: _getTextSize(),
      flashEnabled: _prefs.getBool(SettingsKeys.flashEnabled) ?? false,
      weightUnit: _getWeightUnit(),
      dateFormat: _getDateFormat(),
      language: _getLanguage(),
      captureFps: _prefs.getInt(SettingsKeys.captureFps) ?? 5,
    );
  }

  @override
  Future<void> saveSettings(AppSettings settings) async {
    await Future.wait([
      _prefs.setString(SettingsKeys.themeMode, settings.themeMode.name),
      _prefs.setString(SettingsKeys.textSize, settings.textSize.name),
      _prefs.setBool(SettingsKeys.flashEnabled, settings.flashEnabled),
      _prefs.setString(SettingsKeys.weightUnit, settings.weightUnit.name),
      _prefs.setString(SettingsKeys.dateFormat, settings.dateFormat.name),
      _prefs.setString(SettingsKeys.language, settings.language.name),
      _prefs.setInt(SettingsKeys.captureFps, settings.captureFps),
    ]);
  }

  AppThemeMode _getThemeMode() {
    final value = _prefs.getString(SettingsKeys.themeMode);
    if (value == null) return AppThemeMode.system;
    return AppThemeMode.values.firstWhere(
      (e) => e.name == value,
      orElse: () => AppThemeMode.system,
    );
  }

  TextSize _getTextSize() {
    final value = _prefs.getString(SettingsKeys.textSize);
    if (value == null) return TextSize.normal;
    return TextSize.values.firstWhere(
      (e) => e.name == value,
      orElse: () => TextSize.normal,
    );
  }

  WeightUnit _getWeightUnit() {
    final value = _prefs.getString(SettingsKeys.weightUnit);
    if (value == null) return WeightUnit.kilograms;
    return WeightUnit.values.firstWhere(
      (e) => e.name == value,
      orElse: () => WeightUnit.kilograms,
    );
  }

  DateFormat _getDateFormat() {
    final value = _prefs.getString(SettingsKeys.dateFormat);
    if (value == null) return DateFormat.dayMonthYear;
    return DateFormat.values.firstWhere(
      (e) => e.name == value,
      orElse: () => DateFormat.dayMonthYear,
    );
  }

  AppLanguage _getLanguage() {
    final value = _prefs.getString(SettingsKeys.language);
    if (value == null) return AppLanguage.spanish;
    return AppLanguage.values.firstWhere(
      (e) => e.name == value,
      orElse: () => AppLanguage.spanish,
    );
  }
}

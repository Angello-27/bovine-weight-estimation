/// Locale Helper
///
/// Utilidades para convertir entre AppLanguage y Locale de Flutter.
/// Single Responsibility: Conversión de tipos de idioma.
///
/// Core Layer - Utils
library;

import 'package:flutter/material.dart';

import '../../domain/entities/app_settings.dart';

/// Helper para conversión de idiomas
class LocaleHelper {
  /// Convierte AppLanguage a Locale
  static Locale appLanguageToLocale(AppLanguage language) {
    switch (language) {
      case AppLanguage.spanish:
        return const Locale('es');
      case AppLanguage.portuguese:
        return const Locale('pt');
    }
  }

  /// Convierte Locale a AppLanguage
  static AppLanguage localeToAppLanguage(Locale locale) {
    switch (locale.languageCode) {
      case 'es':
        return AppLanguage.spanish;
      case 'pt':
        return AppLanguage.portuguese;
      default:
        return AppLanguage.spanish; // Default a español
    }
  }
}

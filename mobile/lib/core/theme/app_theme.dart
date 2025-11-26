/// App Theme - Material Design 3
///
/// Tema completo de la aplicación.
/// Single Responsibility: Exportar temas claro y oscuro.
///
/// Core UI Theme Layer
library;

import 'package:flutter/material.dart';

import 'app_theme_dark.dart';
import 'app_theme_light.dart';

/// Tema de la aplicación
///
/// Exporta los temas claro y oscuro desde archivos separados
class AppTheme {
  /// Tema claro (principal)
  static ThemeData get lightTheme {
    return AppThemeLight.theme;
  }

  /// Tema oscuro
  static ThemeData get darkTheme {
    return AppThemeDark.theme;
  }
}

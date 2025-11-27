/// App Theme - Material Design 3
///
/// Tema completo de la aplicación.
/// Single Responsibility: Exportar temas claro y oscuro.
///
/// Core UI Theme Layer
library;

import 'package:flutter/material.dart';

import '../../domain/entities/app_settings.dart';
import 'app_theme_dark.dart';
import 'app_theme_light.dart';

/// Tema de la aplicación
///
/// Exporta los temas claro y oscuro desde archivos separados
class AppTheme {
  /// Factor de escala para tamaño de texto
  /// Público para que pueda ser usado por otros widgets que necesiten escalar dimensiones
  static double getTextScaleFactor(TextSize textSize) {
    switch (textSize) {
      case TextSize.small:
        return 0.85;
      case TextSize.normal:
        return 1.0;
      case TextSize.large:
        return 1.15;
      case TextSize.extraLarge:
        return 1.3;
    }
  }

  /// Factor de escala para tamaño de texto (método privado para uso interno)
  static double _getTextScaleFactor(TextSize textSize) {
    return getTextScaleFactor(textSize);
  }

  /// Tamaños de fuente base para Material Design 3 (en sp)
  /// Estos son los tamaños estándar que se escalarán según la preferencia del usuario
  static const Map<String, double> _baseFontSizes = {
    'displayLarge': 57.0,
    'displayMedium': 45.0,
    'displaySmall': 36.0,
    'headlineLarge': 32.0,
    'headlineMedium': 28.0,
    'headlineSmall': 24.0,
    'titleLarge': 22.0,
    'titleMedium': 16.0,
    'titleSmall': 14.0,
    'bodyLarge': 16.0,
    'bodyMedium': 14.0,
    'bodySmall': 12.0,
    'labelLarge': 14.0,
    'labelMedium': 12.0,
    'labelSmall': 11.0,
  };

  /// Escala un TextTheme con el factor dado usando tamaños base fijos
  static TextTheme _scaleTextTheme(TextTheme baseTheme, double scaleFactor) {
    if (scaleFactor == 1.0) return baseTheme;

    // Función helper para escalar un TextStyle usando tamaño base
    TextStyle? scaleStyle(TextStyle? style, String styleKey) {
      if (style == null) return null;

      // Obtener tamaño base para este estilo
      final baseSize = _baseFontSizes[styleKey] ?? 14.0;
      // Calcular tamaño escalado
      final scaledSize = baseSize * scaleFactor;

      // Copiar el estilo y aplicar el tamaño escalado
      return style.copyWith(fontSize: scaledSize);
    }

    return TextTheme(
      displayLarge: scaleStyle(baseTheme.displayLarge, 'displayLarge'),
      displayMedium: scaleStyle(baseTheme.displayMedium, 'displayMedium'),
      displaySmall: scaleStyle(baseTheme.displaySmall, 'displaySmall'),
      headlineLarge: scaleStyle(baseTheme.headlineLarge, 'headlineLarge'),
      headlineMedium: scaleStyle(baseTheme.headlineMedium, 'headlineMedium'),
      headlineSmall: scaleStyle(baseTheme.headlineSmall, 'headlineSmall'),
      titleLarge: scaleStyle(baseTheme.titleLarge, 'titleLarge'),
      titleMedium: scaleStyle(baseTheme.titleMedium, 'titleMedium'),
      titleSmall: scaleStyle(baseTheme.titleSmall, 'titleSmall'),
      bodyLarge: scaleStyle(baseTheme.bodyLarge, 'bodyLarge'),
      bodyMedium: scaleStyle(baseTheme.bodyMedium, 'bodyMedium'),
      bodySmall: scaleStyle(baseTheme.bodySmall, 'bodySmall'),
      labelLarge: scaleStyle(baseTheme.labelLarge, 'labelLarge'),
      labelMedium: scaleStyle(baseTheme.labelMedium, 'labelMedium'),
      labelSmall: scaleStyle(baseTheme.labelSmall, 'labelSmall'),
    );
  }

  /// Tamaño base para AppBar title (en sp)
  static const double _baseAppBarTitleSize = 20.0;

  /// Escala el AppBarTheme usando tamaño base fijo
  static AppBarThemeData? _scaleAppBarTheme(
    AppBarThemeData? baseAppBarTheme,
    double scaleFactor,
  ) {
    if (baseAppBarTheme == null || scaleFactor == 1.0) {
      return baseAppBarTheme;
    }

    final titleTextStyle = baseAppBarTheme.titleTextStyle;
    if (titleTextStyle == null) {
      return baseAppBarTheme;
    }

    // Calcular tamaño escalado desde el base
    final scaledSize = _baseAppBarTitleSize * scaleFactor;

    return baseAppBarTheme.copyWith(
      titleTextStyle: titleTextStyle.copyWith(fontSize: scaledSize),
    );
  }

  /// Tema claro (principal)
  static ThemeData lightTheme({TextSize textSize = TextSize.normal}) {
    final scaleFactor = _getTextScaleFactor(textSize);
    final baseTheme = AppThemeLight.theme;

    return baseTheme.copyWith(
      textTheme: _scaleTextTheme(baseTheme.textTheme, scaleFactor),
      appBarTheme: _scaleAppBarTheme(baseTheme.appBarTheme, scaleFactor),
    );
  }

  /// Tema oscuro
  static ThemeData darkTheme({TextSize textSize = TextSize.normal}) {
    final scaleFactor = _getTextScaleFactor(textSize);
    final baseTheme = AppThemeDark.theme;

    return baseTheme.copyWith(
      textTheme: _scaleTextTheme(baseTheme.textTheme, scaleFactor),
      appBarTheme: _scaleAppBarTheme(baseTheme.appBarTheme, scaleFactor),
    );
  }
}

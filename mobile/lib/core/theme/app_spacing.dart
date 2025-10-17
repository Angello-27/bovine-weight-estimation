/// App Spacing - Material Design 3
///
/// Sistema de espaciado consistente (múltiplos de 4dp).
///
/// Core UI - Design System
library;

/// Espaciado de la aplicación
class AppSpacing {
  // Espaciado base (múltiplos de 4dp)
  static const double xs = 4.0; // Extra small
  static const double sm = 8.0; // Small
  static const double md = 16.0; // Medium (estándar)
  static const double lg = 24.0; // Large
  static const double xl = 32.0; // Extra large
  static const double xxl = 48.0; // Extra extra large

  // Padding de componentes
  static const double buttonPadding = 16.0;
  static const double cardPadding = 16.0;
  static const double screenPadding = 16.0;

  // Bordes redondeados (más suaves para look moderno)
  static const double borderRadiusSmall = 8.0;
  static const double borderRadiusMedium = 12.0;
  static const double borderRadiusLarge = 20.0;
  static const double borderRadiusXLarge = 28.0;
  static const double borderRadiusCircle = 999.0;

  // Tamaños de componentes
  static const double minButtonHeight = 48.0; // Táctil con guantes
  static const double minTapTarget = 48.0; // Material Design mínimo
  static const double iconSize = 24.0;
  static const double iconSizeLarge = 32.0;
  static const double iconSizeSmall = 20.0;
  static const double iconSizeXSmall = 16.0;
  static const double iconSizeXLarge = 40.0;
  static const double iconSizeXXLarge = 64.0;
  static const double iconSizeHero = 100.0; // Logo/Hero icons
  static const double avatarSize = 56.0;

  // Elevación (sombras más pronunciadas para depth moderno)
  static const double elevationNone = 0.0;
  static const double elevationLow = 2.0;
  static const double elevationMedium = 6.0;
  static const double elevationHigh = 12.0;
  static const double elevationXHigh = 20.0;

  // Tamaños de fuente
  static const double fontSizeSmall = 12.0;
  static const double fontSizeMedium = 14.0;
  static const double fontSizeNormal = 16.0;
  static const double fontSizeLarge = 20.0;
  static const double fontSizeTitle = 24.0;
}

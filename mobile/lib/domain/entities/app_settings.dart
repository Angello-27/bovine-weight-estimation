/// App Settings Entity
///
/// Entidad que representa las preferencias de configuración del usuario.
/// Single Responsibility: Modelar las configuraciones de la aplicación.
///
/// Domain Layer - Entities
library;

/// Configuración de tema visual
enum AppThemeMode {
  /// Sigue la preferencia del sistema
  system,

  /// Modo claro forzado
  light,

  /// Modo oscuro forzado
  dark,
}

/// Unidades de medida
enum WeightUnit {
  /// Kilogramos
  kilograms,

  /// Libras
  pounds,
}

/// Formato de fecha
enum DateFormat {
  /// DD/MM/YYYY
  dayMonthYear,

  /// MM/DD/YYYY
  monthDayYear,

  /// YYYY-MM-DD
  yearMonthDay,
}

/// Idioma de la interfaz
enum AppLanguage {
  /// Español
  spanish,

  /// Inglés
  english,
}

/// Tamaño de texto
enum TextSize {
  /// Pequeño
  small,

  /// Normal
  normal,

  /// Grande
  large,

  /// Extra grande
  extraLarge,
}

/// Entidad de configuración de la aplicación
class AppSettings {
  /// Modo de tema
  final AppThemeMode themeMode;

  /// Tamaño de texto
  final TextSize textSize;

  /// Flash activado durante captura
  final bool flashEnabled;

  /// Unidad de peso
  final WeightUnit weightUnit;

  /// Formato de fecha
  final DateFormat dateFormat;

  /// Idioma de la interfaz
  final AppLanguage language;

  const AppSettings({
    this.themeMode = AppThemeMode.system,
    this.textSize = TextSize.normal,
    this.flashEnabled = false,
    this.weightUnit = WeightUnit.kilograms,
    this.dateFormat = DateFormat.dayMonthYear,
    this.language = AppLanguage.spanish,
  });

  /// Crea una copia con valores modificados
  AppSettings copyWith({
    AppThemeMode? themeMode,
    TextSize? textSize,
    bool? flashEnabled,
    WeightUnit? weightUnit,
    DateFormat? dateFormat,
    AppLanguage? language,
  }) {
    return AppSettings(
      themeMode: themeMode ?? this.themeMode,
      textSize: textSize ?? this.textSize,
      flashEnabled: flashEnabled ?? this.flashEnabled,
      weightUnit: weightUnit ?? this.weightUnit,
      dateFormat: dateFormat ?? this.dateFormat,
      language: language ?? this.language,
    );
  }

  /// Configuración por defecto
  static const AppSettings defaultSettings = AppSettings();
}

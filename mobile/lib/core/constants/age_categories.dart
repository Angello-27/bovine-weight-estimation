/// Categorías de Edad Bovinas - Hacienda Gamelera
/// 4 categorías exactas (NO MODIFICAR sin autorización de Bruno Brito Macedo)

/// Enum de categorías de edad
enum AgeCategory {
  terneros('terneros', 'Terneros', '<8 meses', 0, 8),
  vaquillonasTorillo(
    'vaquillonas_torillos',
    'Vaquillonas/Torillos',
    '6-18 meses',
    6,
    18,
  ),
  vaquillonasToretes(
    'vaquillonas_toretes',
    'Vaquillonas/Toretes',
    '19-30 meses',
    19,
    30,
  ),
  vacasToros('vacas_toros', 'Vacas/Toros', '>30 meses', 30, null);

  const AgeCategory(
    this.value,
    this.displayName,
    this.rangeDescription,
    this.minMonths,
    this.maxMonths,
  );

  /// Valor para almacenamiento/API
  final String value;
  
  /// Nombre para mostrar en UI
  final String displayName;
  
  /// Descripción del rango
  final String rangeDescription;
  
  /// Edad mínima en meses
  final int minMonths;
  
  /// Edad máxima en meses (null = sin límite)
  final int? maxMonths;

  /// Valida si un string es una categoría válida
  static bool isValid(String category) {
    try {
      fromValue(category);
      return true;
    } catch (_) {
      return false;
    }
  }

  /// Obtiene AgeCategory desde string value
  static AgeCategory fromValue(String value) {
    return AgeCategory.values.firstWhere(
      (category) => category.value == value,
      orElse: () => throw ArgumentError('Categoría de edad inválida: $value'),
    );
  }

  /// Obtiene categoría apropiada según edad en meses
  static AgeCategory fromAgeInMonths(int months) {
    if (months < 8) return AgeCategory.terneros;
    if (months >= 6 && months <= 18) return AgeCategory.vaquillonasTorillo;
    if (months >= 19 && months <= 30) return AgeCategory.vaquillonasToretes;
    return AgeCategory.vacasToros;
  }

  /// Verifica si una edad en meses pertenece a esta categoría
  bool containsAge(int months) {
    if (maxMonths == null) {
      return months >= minMonths;
    }
    return months >= minMonths && months <= maxMonths!;
  }
}

/// Lista de todas las categorías para uso en dropdowns
const List<AgeCategory> allAgeCategories = AgeCategory.values;


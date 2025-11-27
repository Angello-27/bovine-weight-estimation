/// Weight Converter Utility
///
/// Utilidad para convertir peso entre unidades.
/// Single Responsibility: Conversión de unidades de peso.
///
/// Core Utils Layer
library;

import '../../domain/entities/app_settings.dart';

/// Utilidad para conversión de peso
class WeightConverter {
  /// Factor de conversión: 1 kg = 2.20462 lb
  static const double kgToLbFactor = 2.20462;

  /// Convierte kilogramos a libras
  static double kgToLb(double kg) {
    return kg * kgToLbFactor;
  }

  /// Convierte libras a kilogramos
  static double lbToKg(double lb) {
    return lb / kgToLbFactor;
  }

  /// Formatea el peso según la unidad configurada
  static String formatWeight(double weightInKg, WeightUnit unit) {
    final value = unit == WeightUnit.kilograms
        ? weightInKg
        : kgToLb(weightInKg);
    final unitLabel = unit == WeightUnit.kilograms ? 'kg' : 'lb';
    return '${value.toStringAsFixed(1)} $unitLabel';
  }

  /// Obtiene el peso convertido según la unidad
  static double getWeightInUnit(double weightInKg, WeightUnit unit) {
    return unit == WeightUnit.kilograms ? weightInKg : kgToLb(weightInKg);
  }
}

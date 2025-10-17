/// Provider: WeightHistoryProvider
///
/// US-004: Provider para gestión de historial de pesajes.
/// Implementa lógica de UI para análisis y gráficos.
///
/// Presentation Layer - Provider Pattern
library;

import 'package:flutter/material.dart';

import '../../domain/entities/weight_history.dart';
import '../../domain/usecases/get_weight_history_usecase.dart';

/// Estados del historial
enum WeightHistoryState {
  /// Estado inicial
  idle,

  /// Cargando historial
  loading,

  /// Historial cargado exitosamente
  loaded,

  /// Error al cargar
  error,
}

/// Extension para UI del estado
extension WeightHistoryStateUI on WeightHistoryState {
  IconData get icon {
    switch (this) {
      case WeightHistoryState.idle:
        return Icons.history;
      case WeightHistoryState.loading:
        return Icons.hourglass_empty;
      case WeightHistoryState.loaded:
        return Icons.check_circle;
      case WeightHistoryState.error:
        return Icons.error;
    }
  }

  Color get color {
    switch (this) {
      case WeightHistoryState.idle:
        return Colors.grey;
      case WeightHistoryState.loading:
        return Colors.blue;
      case WeightHistoryState.loaded:
        return Colors.green;
      case WeightHistoryState.error:
        return Colors.red;
    }
  }
}

/// Provider para gestión de historial de pesajes
class WeightHistoryProvider with ChangeNotifier {
  final GetWeightHistoryUseCase getWeightHistoryUseCase;

  /// Estado actual
  WeightHistoryState _state = WeightHistoryState.idle;

  /// Historial actual
  WeightHistory? _history;

  /// Mensaje de error
  String? _errorMessage;

  /// Período de filtro seleccionado
  HistoryPeriod _selectedPeriod = HistoryPeriod.all;

  /// Fecha inicio personalizada
  DateTime? _customStartDate;

  /// Fecha fin personalizada
  DateTime? _customEndDate;

  WeightHistoryProvider({required this.getWeightHistoryUseCase});

  // Getters
  WeightHistoryState get state => _state;
  WeightHistory? get history => _history;
  String? get errorMessage => _errorMessage;
  HistoryPeriod get selectedPeriod => _selectedPeriod;
  DateTime? get customStartDate => _customStartDate;
  DateTime? get customEndDate => _customEndDate;

  bool get isLoading => _state == WeightHistoryState.loading;
  bool get hasHistory => _history != null && _history!.weighings.isNotEmpty;
  bool get hasError => _state == WeightHistoryState.error;

  /// Carga el historial de un animal
  Future<void> loadHistory(String cattleId) async {
    _state = WeightHistoryState.loading;
    _errorMessage = null;
    notifyListeners();

    try {
      // Calcular fechas según período seleccionado
      DateTime? startDate;
      DateTime? endDate;

      if (_selectedPeriod != HistoryPeriod.all) {
        endDate = DateTime.now();
        startDate = _calculateStartDate(endDate, _selectedPeriod);
      }

      // Si hay período personalizado, usar esas fechas
      if (_selectedPeriod == HistoryPeriod.custom &&
          _customStartDate != null &&
          _customEndDate != null) {
        startDate = _customStartDate;
        endDate = _customEndDate;
      }

      // Obtener historial
      final params = WeightHistoryParams(
        cattleId: cattleId,
        startDate: startDate,
        endDate: endDate,
      );

      _history = await getWeightHistoryUseCase(params);
      _state = WeightHistoryState.loaded;
      notifyListeners();
    } catch (e) {
      _errorMessage = e.toString();
      _state = WeightHistoryState.error;
      notifyListeners();
    }
  }

  /// Cambia el período de filtro
  void setPeriod(HistoryPeriod period) {
    _selectedPeriod = period;
    notifyListeners();
  }

  /// Establece fechas personalizadas
  void setCustomDates({
    required DateTime startDate,
    required DateTime endDate,
  }) {
    _customStartDate = startDate;
    _customEndDate = endDate;
    _selectedPeriod = HistoryPeriod.custom;
    notifyListeners();
  }

  /// Reinicia el provider
  void reset() {
    _state = WeightHistoryState.idle;
    _history = null;
    _errorMessage = null;
    _selectedPeriod = HistoryPeriod.all;
    _customStartDate = null;
    _customEndDate = null;
    notifyListeners();
  }

  /// Calcula fecha de inicio según período
  DateTime _calculateStartDate(DateTime endDate, HistoryPeriod period) {
    switch (period) {
      case HistoryPeriod.lastWeek:
        return endDate.subtract(const Duration(days: 7));
      case HistoryPeriod.lastMonth:
        return DateTime(endDate.year, endDate.month - 1, endDate.day);
      case HistoryPeriod.lastQuarter:
        return DateTime(endDate.year, endDate.month - 3, endDate.day);
      case HistoryPeriod.lastYear:
        return DateTime(endDate.year - 1, endDate.month, endDate.day);
      case HistoryPeriod.all:
      case HistoryPeriod.custom:
        return endDate; // No se usa en estos casos
    }
  }
}

/// Períodos de filtro de historial
enum HistoryPeriod {
  /// Toda la historia
  all,

  /// Última semana
  lastWeek,

  /// Último mes
  lastMonth,

  /// Último trimestre
  lastQuarter,

  /// Último año
  lastYear,

  /// Período personalizado
  custom,
}

/// Extension para períodos
extension HistoryPeriodExtension on HistoryPeriod {
  String get displayName {
    switch (this) {
      case HistoryPeriod.all:
        return 'Todo el Historial';
      case HistoryPeriod.lastWeek:
        return 'Última Semana';
      case HistoryPeriod.lastMonth:
        return 'Último Mes';
      case HistoryPeriod.lastQuarter:
        return 'Último Trimestre';
      case HistoryPeriod.lastYear:
        return 'Último Año';
      case HistoryPeriod.custom:
        return 'Personalizado';
    }
  }
}

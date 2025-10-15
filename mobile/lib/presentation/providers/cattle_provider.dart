/// Provider: CattleProvider
/// 
/// Provider para gestionar el estado de registro y gestión de ganado (US-003).
/// Single Responsibility: State management de ganado.
///
/// Presentation Layer - Provider Pattern
library;

import 'package:flutter/foundation.dart';

import '../../core/constants/breeds.dart';
import '../../domain/entities/cattle.dart';
import '../../domain/usecases/register_cattle_usecase.dart';

/// Estados de gestión de ganado
enum CattleState {
  /// Estado inicial
  idle,

  /// Cargando datos
  loading,

  /// Registro/actualización exitosa
  success,

  /// Error
  error,
}

/// Provider para gestión de ganado
class CattleProvider with ChangeNotifier {
  final RegisterCattleUseCase registerCattleUseCase;

  /// Estado actual
  CattleState _state = CattleState.idle;

  /// Lista de animales
  List<Cattle> _cattleList = [];

  /// Animal actualmente seleccionado/editando
  Cattle? _selectedCattle;

  /// Mensaje de error (si existe)
  String? _errorMessage;

  /// Mensaje de éxito (si existe)
  String? _successMessage;

  CattleProvider({
    required this.registerCattleUseCase,
  });

  // Getters
  CattleState get state => _state;
  List<Cattle> get cattleList => _cattleList;
  Cattle? get selectedCattle => _selectedCattle;
  String? get errorMessage => _errorMessage;
  String? get successMessage => _successMessage;

  /// Indica si está cargando
  bool get isLoading => _state == CattleState.loading;

  /// Indica si hay error
  bool get hasError => _state == CattleState.error;

  /// Conteo total de animales
  int get totalCount => _cattleList.length;

  /// Animales activos
  List<Cattle> get activeCattle =>
      _cattleList.where((c) => c.status == CattleStatus.active).toList();

  /// Registra un nuevo animal
  Future<void> registerCattle({
    required String earTag,
    String? name,
    required BreedType breed,
    required DateTime birthDate,
    required Gender gender,
    String? color,
    double? birthWeight,
    String? motherId,
    String? fatherId,
    String? observations,
    String? photoPath,
  }) async {
    try {
      _state = CattleState.loading;
      _errorMessage = null;
      _successMessage = null;
      notifyListeners();

      // Crear parámetros
      final params = RegisterCattleParams(
        earTag: earTag,
        name: name,
        breed: breed,
        birthDate: birthDate,
        gender: gender,
        color: color,
        birthWeight: birthWeight,
        motherId: motherId,
        fatherId: fatherId,
        observations: observations,
        photoPath: photoPath,
      );

      // Ejecutar registro
      final result = await registerCattleUseCase.call(params);

      result.fold(
        // Error
        (failure) {
          _state = CattleState.error;
          _errorMessage = failure.message;
          _successMessage = null;
          notifyListeners();
        },
        // Éxito
        (cattle) {
          _state = CattleState.success;
          _cattleList.insert(0, cattle); // Agregar al inicio
          _errorMessage = null;
          _successMessage = 'Animal registrado exitosamente: ${cattle.earTag}';
          notifyListeners();
        },
      );
    } catch (e) {
      _state = CattleState.error;
      _errorMessage = 'Error inesperado: $e';
      _successMessage = null;
      notifyListeners();
    }
  }

  /// Selecciona un animal
  void selectCattle(Cattle cattle) {
    _selectedCattle = cattle;
    notifyListeners();
  }

  /// Deselecciona el animal actual
  void deselectCattle() {
    _selectedCattle = null;
    notifyListeners();
  }

  /// Reinicia el provider a estado inicial
  void reset() {
    _state = CattleState.idle;
    _errorMessage = null;
    _successMessage = null;
    _selectedCattle = null;
    notifyListeners();
  }

  /// Limpia mensajes
  void clearMessages() {
    _errorMessage = null;
    _successMessage = null;
    notifyListeners();
  }

  @override
  void dispose() {
    _cattleList = [];
    _selectedCattle = null;
    super.dispose();
  }
}


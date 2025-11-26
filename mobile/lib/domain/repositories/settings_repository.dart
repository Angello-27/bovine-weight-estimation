/// Settings Repository Interface
///
/// Contrato para gestión de preferencias del usuario.
/// Single Responsibility: Definir operaciones de settings.
///
/// Domain Layer - Repositories
library;

import 'package:dartz/dartz.dart';

import '../../core/errors/failures.dart';
import '../entities/app_settings.dart';

/// Repositorio de configuración
abstract class SettingsRepository {
  /// Obtiene las preferencias actuales
  Future<Either<Failure, AppSettings>> getSettings();

  /// Guarda las preferencias
  Future<Either<Failure, void>> saveSettings(AppSettings settings);
}

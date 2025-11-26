/// Get Settings UseCase
///
/// Caso de uso para obtener las preferencias del usuario.
/// Single Responsibility: Obtener configuración actual.
///
/// Domain Layer - UseCases
library;

import 'package:dartz/dartz.dart';

import '../../core/errors/failures.dart';
import '../../core/usecases/usecase.dart';
import '../entities/app_settings.dart';
import '../repositories/settings_repository.dart';

/// UseCase para obtener settings
class GetSettingsUseCase implements UseCase<AppSettings, NoParams> {
  final SettingsRepository _repository;

  GetSettingsUseCase(this._repository);

  @override
  Future<Either<Failure, AppSettings>> call(NoParams params) {
    return _repository.getSettings();
  }
}

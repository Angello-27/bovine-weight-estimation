/// Save Settings UseCase
///
/// Caso de uso para guardar las preferencias del usuario.
/// Single Responsibility: Persistir configuración.
///
/// Domain Layer - UseCases
library;

import 'package:dartz/dartz.dart';

import '../../core/errors/failures.dart';
import '../../core/usecases/usecase.dart';
import '../entities/app_settings.dart';
import '../repositories/settings_repository.dart';

/// Parámetros para guardar settings
class SaveSettingsParams {
  final AppSettings settings;

  const SaveSettingsParams(this.settings);
}

/// UseCase para guardar settings
class SaveSettingsUseCase implements UseCase<void, SaveSettingsParams> {
  final SettingsRepository _repository;

  SaveSettingsUseCase(this._repository);

  @override
  Future<Either<Failure, void>> call(SaveSettingsParams params) {
    return _repository.saveSettings(params.settings);
  }
}

/// Settings Repository Implementation
///
/// Implementación del repositorio de configuración.
/// Single Responsibility: Implementar operaciones de settings.
///
/// Data Layer - Repositories
library;

import 'package:dartz/dartz.dart';

import '../../core/errors/failures.dart';
import '../../domain/entities/app_settings.dart';
import '../../domain/repositories/settings_repository.dart';
import '../datasources/settings_local_datasource.dart';

/// Implementación del repositorio de settings
class SettingsRepositoryImpl implements SettingsRepository {
  final SettingsLocalDataSource _localDataSource;

  SettingsRepositoryImpl({required SettingsLocalDataSource localDataSource})
    : _localDataSource = localDataSource;

  @override
  Future<Either<Failure, AppSettings>> getSettings() async {
    try {
      final settings = await _localDataSource.getSettings();
      return Right(settings);
    } on Exception catch (e) {
      return Left(ServerFailure(message: e.toString()));
    }
  }

  @override
  Future<Either<Failure, void>> saveSettings(AppSettings settings) async {
    try {
      await _localDataSource.saveSettings(settings);
      return const Right(null);
    } on Exception catch (e) {
      return Left(ServerFailure(message: e.toString()));
    }
  }
}

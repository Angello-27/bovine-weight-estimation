/// UseCase: CheckConnectivityUseCase
///
/// US-005: Sincronización Offline
///
/// Caso de uso que verifica la conectividad con el backend.
/// Usado para mostrar indicador visual: offline/online/sincronizando.
///
/// Domain Layer - Clean Architecture
library;

import 'package:dartz/dartz.dart';

import '../../core/errors/failures.dart';
import '../../core/usecases/usecase.dart';
import '../repositories/sync_repository.dart';

/// Caso de uso para verificar conectividad
class CheckConnectivityUseCase implements UseCase<bool, NoParams> {
  final SyncRepository repository;

  CheckConnectivityUseCase(this.repository);

  /// Verifica si hay conectividad con el backend
  ///
  /// Llamada lightweight para verificar conexión.
  /// Timeout corto (2-3 segundos) para detección rápida.
  ///
  /// Retorna:
  /// - [Right(true)]: Conectividad OK
  /// - [Right(false)]: Sin conexión (no es error, es estado normal offline)
  /// - [Left(Failure)]: Error inesperado
  @override
  Future<Either<Failure, bool>> call(NoParams params) async {
    return await repository.checkConnectivity();
  }
}

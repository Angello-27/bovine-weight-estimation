/// UseCase: GetPendingCountUseCase
///
/// US-005: Sincronización Offline
///
/// Caso de uso que obtiene el conteo de items pendientes de sincronización.
/// Usado para mostrar badge en UI: "X items pendientes".
///
/// Domain Layer - Clean Architecture
library;

import 'package:dartz/dartz.dart';

import '../../core/errors/failures.dart';
import '../../core/usecases/usecase.dart';
import '../repositories/sync_repository.dart';

/// Caso de uso para obtener conteo de items pendientes
class GetPendingCountUseCase implements UseCase<int, NoParams> {
  final SyncRepository repository;

  GetPendingCountUseCase(this.repository);

  /// Obtiene el conteo de items pendientes en la cola
  ///
  /// Retorna:
  /// - [Right(int)]: Cantidad de items pendientes
  /// - [Left(Failure)]: Error al contar items
  @override
  Future<Either<Failure, int>> call(NoParams params) async {
    return await repository.getPendingCount();
  }
}

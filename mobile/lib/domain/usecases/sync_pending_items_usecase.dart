/// UseCase: SyncPendingItemsUseCase
///
/// US-005: Sincronización Offline
///
/// Caso de uso que sincroniza todos los items pendientes en la cola
/// con estrategia last-write-wins y backoff exponencial.
///
/// Domain Layer - Clean Architecture
library;

import 'package:dartz/dartz.dart';

import '../../core/errors/failures.dart';
import '../../core/usecases/usecase.dart';
import '../entities/sync_result.dart';
import '../repositories/sync_repository.dart';

/// Caso de uso para sincronización automática de items pendientes
class SyncPendingItemsUseCase implements UseCase<SyncResult, NoParams> {
  final SyncRepository repository;

  SyncPendingItemsUseCase(this.repository);

  /// Ejecuta la sincronización de items pendientes
  ///
  /// Proceso:
  /// 1. Verificar conectividad con backend
  /// 2. Obtener items pendientes ordenados por prioridad
  /// 3. Sincronizar en batches de hasta 100 items
  /// 4. Aplicar last-write-wins basado en timestamps UTC
  /// 5. Reintentar items con error según backoff exponencial
  ///
  /// Retorna:
  /// - [Right(SyncResult)]: Resultado con métricas de sincronización
  /// - [Left(Failure)]: Error durante sincronización
  @override
  Future<Either<Failure, SyncResult>> call(NoParams params) async {
    // 1. Verificar conectividad primero
    final connectivityResult = await repository.checkConnectivity();

    final isConnected = connectivityResult.fold(
      (failure) => false,
      (connected) => connected,
    );

    if (!isConnected) {
      return Left(
        NetworkFailure(
          message:
              'Sin conexión a internet. La sincronización se ejecutará '
              'automáticamente cuando se detecte conexión.',
        ),
      );
    }

    // 2. Sincronizar items pendientes
    return await repository.syncPendingItems();
  }
}

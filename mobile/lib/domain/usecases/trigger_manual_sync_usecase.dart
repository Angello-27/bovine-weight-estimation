/// UseCase: TriggerManualSyncUseCase
///
/// US-005: Sincronización Offline
///
/// Caso de uso para forzar una sincronización manual inmediata.
/// Usado cuando el usuario presiona el botón "Sincronizar ahora".
///
/// Domain Layer - Clean Architecture
library;

import 'package:dartz/dartz.dart';

import '../../core/errors/failures.dart';
import '../../core/usecases/usecase.dart';
import '../entities/sync_result.dart';
import '../repositories/sync_repository.dart';

/// Caso de uso para sincronización manual forzada
class TriggerManualSyncUseCase implements UseCase<SyncResult, NoParams> {
  final SyncRepository repository;

  TriggerManualSyncUseCase(this.repository);

  /// Fuerza una sincronización manual inmediata
  ///
  /// Proceso:
  /// 1. Verificar conectividad
  /// 2. Si offline → retornar error claro
  /// 3. Si online → sincronizar inmediatamente con alta prioridad
  ///
  /// Retorna:
  /// - [Right(SyncResult)]: Resultado de sincronización
  /// - [Left(Failure)]: Error (típicamente NetworkFailure si offline)
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
              'No hay conexión a internet. '
              'Verifica tu conectividad WiFi/3G/4G e intenta nuevamente.',
        ),
      );
    }

    // 2. Trigger manual sync con alta prioridad
    return await repository.triggerManualSync();
  }
}

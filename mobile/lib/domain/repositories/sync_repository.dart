/// Repository Interface: SyncRepository
///
/// Contrato para operaciones de sincronización offline-first.
/// Single Responsibility: Definir operaciones de sync bidireccional.
///
/// Domain Layer - Clean Architecture
library;

import 'package:dartz/dartz.dart';

import '../../core/errors/failures.dart';
import '../entities/sync_queue_item.dart';
import '../entities/sync_result.dart';
import '../entities/sync_status.dart';

/// Repositorio para sincronización offline-first
abstract class SyncRepository {
  /// Sincroniza todos los items pendientes en la cola
  ///
  /// Estrategia US-005:
  /// - Batch sync de hasta 100 items simultáneos
  /// - Last-write-wins basado en timestamps UTC
  /// - Reintentos automáticos con backoff exponencial
  ///
  /// Retorna:
  /// - [Right(SyncResult)]: Resultado con métricas de sincronización
  /// - [Left(Failure)]: Error durante sincronización (red, servidor, etc.)
  Future<Either<Failure, SyncResult>> syncPendingItems();

  /// Obtiene todos los items pendientes en la cola
  ///
  /// Retorna:
  /// - [Right(List<SyncQueueItem>)]: Lista de items pendientes
  /// - [Left(Failure)]: Error al obtener items
  Future<Either<Failure, List<SyncQueueItem>>> getPendingItems();

  /// Obtiene el conteo de items pendientes
  ///
  /// Retorna:
  /// - [Right(int)]: Cantidad de items pendientes
  /// - [Left(Failure)]: Error al contar items
  Future<Either<Failure, int>> getPendingCount();

  /// Agrega un item a la cola de sincronización
  ///
  /// Parámetros:
  /// - [item]: Item a agregar a la cola
  ///
  /// Retorna:
  /// - [Right(void)]: Item agregado exitosamente
  /// - [Left(Failure)]: Error al agregar item
  Future<Either<Failure, void>> enqueueItem(SyncQueueItem item);

  /// Actualiza el estado de un item en la cola
  ///
  /// Parámetros:
  /// - [itemId]: ID del item
  /// - [status]: Nuevo estado
  /// - [errorMessage]: Mensaje de error (opcional)
  ///
  /// Retorna:
  /// - [Right(void)]: Estado actualizado
  /// - [Left(Failure)]: Error al actualizar
  Future<Either<Failure, void>> updateItemStatus(
    String itemId,
    SyncStatus status, {
    String? errorMessage,
  });

  /// Verifica la conectividad con el backend
  ///
  /// Retorna:
  /// - [Right(bool)]: true si hay conectividad, false si offline
  /// - [Left(Failure)]: Error al verificar conectividad
  Future<Either<Failure, bool>> checkConnectivity();

  /// Fuerza una sincronización manual inmediata
  ///
  /// Mismo que [syncPendingItems] pero con prioridad alta.
  /// Usado cuando el usuario presiona "Sincronizar ahora".
  ///
  /// Retorna:
  /// - [Right(SyncResult)]: Resultado de sincronización
  /// - [Left(Failure)]: Error durante sincronización
  Future<Either<Failure, SyncResult>> triggerManualSync();

  /// Limpia items antiguos con demasiados reintentos
  ///
  /// Parámetros:
  /// - [maxRetryCount]: Límite de reintentos (default: 10)
  ///
  /// Retorna:
  /// - [Right(int)]: Cantidad de items eliminados
  /// - [Left(Failure)]: Error al limpiar
  Future<Either<Failure, int>> cleanupStaleItems({int maxRetryCount = 10});

  /// Obtiene el último resultado de sincronización
  ///
  /// Útil para mostrar en UI el estado de la última sync.
  ///
  /// Retorna:
  /// - [Right(SyncResult?)]: Último resultado o null si nunca se sincronizó
  /// - [Left(Failure)]: Error al obtener resultado
  Future<Either<Failure, SyncResult?>> getLastSyncResult();

  /// Inicia el listener de sincronización automática
  ///
  /// Detecta cambios en conectividad y sincroniza automáticamente.
  /// Solo debe llamarse una vez al iniciar la app.
  ///
  /// Retorna:
  /// - [Right(void)]: Listener iniciado
  /// - [Left(Failure)]: Error al iniciar listener
  Future<Either<Failure, void>> startAutoSyncListener();

  /// Detiene el listener de sincronización automática
  ///
  /// Retorna:
  /// - [Right(void)]: Listener detenido
  /// - [Left(Failure)]: Error al detener listener
  Future<Either<Failure, void>> stopAutoSyncListener();
}

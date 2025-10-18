/// Repository Implementation: SyncRepositoryImpl
///
/// Implementa sincronización offline-first con estrategia last-write-wins.
/// Coordina entre SyncQueueLocal, CattleLocal, WeightEstimationLocal y Remote.
///
/// Data Layer - Clean Architecture
library;

import 'dart:async';
import 'dart:convert';

import 'package:dartz/dartz.dart';

import '../../core/errors/exceptions.dart';
import '../../core/errors/failures.dart';
import '../../domain/entities/sync_queue_item.dart';
import '../../domain/entities/sync_result.dart';
import '../../domain/entities/sync_status.dart';
import '../../domain/repositories/sync_repository.dart';
import '../datasources/cattle_local_datasource.dart';
import '../datasources/sync_queue_local_datasource.dart';
import '../datasources/sync_remote_datasource.dart';
import '../datasources/weight_estimation_local_datasource.dart';
import '../models/sync_batch_request_model.dart';

/// Implementación de SyncRepository con offline-first
class SyncRepositoryImpl implements SyncRepository {
  final SyncQueueLocalDataSource syncQueueLocal;
  final CattleLocalDataSource cattleLocal;
  final WeightEstimationLocalDataSource weightEstimationLocal;
  final SyncRemoteDataSource syncRemote;

  /// Último resultado de sincronización (en memoria)
  SyncResult? _lastSyncResult;

  /// Listener de sincronización automática
  Timer? _autoSyncTimer;

  /// Device ID (generado al instalar la app)
  final String deviceId;

  SyncRepositoryImpl({
    required this.syncQueueLocal,
    required this.cattleLocal,
    required this.weightEstimationLocal,
    required this.syncRemote,
    required this.deviceId,
  });

  @override
  Future<Either<Failure, SyncResult>> syncPendingItems() async {
    final startTime = DateTime.now();

    try {
      // 1. Obtener items pendientes y listos para reintento
      final pendingItems = await syncQueueLocal.getPendingItems();
      final retryItems = await syncQueueLocal.getItemsReadyForRetry();

      final allItems = [...pendingItems, ...retryItems];

      if (allItems.isEmpty) {
        final result = SyncResult.empty(
          startedAt: startTime,
          completedAt: DateTime.now(),
        );
        _lastSyncResult = result;
        return Right(result);
      }

      // 2. Agrupar por tipo de entidad
      final cattleItems = allItems
          .where((item) => item.entityType == SyncEntityType.cattle)
          .toList();

      final weightEstimationItems = allItems
          .where((item) => item.entityType == SyncEntityType.weightEstimation)
          .toList();

      int syncedCount = 0;
      int failedCount = 0;
      int conflictCount = 0;
      final List<SyncQueueItem> failedItemsList = [];
      final List<SyncQueueItem> conflictItemsList = [];
      final List<String> errors = [];

      // 3. Sincronizar ganado (batches de 100)
      if (cattleItems.isNotEmpty) {
        final cattleResult = await _syncCattleBatch(cattleItems);
        cattleResult.fold(
          (failure) {
            failedCount += cattleItems.length;
            errors.add('Error sincronizando ganado: ${failure.message}');
            failedItemsList.addAll(cattleItems);
          },
          (response) {
            syncedCount += response.syncedCount;
            failedCount += response.failedCount;
            conflictCount += response.conflictCount;

            // Actualizar estado en cola según respuesta
            _updateQueueFromResponse(response, cattleItems);
          },
        );
      }

      // 4. Sincronizar estimaciones (batches de 100)
      if (weightEstimationItems.isNotEmpty) {
        final estimationResult = await _syncWeightEstimationsBatch(
          weightEstimationItems,
        );
        estimationResult.fold(
          (failure) {
            failedCount += weightEstimationItems.length;
            errors.add('Error sincronizando estimaciones: ${failure.message}');
            failedItemsList.addAll(weightEstimationItems);
          },
          (response) {
            syncedCount += response.syncedCount;
            failedCount += response.failedCount;
            conflictCount += response.conflictCount;

            _updateQueueFromResponse(response, weightEstimationItems);
          },
        );
      }

      // 5. Generar resultado
      final endTime = DateTime.now();
      final duration = endTime.difference(startTime);

      final result = SyncResult(
        success: failedCount == 0 && conflictCount == 0,
        totalItems: allItems.length,
        syncedCount: syncedCount,
        failedCount: failedCount,
        conflictCount: conflictCount,
        duration: duration,
        startedAt: startTime,
        completedAt: endTime,
        failedItems: failedItemsList,
        conflictItems: conflictItemsList,
        errors: errors,
        message: _generateSyncMessage(
          syncedCount,
          failedCount,
          conflictCount,
          allItems.length,
        ),
      );

      _lastSyncResult = result;
      return Right(result);
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message));
    } on ServerException catch (e) {
      return Left(ServerFailure(message: e.message));
    } on TimeoutException catch (e) {
      return Left(TimeoutFailure(message: e.message));
    } catch (e) {
      return Left(UnexpectedFailure(message: 'Error inesperado: $e'));
    }
  }

  @override
  Future<Either<Failure, List<SyncQueueItem>>> getPendingItems() async {
    try {
      final items = await syncQueueLocal.getPendingItems();
      return Right(items);
    } on DatabaseException catch (e) {
      return Left(DatabaseFailure(message: e.message));
    } catch (e) {
      return Left(UnexpectedFailure(message: 'Error: $e'));
    }
  }

  @override
  Future<Either<Failure, int>> getPendingCount() async {
    try {
      final count = await syncQueueLocal.getPendingCount();
      return Right(count);
    } on DatabaseException catch (e) {
      return Left(DatabaseFailure(message: e.message));
    } catch (e) {
      return Left(UnexpectedFailure(message: 'Error: $e'));
    }
  }

  @override
  Future<Either<Failure, void>> enqueueItem(SyncQueueItem item) async {
    try {
      await syncQueueLocal.enqueue(item);
      return const Right(null);
    } on DatabaseException catch (e) {
      return Left(DatabaseFailure(message: e.message));
    } catch (e) {
      return Left(UnexpectedFailure(message: 'Error: $e'));
    }
  }

  @override
  Future<Either<Failure, void>> updateItemStatus(
    String itemId,
    SyncStatus status, {
    String? errorMessage,
  }) async {
    try {
      await syncQueueLocal.updateItemStatus(
        itemId,
        status,
        errorMessage: errorMessage,
      );
      return const Right(null);
    } on DatabaseException catch (e) {
      return Left(DatabaseFailure(message: e.message));
    } catch (e) {
      return Left(UnexpectedFailure(message: 'Error: $e'));
    }
  }

  @override
  Future<Either<Failure, bool>> checkConnectivity() async {
    try {
      final response = await syncRemote.healthCheck();
      return Right(response.isOnline);
    } on NetworkException {
      // No es un error, simplemente offline
      return const Right(false);
    } on TimeoutException {
      return const Right(false);
    } catch (e) {
      return const Right(false);
    }
  }

  @override
  Future<Either<Failure, SyncResult>> triggerManualSync() async {
    // Mismo que syncPendingItems pero con alta prioridad
    return await syncPendingItems();
  }

  @override
  Future<Either<Failure, int>> cleanupStaleItems({
    int maxRetryCount = 10,
  }) async {
    try {
      final removedCount = await syncQueueLocal.cleanupStaleItems(
        maxRetryCount: maxRetryCount,
      );
      return Right(removedCount);
    } on DatabaseException catch (e) {
      return Left(DatabaseFailure(message: e.message));
    } catch (e) {
      return Left(UnexpectedFailure(message: 'Error: $e'));
    }
  }

  @override
  Future<Either<Failure, SyncResult?>> getLastSyncResult() async {
    return Right(_lastSyncResult);
  }

  @override
  Future<Either<Failure, void>> startAutoSyncListener() async {
    try {
      // Iniciar timer que verifica cada 60 segundos si hay items pendientes
      _autoSyncTimer?.cancel();
      _autoSyncTimer = Timer.periodic(
        const Duration(seconds: 60),
        (_) => _autoSyncCheck(),
      );
      return const Right(null);
    } catch (e) {
      return Left(UnexpectedFailure(message: 'Error al iniciar listener: $e'));
    }
  }

  @override
  Future<Either<Failure, void>> stopAutoSyncListener() async {
    try {
      _autoSyncTimer?.cancel();
      _autoSyncTimer = null;
      return const Right(null);
    } catch (e) {
      return Left(UnexpectedFailure(message: 'Error al detener listener: $e'));
    }
  }

  // ===== Métodos privados auxiliares =====

  /// Sincroniza batch de ganado
  Future<Either<Failure, SyncBatchResponseModel>> _syncCattleBatch(
    List<SyncQueueItem> items,
  ) async {
    try {
      // Convertir SyncQueueItems a CattleSyncItems
      final cattleItems = <CattleSyncItemModel>[];

      for (final item in items) {
        final cattleData = jsonDecode(item.data);
        cattleItems.add(
          CattleSyncItemModel(
            id: cattleData['id'],
            earTag: cattleData['ear_tag'],
            name: cattleData['name'],
            breed: cattleData['breed'],
            birthDate: DateTime.parse(cattleData['birth_date']),
            gender: cattleData['gender'],
            color: cattleData['color'],
            birthWeight: cattleData['birth_weight']?.toDouble(),
            motherId: cattleData['mother_id'],
            fatherId: cattleData['father_id'],
            observations: cattleData['observations'],
            status: cattleData['status'] ?? 'active',
            registrationDate: DateTime.parse(cattleData['registration_date']),
            lastUpdated: DateTime.parse(cattleData['last_updated']),
            photoPath: cattleData['photo_path'],
            operation: item.operation.name,
          ),
        );
      }

      final request = CattleSyncBatchRequestModel(
        items: cattleItems,
        deviceId: deviceId,
        syncTimestamp: DateTime.now().toUtc(),
      );

      final response = await syncRemote.syncCattleBatch(request);
      return Right(response);
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message));
    } on ServerException catch (e) {
      return Left(ServerFailure(message: e.message));
    } catch (e) {
      return Left(UnexpectedFailure(message: 'Error: $e'));
    }
  }

  /// Sincroniza batch de estimaciones
  Future<Either<Failure, SyncBatchResponseModel>> _syncWeightEstimationsBatch(
    List<SyncQueueItem> items,
  ) async {
    try {
      final estimationItems = <WeightEstimationSyncItemModel>[];

      for (final item in items) {
        final estData = jsonDecode(item.data);
        estimationItems.add(
          WeightEstimationSyncItemModel(
            id: estData['id'],
            cattleId: estData['cattle_id'],
            breed: estData['breed'],
            estimatedWeight: estData['estimated_weight'].toDouble(),
            confidenceScore: estData['confidence_score'].toDouble(),
            frameImagePath: estData['frame_image_path'],
            timestamp: DateTime.parse(estData['timestamp']),
            gpsLatitude: estData['gps_latitude']?.toDouble(),
            gpsLongitude: estData['gps_longitude']?.toDouble(),
            method: estData['method'] ?? 'tflite',
            modelVersion: estData['model_version'] ?? '1.0.0',
            processingTimeMs: estData['processing_time_ms'],
            operation: item.operation.name,
          ),
        );
      }

      final request = WeightEstimationSyncBatchRequestModel(
        items: estimationItems,
        deviceId: deviceId,
        syncTimestamp: DateTime.now().toUtc(),
      );

      final response = await syncRemote.syncWeightEstimationsBatch(request);
      return Right(response);
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message));
    } on ServerException catch (e) {
      return Left(ServerFailure(message: e.message));
    } catch (e) {
      return Left(UnexpectedFailure(message: 'Error: $e'));
    }
  }

  /// Actualiza estado en cola según respuesta del servidor
  Future<void> _updateQueueFromResponse(
    SyncBatchResponseModel response,
    List<SyncQueueItem> items,
  ) async {
    for (final resultItem in response.results) {
      final queueItem = items.firstWhere(
        (item) => item.entityId == resultItem.id,
        orElse: () => items.first,
      );

      final status = SyncStatus.fromString(resultItem.status);

      if (status == SyncStatus.synced) {
        // Remover de cola y marcar entidad como sincronizada
        await syncQueueLocal.removeItem(queueItem.id);

        if (queueItem.entityType == SyncEntityType.cattle) {
          await cattleLocal.markAsSynced(queueItem.entityId);
        } else if (queueItem.entityType == SyncEntityType.weightEstimation) {
          await weightEstimationLocal.markAsSynced(queueItem.entityId);
        }
      } else if (status == SyncStatus.error) {
        // Incrementar reintentos
        await syncQueueLocal.incrementRetryCount(queueItem.id);
        await syncQueueLocal.updateItemStatus(
          queueItem.id,
          SyncStatus.error,
          errorMessage: resultItem.message,
        );

        // Marcar entidad con error
        if (queueItem.entityType == SyncEntityType.cattle) {
          await cattleLocal.markAsSyncError(
            queueItem.entityId,
            resultItem.message ?? 'Error desconocido',
          );
        } else if (queueItem.entityType == SyncEntityType.weightEstimation) {
          await weightEstimationLocal.markAsSyncError(
            queueItem.entityId,
            resultItem.message ?? 'Error desconocido',
          );
        }
      } else if (status == SyncStatus.conflict) {
        // Resolver conflicto aplicando last-write-wins (backend prevalece)
        await syncQueueLocal.updateItemStatus(
          queueItem.id,
          SyncStatus.conflict,
          errorMessage: 'Conflicto: backend tiene versión más reciente',
        );
      }
    }
  }

  /// Verifica automáticamente si hay items pendientes y sincroniza
  Future<void> _autoSyncCheck() async {
    final pendingCountResult = await getPendingCount();
    final pendingCount = pendingCountResult.fold((_) => 0, (count) => count);

    if (pendingCount > 0) {
      // Hay items pendientes, intentar sincronizar
      await syncPendingItems();
    }
  }

  /// Genera mensaje de resumen
  String _generateSyncMessage(
    int synced,
    int failed,
    int conflicts,
    int total,
  ) {
    if (failed == 0 && conflicts == 0) {
      return '✓ $synced de $total items sincronizados exitosamente';
    } else if (failed > 0 && conflicts == 0) {
      return '⚠ $synced sincronizados, $failed errores de $total items';
    } else if (conflicts > 0) {
      return '⚠ $synced sincronizados, $conflicts conflictos, $failed errores de $total items';
    } else {
      return 'Sincronización completada: $synced/$total';
    }
  }
}

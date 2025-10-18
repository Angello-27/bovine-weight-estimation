/// Provider: SyncProvider
///
/// US-005: Sincronización Offline
///
/// State management para sincronización offline-first con indicadores visuales.
/// Gestiona estado reactivo: offline/sincronizando/sincronizado.
///
/// Presentation Layer - Clean Architecture
library;

import 'dart:async';

import 'package:flutter/foundation.dart';

import '../../core/usecases/usecase.dart';
import '../../domain/entities/sync_result.dart';
import '../../domain/usecases/check_connectivity_usecase.dart';
import '../../domain/usecases/get_pending_count_usecase.dart';
import '../../domain/usecases/sync_pending_items_usecase.dart';
import '../../domain/usecases/trigger_manual_sync_usecase.dart';

/// Estado global de sincronización
enum GlobalSyncState {
  /// Offline (sin conexión)
  offline,

  /// Online pero sin items pendientes
  idle,

  /// Sincronizando items pendientes
  syncing,

  /// Sincronización exitosa reciente
  synced,

  /// Error durante sincronización
  error,
}

/// Provider de sincronización con ChangeNotifier
class SyncProvider extends ChangeNotifier {
  // UseCases
  final SyncPendingItemsUseCase syncPendingItemsUseCase;
  final GetPendingCountUseCase getPendingCountUseCase;
  final TriggerManualSyncUseCase triggerManualSyncUseCase;
  final CheckConnectivityUseCase checkConnectivityUseCase;

  // Estado
  GlobalSyncState _syncState = GlobalSyncState.idle;
  int _pendingCount = 0;
  SyncResult? _lastSyncResult;
  String? _errorMessage;
  bool _isConnected = false;
  DateTime? _lastSyncTime;

  // Timer para polling de estado
  Timer? _statePollingTimer;

  SyncProvider({
    required this.syncPendingItemsUseCase,
    required this.getPendingCountUseCase,
    required this.triggerManualSyncUseCase,
    required this.checkConnectivityUseCase,
  }) {
    // Iniciar polling de estado cada 5 segundos
    _startStatePolling();

    // Hacer primera verificación inmediatamente
    _updateState();
  }

  // ===== Getters =====

  GlobalSyncState get syncState => _syncState;
  int get pendingCount => _pendingCount;
  SyncResult? get lastSyncResult => _lastSyncResult;
  String? get errorMessage => _errorMessage;
  bool get isConnected => _isConnected;
  DateTime? get lastSyncTime => _lastSyncTime;

  bool get isSyncing => _syncState == GlobalSyncState.syncing;
  bool get isOffline => _syncState == GlobalSyncState.offline;
  bool get hasError => _syncState == GlobalSyncState.error;
  bool get hasPendingItems => _pendingCount > 0;

  /// Color del indicador según estado (para UI)
  String get stateColor {
    switch (_syncState) {
      case GlobalSyncState.offline:
        return 'red';
      case GlobalSyncState.syncing:
        return 'amber';
      case GlobalSyncState.synced:
        return 'green';
      case GlobalSyncState.error:
        return 'orange';
      case GlobalSyncState.idle:
        return _isConnected ? 'green' : 'gray';
    }
  }

  /// Texto del indicador
  String get stateText {
    switch (_syncState) {
      case GlobalSyncState.offline:
        return 'Sin conexión';
      case GlobalSyncState.syncing:
        return 'Sincronizando...';
      case GlobalSyncState.synced:
        return 'Sincronizado';
      case GlobalSyncState.error:
        return 'Error al sincronizar';
      case GlobalSyncState.idle:
        return _pendingCount > 0
            ? '$_pendingCount pendientes'
            : 'Todo sincronizado';
    }
  }

  /// Texto detallado para UI expandida
  String get detailedStatusText {
    if (_lastSyncResult != null) {
      return _lastSyncResult!.message ?? _lastSyncResult!.shortSummary;
    }
    if (_errorMessage != null) {
      return _errorMessage!;
    }
    if (_pendingCount > 0) {
      return '$_pendingCount items esperando sincronización';
    }
    return 'No hay cambios pendientes';
  }

  // ===== Métodos públicos =====

  /// Fuerza una sincronización manual inmediata
  Future<void> triggerManualSync() async {
    if (_syncState == GlobalSyncState.syncing) {
      // Ya hay una sincronización en curso
      return;
    }

    _syncState = GlobalSyncState.syncing;
    _errorMessage = null;
    notifyListeners();

    final result = await triggerManualSyncUseCase(const NoParams());

    result.fold(
      (failure) {
        _syncState = GlobalSyncState.error;
        _errorMessage = failure.message;
        notifyListeners();
      },
      (syncResult) {
        _lastSyncResult = syncResult;
        _lastSyncTime = DateTime.now();

        if (syncResult.isCompleteSuccess) {
          _syncState = GlobalSyncState.synced;
          _pendingCount = 0;
        } else if (syncResult.hasPendingItems) {
          _syncState = GlobalSyncState.error;
          _pendingCount = syncResult.failedCount + syncResult.conflictCount;
          _errorMessage = syncResult.message;
        }

        notifyListeners();

        // Volver a idle después de 3 segundos
        Future.delayed(const Duration(seconds: 3), () {
          if (_syncState == GlobalSyncState.synced) {
            _syncState = GlobalSyncState.idle;
            notifyListeners();
          }
        });
      },
    );
  }

  /// Sincronización automática en background
  Future<void> autoSync() async {
    if (_syncState == GlobalSyncState.syncing) {
      return;
    }

    if (_pendingCount == 0) {
      return;
    }

    if (!_isConnected) {
      return;
    }

    _syncState = GlobalSyncState.syncing;
    notifyListeners();

    final result = await syncPendingItemsUseCase(const NoParams());

    result.fold(
      (failure) {
        // En auto-sync, no mostramos error (solo actualizamos estado)
        _syncState = GlobalSyncState.idle;
        notifyListeners();
      },
      (syncResult) {
        _lastSyncResult = syncResult;
        _lastSyncTime = DateTime.now();

        if (syncResult.isCompleteSuccess) {
          _syncState = GlobalSyncState.synced;
          _pendingCount = 0;

          // Volver a idle rápido en auto-sync
          Future.delayed(const Duration(seconds: 2), () {
            if (_syncState == GlobalSyncState.synced) {
              _syncState = GlobalSyncState.idle;
              notifyListeners();
            }
          });
        } else {
          _syncState = GlobalSyncState.idle;
          _pendingCount = syncResult.failedCount + syncResult.conflictCount;
        }

        notifyListeners();
      },
    );
  }

  /// Actualiza el conteo de items pendientes
  Future<void> refreshPendingCount() async {
    final result = await getPendingCountUseCase(const NoParams());

    result.fold(
      (_) {
        // Ignorar error silenciosamente
      },
      (count) {
        _pendingCount = count;
        notifyListeners();
      },
    );
  }

  /// Verifica conectividad
  Future<void> checkConnectivity() async {
    final result = await checkConnectivityUseCase(const NoParams());

    result.fold(
      (_) {
        _isConnected = false;
      },
      (connected) {
        _isConnected = connected;
      },
    );

    // Actualizar estado según conectividad
    if (!_isConnected && _syncState != GlobalSyncState.syncing) {
      _syncState = GlobalSyncState.offline;
      notifyListeners();
    } else if (_isConnected && _syncState == GlobalSyncState.offline) {
      _syncState = GlobalSyncState.idle;
      notifyListeners();

      // Si hay items pendientes y volvió conectividad → auto-sync
      if (_pendingCount > 0) {
        autoSync();
      }
    }
  }

  // ===== Métodos privados =====

  /// Inicia polling de estado cada 5 segundos
  void _startStatePolling() {
    _statePollingTimer?.cancel();
    _statePollingTimer = Timer.periodic(
      const Duration(seconds: 5),
      (_) => _updateState(),
    );
  }

  /// Actualiza estado completo
  Future<void> _updateState() async {
    await checkConnectivity();
    await refreshPendingCount();

    // Si hay items pendientes y hay conexión → auto-sync
    if (_pendingCount > 0 &&
        _isConnected &&
        _syncState != GlobalSyncState.syncing) {
      await autoSync();
    }
  }

  @override
  void dispose() {
    _statePollingTimer?.cancel();
    super.dispose();
  }
}

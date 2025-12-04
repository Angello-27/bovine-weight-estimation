/// UseCase: HasSessionUseCase
///
/// Verifica si hay una sesión activa.
///
/// Domain Layer - Clean Architecture
library;

import 'package:dartz/dartz.dart';

import '../../core/errors/failures.dart';
import '../../core/usecases/usecase.dart';
import '../repositories/auth_repository.dart';

/// Caso de uso para verificar sesión
class HasSessionUseCase implements UseCase<bool, NoParams> {
  final AuthRepository repository;

  HasSessionUseCase(this.repository);

  @override
  Future<Either<Failure, bool>> call(NoParams params) async {
    return await repository.hasSession();
  }
}

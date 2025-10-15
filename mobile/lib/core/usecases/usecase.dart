/// Base UseCase Interface
/// 
/// Interfaz genérica para todos los casos de uso del sistema.
/// Siguiendo Clean Architecture, todos los UseCases deben implementar esta interfaz.
///
/// Core Layer - Clean Architecture
library;

import 'package:dartz/dartz.dart';

import '../errors/failures.dart';

/// Interfaz base para todos los casos de uso
/// 
/// Type: Tipo de retorno esperado del caso de uso
/// Params: Parámetros de entrada del caso de uso
abstract class UseCase<Type, Params> {
  /// Ejecuta el caso de uso
  /// 
  /// Retorna:
  /// - [Right(Type)]: Resultado exitoso del tipo especificado
  /// - [Left(Failure)]: Fallo durante la ejecución
  Future<Either<Failure, Type>> call(Params params);
}

/// Clase para casos de uso sin parámetros
class NoParams {
  const NoParams();
}


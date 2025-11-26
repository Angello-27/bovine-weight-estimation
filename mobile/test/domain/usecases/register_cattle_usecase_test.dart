/// Unit Test: RegisterCattleUseCase
///
/// Tests unitarios para el caso de uso de registro de ganado.
/// Validación de reglas de negocio.
///
/// Testing Layer
library;

import 'package:bovine_weight_mobile/core/constants/breeds.dart';
import 'package:bovine_weight_mobile/core/errors/failures.dart';
import 'package:bovine_weight_mobile/domain/entities/cattle.dart';
import 'package:bovine_weight_mobile/domain/repositories/cattle_repository.dart';
import 'package:bovine_weight_mobile/domain/usecases/register_cattle_usecase.dart';
import 'package:dartz/dartz.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';

@GenerateMocks([CattleRepository])
import 'register_cattle_usecase_test.mocks.dart';

void main() {
  late RegisterCattleUseCase useCase;
  late MockCattleRepository mockRepository;

  setUp(() {
    mockRepository = MockCattleRepository();
    useCase = RegisterCattleUseCase(mockRepository);
  });

  group('RegisterCattleUseCase', () {
    final tParams = RegisterCattleParams(
      earTag: 'A-001',
      name: 'Brownie',
      breed: BreedType.brahman,
      birthDate: DateTime(2023, 1, 15),
      gender: Gender.female,
    );

    final tCattle = Cattle(
      id: '1',
      earTag: 'A-001',
      name: 'Brownie',
      breed: BreedType.brahman,
      birthDate: DateTime(2023, 1, 15),
      gender: Gender.female,
      status: CattleStatus.active,
      registrationDate: DateTime.now(),
      lastUpdated: DateTime.now(),
    );

    test('debe registrar ganado exitosamente', () async {
      // Arrange
      when(
        mockRepository.earTagExists(any),
      ).thenAnswer((_) async => const Right(false));
      when(
        mockRepository.registerCattle(any),
      ).thenAnswer((_) async => Right(tCattle));

      // Act
      final result = await useCase.call(tParams);

      // Assert
      expect(result.isRight(), true);
      verify(mockRepository.earTagExists('A-001')).called(1);
      verify(mockRepository.registerCattle(any)).called(1);
    });

    test('debe retornar ValidationFailure si caravana ya existe', () async {
      // Arrange
      when(mockRepository.earTagExists(any)).thenAnswer(
        (_) async => const Right(true), // Ya existe
      );

      // Act
      final result = await useCase.call(tParams);

      // Assert
      expect(result.isLeft(), true);
      result.fold((failure) {
        expect(failure, isA<ValidationFailure>());
        expect(failure.message, contains('caravana ya existe'));
      }, (_) => fail('Should return failure'));
    });

    test('debe retornar ValidationFailure si caravana está vacía', () async {
      // Arrange
      final invalidParams = RegisterCattleParams(
        earTag: '',
        breed: BreedType.senepol,
        birthDate: DateTime(2023, 1, 1),
        gender: Gender.male,
      );

      // Act
      final result = await useCase.call(invalidParams);

      // Assert
      expect(result.isLeft(), true);
      result.fold((failure) {
        expect(failure, isA<ValidationFailure>());
        expect(failure.message, contains('obligatoria'));
      }, (_) => fail('Should return failure'));
    });

    test('debe retornar ValidationFailure si fecha es futura', () async {
      // Arrange
      final invalidParams = RegisterCattleParams(
        earTag: 'A-002',
        breed: BreedType.nelore,
        birthDate: DateTime.now().add(const Duration(days: 1)), // Futura
        gender: Gender.female,
      );

      // Act
      final result = await useCase.call(invalidParams);

      // Assert
      expect(result.isLeft(), true);
      result.fold((failure) {
        expect(failure, isA<ValidationFailure>());
        expect(failure.message, contains('futura'));
      }, (_) => fail('Should return failure'));
    });

    test(
      'debe retornar ValidationFailure si peso al nacer es inválido',
      () async {
        // Arrange
        final invalidParams = RegisterCattleParams(
          earTag: 'A-003',
          breed: BreedType.girolando,
          birthDate: DateTime(2023, 1, 1),
          gender: Gender.male,
          birthWeight: 5.0, // Muy bajo (debe ser 10-100 kg)
        );

        // Act
        final result = await useCase.call(invalidParams);

        // Assert
        expect(result.isLeft(), true);
        result.fold((failure) {
          expect(failure, isA<ValidationFailure>());
          expect(failure.message, contains('10-100'));
        }, (_) => fail('Should return failure'));
      },
    );
  });
}

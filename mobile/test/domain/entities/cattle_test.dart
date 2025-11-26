/// Unit Test: Cattle Entity
///
/// Tests unitarios para la entidad Cattle.
/// Validación de lógica de negocio (edad, categoría, etc.)
///
/// Testing Layer
library;

import 'package:bovine_weight_mobile/core/constants/age_categories.dart';
import 'package:bovine_weight_mobile/core/constants/breeds.dart';
import 'package:bovine_weight_mobile/domain/entities/cattle.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('Cattle Entity', () {
    final now = DateTime.now();

    final testCattle = Cattle(
      id: '1',
      earTag: 'A-001',
      name: 'Brownie',
      breed: BreedType.brahman,
      birthDate: DateTime(2022, 1, 15),
      gender: Gender.female,
      status: CattleStatus.active,
      registrationDate: now,
      lastUpdated: now,
    );

    test('debe calcular edad en meses correctamente', () {
      final ageInMonths = testCattle.ageInMonths;

      // Verificar que la edad sea razonable (>24 meses para 2022)
      expect(ageInMonths, greaterThan(24));
    });

    test('debe calcular categoría de edad correctamente', () {
      // Ternero (<8 meses)
      final ternero = Cattle(
        id: '2',
        earTag: 'T-001',
        breed: BreedType.senepol,
        birthDate: DateTime.now().subtract(
          const Duration(days: 180),
        ), // ~6 meses
        gender: Gender.male,
        registrationDate: now,
        lastUpdated: now,
      );

      expect(ternero.ageCategory, AgeCategory.terneros);

      // Vaca (>30 meses)
      final vaca = Cattle(
        id: '3',
        earTag: 'V-001',
        breed: BreedType.nelore,
        birthDate: DateTime.now().subtract(
          const Duration(days: 1000),
        ), // ~33 meses
        gender: Gender.female,
        registrationDate: now,
        lastUpdated: now,
      );

      expect(vaca.ageCategory, AgeCategory.vacasToros);
    });

    test('debe retornar displayName correcto', () {
      expect(testCattle.displayName, 'A-001 - Brownie');

      final sinNombre = Cattle(
        id: '4',
        earTag: 'A-002',
        breed: BreedType.guzerat,
        birthDate: DateTime(2023, 1, 1),
        gender: Gender.male,
        registrationDate: now,
        lastUpdated: now,
      );

      expect(sinNombre.displayName, 'A-002');
    });

    test('debe identificar si está activo', () {
      expect(testCattle.isActive, true);

      final inactivo = testCattle.copyWith(status: CattleStatus.sold);
      expect(inactivo.isActive, false);
    });

    test('copyWith debe funcionar correctamente', () {
      final updated = testCattle.copyWith(
        name: 'New Name',
        status: CattleStatus.inactive,
      );

      expect(updated.name, 'New Name');
      expect(updated.status, CattleStatus.inactive);
      expect(updated.earTag, 'A-001'); // No cambiado
    });
  });

  group('Gender Enum', () {
    test('debe retornar displayName correcto', () {
      expect(Gender.male.displayName, 'Macho');
      expect(Gender.female.displayName, 'Hembra');
    });

    test('debe convertir desde value correctamente', () {
      expect(GenderExtension.fromValue('male'), Gender.male);
      expect(GenderExtension.fromValue('female'), Gender.female);
    });
  });

  group('CattleStatus Enum', () {
    test('debe retornar displayName correcto', () {
      expect(CattleStatus.active.displayName, 'Activo');
      expect(CattleStatus.sold.displayName, 'Vendido');
    });

    test('debe retornar color hex correcto', () {
      expect(CattleStatus.active.colorHex, '#4CAF50'); // Verde
      expect(CattleStatus.inactive.colorHex, '#9E9E9E'); // Gris
      expect(CattleStatus.sold.colorHex, '#2196F3'); // Azul
      expect(CattleStatus.deceased.colorHex, '#D32F2F'); // Rojo
    });
  });
}

/// Constantes de Razas Bovinas - Hacienda Gamelera
/// 7 razas tropicales priorizadas (alineadas con modelo ML entrenado en Colab)
/// NO MODIFICAR sin autorización de Bruno Brito Macedo
library;

/// Enum de razas bovinas disponibles
enum BreedType {
  nelore('nelore', 'Nelore', BovineSpecies.bosIndicus),
  brahman('brahman', 'Brahman', BovineSpecies.bosIndicus),
  guzerat('guzerat', 'Guzerat', BovineSpecies.bosIndicus),
  senepol('senepol', 'Senepol', BovineSpecies.bosTaurus),
  girolando('girolando', 'Girolando', BovineSpecies.bosTaurus),
  gyrLechero('gyr_lechero', 'Gyr Lechero', BovineSpecies.bosIndicus),
  sindi('sindi', 'Sindi', BovineSpecies.bosIndicus);

  const BreedType(this.value, this.displayName, this.species);

  /// Valor para almacenamiento/API
  final String value;

  /// Nombre para mostrar en UI
  final String displayName;

  /// Especie bovina (Bos indicus o Bos taurus)
  final BovineSpecies species;

  /// Retorna el nombre del archivo del modelo TFLite
  String get modelFilename => '$value-v1.0.0.tflite';

  /// Retorna el path del asset de imagen de la raza
  String get imageAssetPath => 'assets/$value.jpg';

  /// Valida si un string es una raza válida
  static bool isValid(String breed) {
    try {
      fromValue(breed);
      return true;
    } catch (_) {
      return false;
    }
  }

  /// Obtiene BreedType desde string value
  static BreedType fromValue(String value) {
    return BreedType.values.firstWhere(
      (breed) => breed.value == value,
      orElse: () => throw ArgumentError('Raza inválida: $value'),
    );
  }
}

/// Clasificación taxonómica de bovinos
enum BovineSpecies {
  bosIndicus('bos_indicus', 'Bos indicus'),
  bosTaurus('bos_taurus', 'Bos taurus');

  const BovineSpecies(this.value, this.displayName);

  final String value;
  final String displayName;
}

/// Lista de todas las razas para uso en dropdowns
const List<BreedType> allBreeds = BreedType.values;

/// Razas Bos indicus (cebuinas/tropicales)
const List<BreedType> bosIndicusBreeds = [
  BreedType.nelore,
  BreedType.brahman,
  BreedType.guzerat,
  BreedType.gyrLechero,
  BreedType.sindi,
];

/// Razas Bos taurus (europeas/adaptadas)
const List<BreedType> bosTaurusBreeds = [
  BreedType.senepol,
  BreedType.girolando,
];

/// Razas de carne (prioritarias en Santa Cruz)
const List<BreedType> meatBreeds = [
  BreedType.nelore,
  BreedType.brahman,
  BreedType.senepol,
];

/// Razas lecheras (tropicales)
const List<BreedType> dairyBreeds = [
  BreedType.girolando,
  BreedType.gyrLechero,
  BreedType.sindi,
];

/// Razas doble propósito
const List<BreedType> dualPurposeBreeds = [BreedType.guzerat];

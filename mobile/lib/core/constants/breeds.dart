/// Constantes de Razas Bovinas - Hacienda Gamelera
/// 7 razas exactas (NO MODIFICAR sin autorización de Bruno Brito Macedo)
library;

/// Enum de razas bovinas disponibles
enum BreedType {
  brahman('brahman', 'Brahman', BovineSpecies.bosIndicus),
  nelore('nelore', 'Nelore', BovineSpecies.bosIndicus),
  angus('angus', 'Angus', BovineSpecies.bosTaurus),
  cebuinas('cebuinas', 'Cebuinas (Bos indicus)', BovineSpecies.bosIndicus),
  criollo('criollo', 'Criollo (Bos taurus)', BovineSpecies.bosTaurus),
  pardoSuizo('pardo_suizo', 'Pardo Suizo', BovineSpecies.bosTaurus),
  jersey('jersey', 'Jersey', BovineSpecies.bosTaurus);

  const BreedType(this.value, this.displayName, this.species);

  /// Valor para almacenamiento/API
  final String value;

  /// Nombre para mostrar en UI
  final String displayName;

  /// Especie bovina (Bos indicus o Bos taurus)
  final BovineSpecies species;

  /// Retorna el nombre del archivo del modelo TFLite
  String get modelFilename => '$value-v1.0.0.tflite';

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

/// Razas Bos indicus (cebuinas)
const List<BreedType> bosIndicusBreeds = [
  BreedType.brahman,
  BreedType.nelore,
  BreedType.cebuinas,
];

/// Razas Bos taurus (europeas)
const List<BreedType> bosTaurusBreeds = [
  BreedType.angus,
  BreedType.criollo,
  BreedType.pardoSuizo,
  BreedType.jersey,
];

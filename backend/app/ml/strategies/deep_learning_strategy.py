"""
Deep Learning Weight Estimation Strategy - Estimación usando modelos ML entrenados
Implementa Strategy Pattern para método de Deep Learning
"""

import numpy as np

from app.domain.shared.constants import BreedType
from app.ml.model_loader import MLModelLoader
from app.ml.preprocessing import ImagePreprocessor

from .base_strategy import BaseWeightEstimationStrategy


class DeepLearningWeightEstimationStrategy(BaseWeightEstimationStrategy):
    """
    Estrategia de Deep Learning usando modelos TFLite entrenados.

    Single Responsibility: Implementar estimación de Deep Learning específica
    Open/Closed: Extensible para diferentes arquitecturas de modelo
    Dependency Inversion: Depende de abstracción (BaseWeightEstimationStrategy)

    Método: Modelos de Deep Learning entrenados con TensorFlow/Keras
    para estimación directa de peso desde imágenes.
    """

    def __init__(self):
        """Inicializa la estrategia de Deep Learning."""
        self.model_loader = MLModelLoader()
        self.preprocessor = ImagePreprocessor()
        self._model = None

    def _ensure_model_loaded(self):
        """Asegura que el modelo TFLite esté cargado."""
        if self._model is None:
            self._model = self.model_loader.load_generic_model()

    def estimate_weight(self, image_bytes: bytes, breed: BreedType) -> dict:
        """
        Estima peso usando modelo TFLite entrenado.

        Args:
            image_bytes: Bytes de imagen (JPEG/PNG)
            breed: Raza del animal (usado para validación, modelo es genérico)

        Returns:
            Dict con peso estimado, confianza, método y metadatos

        Raises:
            ValueError: Si no se puede estimar el peso
        """
        try:
            # 1. Cargar modelo si no está cargado
            self._ensure_model_loaded()

            # 2. Preprocesar imagen
            preprocessed_image = self.preprocessor.preprocess_from_bytes(image_bytes)

            # 3. Ejecutar inferencia TFLite
            interpreter = self._model["interpreter"]
            input_details = self._model["input_details"]
            output_details = self._model["output_details"]

            # Preparar input (ya viene con batch dimension del preprocessor)
            input_data = preprocessed_image.astype(np.float32)

            # Ejecutar inferencia
            interpreter.set_tensor(input_details[0]["index"], input_data)
            interpreter.invoke()

            # Obtener output
            output_data = interpreter.get_tensor(output_details[0]["index"])
            raw_weight = float(output_data[0][0])  # Modelo retorna peso directamente

            # 4. Aplicar corrección post-procesamiento para animales fuera del rango
            estimated_weight = self._apply_weight_correction(raw_weight, breed)

            # 5. Calcular confidence basado en peso corregido y rango típico de la raza
            confidence = self._calculate_confidence(estimated_weight, breed)

            return {
                "weight": round(estimated_weight, 2),
                "confidence": confidence,
                "method": "tflite_model",
                "ml_model_version": self._model["version"],
                "strategy": self.get_strategy_name(),
                "detection_quality": "good" if confidence > 0.85 else "acceptable",
                "weight_corrected": raw_weight
                != estimated_weight,  # Indicar si se aplicó corrección
            }

        except Exception as e:
            # Fallback a mock si hay error (para desarrollo)
            print(f"⚠️ Error en inferencia TFLite: {str(e)}")
            print("   Usando estimación mock como fallback")
            weight_kg, confidence = self._mock_ml_inference(breed, image_bytes)
            return {
                "weight": weight_kg,
                "confidence": confidence,
                "method": "ml_model_mock",
                "ml_model_version": "1.0.0-mock",
                "strategy": self.get_strategy_name(),
                "detection_quality": "acceptable",
            }

    def _mock_ml_inference(
        self, breed: BreedType, image_bytes: bytes
    ) -> tuple[float, float]:
        """
        Inferencia mock para ML (MVP - reemplazar con modelo real).

        Args:
            breed: Raza del animal
            image_bytes: Bytes de imagen

        Returns:
            (peso_estimado_kg, confidence)
        """
        # Rangos típicos por raza (alineados con entrenamiento ML)
        breed_weight_ranges = {
            BreedType.NELORE: (250, 650),
            BreedType.BRAHMAN: (260, 680),
            BreedType.GUZERAT: (240, 650),
            BreedType.SENEPOL: (280, 620),
            BreedType.GIROLANDO: (240, 640),
            BreedType.GYR_LECHERO: (220, 620),
            BreedType.SINDI: (150, 380),
        }

        # Obtener rango de la raza
        weight_min, weight_max = breed_weight_ranges.get(breed, (400, 600))

        # Generar peso pseudo-aleatorio usando bytes de imagen como seed
        pixel_sum = sum(image_bytes[:100])  # Usar primeros 100 bytes
        normalized_seed = (pixel_sum % 1000) / 1000

        estimated_weight = weight_min + (weight_max - weight_min) * normalized_seed

        # Confidence mock (alto para simular modelo bueno)
        base_confidence = 0.93
        confidence_variation = normalized_seed * 0.05
        confidence = min(0.98, base_confidence + confidence_variation)

        return round(estimated_weight, 1), round(confidence, 4)

    def _apply_weight_correction(self, raw_weight: float, breed: BreedType) -> float:
        """
        Aplica corrección post-procesamiento para pesos fuera del rango del modelo.

        El modelo genérico está entrenado para rangos típicos (250-650 kg para Nelore),
        pero hay animales que pueden pesar más (hasta 1000+ kg). Esta función detecta
        cuando el peso está subestimado y aplica una corrección basada en extrapolación.

        Args:
            raw_weight: Peso crudo del modelo ML
            breed: Raza del animal

        Returns:
            Peso corregido (puede ser igual al raw_weight si no necesita corrección)
        """
        # Rangos de entrenamiento del modelo (lo que el modelo "conoce")
        model_training_ranges = {
            BreedType.NELORE: (250, 650),
            BreedType.BRAHMAN: (260, 680),
            BreedType.GUZERAT: (240, 650),
            BreedType.SENEPOL: (280, 620),
            BreedType.GIROLANDO: (240, 640),
            BreedType.GYR_LECHERO: (220, 620),
            BreedType.SINDI: (150, 380),
        }

        # Rangos máximos reales conocidos para cada raza (basados en datos zootécnicos)
        # Estos son los pesos máximos que pueden alcanzar animales adultos bien desarrollados
        # NOTA: Toros reproductores de élite pueden superar estos rangos
        real_max_ranges = {
            BreedType.NELORE: 1150,  # Toros Nelore de élite pueden llegar a 1150+ kg
            BreedType.BRAHMAN: 1100,  # Toros Brahman de élite pueden llegar a 1100+ kg
            BreedType.GUZERAT: 1000,  # Toros Guzerat de élite pueden llegar a 1000+ kg
            BreedType.SENEPOL: 950,  # Toros Senepol de élite pueden llegar a 950+ kg
            BreedType.GIROLANDO: 900,  # Toros Girolando de élite pueden llegar a 900+ kg
            BreedType.GYR_LECHERO: 850,  # Toros Gyr Lechero de élite pueden llegar a 850+ kg
            BreedType.SINDI: 550,  # Toros Sindi de élite pueden llegar a 550+ kg
        }

        weight_min, weight_max = model_training_ranges.get(breed, (300, 700))
        real_max = real_max_ranges.get(breed, 1000)

        # Calcular posición en el rango del modelo
        range_size = weight_max - weight_min
        position_in_range = (
            (raw_weight - weight_min) / range_size if range_size > 0 else 0
        )

        # Estrategia de corrección mejorada:
        # Detecta cuando el peso está subestimado basándose en:
        # 1. Posición en el rango del modelo (animales grandes suelen estar en rango bajo)
        # 2. Distancia al máximo real conocido
        # 3. Factor de corrección proporcional y conservador
        # NOTA: Las hembras tienen rangos típicos más bajos (vacas: 380-520 kg para Nelore)
        # por lo que pesos en el rango bajo pueden ser normales para hembras

        # Rangos típicos para hembras adultas (para evitar sobrecorregir vacas)
        female_ranges = {
            BreedType.NELORE: (380, 520),  # vaca: 380-520 kg
            BreedType.BRAHMAN: (390, 540),  # vaca: 390-540 kg
            BreedType.GUZERAT: (360, 520),  # vaca: 360-520 kg
            BreedType.SENEPOL: (360, 480),  # vaca: 360-480 kg
            BreedType.GIROLANDO: (420, 580),  # vaca: 420-580 kg
            BreedType.GYR_LECHERO: (380, 520),  # vaca: 380-520 kg
            BreedType.SINDI: (260, 380),  # vaca: 260-380 kg
        }

        female_min, female_max = female_ranges.get(breed, (300, 500))

        should_correct = False
        correction_factor = 1.0
        correction_reason = ""

        # Caso 1: Peso muy por debajo del mínimo del modelo (< 90% del mínimo)
        # (animal claramente grande subestimado, posible toro de élite)
        # Solo aplicar si está significativamente por debajo, no solo ligeramente
        if raw_weight < weight_min * 0.9:
            # Factor base: relación entre máximo real y máximo modelo
            base_factor = real_max / weight_max
            # Factor adicional para casos extremos (animales muy subestimados)
            # Si está por debajo del 70% del mínimo, aplicar factor extra más agresivo
            extreme_factor = 1.3 if raw_weight < weight_min * 0.7 else 1.1
            correction_factor = base_factor * extreme_factor
            correction_reason = (
                "peso muy por debajo del mínimo (posible animal excepcional)"
            )
            should_correct = True

        # Caso 2: Peso en el rango muy bajo del modelo (primeros 25% del rango)
        # Solo aplicar corrección agresiva si está en el rango muy bajo
        # PERO: Si el peso está dentro del rango típico de hembras, ser más conservador
        elif position_in_range < 0.25:
            # Verificar si podría ser una hembra
            # Considerar hembra SOLO si está cerca del rango de hembras (no muy por debajo)
            # Si está muy por debajo del mínimo de hembras (< 85%), probablemente es un toro grande subestimado
            # También verificar que no esté extremadamente por debajo del mínimo del modelo
            is_likely_female = (
                female_min * 0.85 <= raw_weight <= female_max * 1.1
            ) and (
                raw_weight >= weight_min * 1.1
            )  # Más estricto: debe estar cerca del rango de hembras Y no muy por debajo del mínimo del modelo

            if is_likely_female:
                # Corrección conservadora para hembras
                # Si está por debajo del mínimo de hembras, aplicar corrección moderada
                if raw_weight < female_min:
                    # Factor para llevar el peso hacia el rango típico de hembras
                    # Objetivo: llevar hacia el mínimo de hembras (female_min)
                    target_weight = female_min
                    # Factor de corrección basado en la distancia al objetivo
                    # Más agresivo cuanto más lejos esté del mínimo de hembras
                    distance_to_target = target_weight - raw_weight
                    max_distance = female_min - weight_min  # Distancia máxima posible
                    if max_distance > 0:
                        correction_ratio = min(distance_to_target / max_distance, 1.0)
                        # Factor de corrección: entre 1.1x y 1.6x dependiendo de la distancia
                        correction_factor = 1.1 + (correction_ratio * 0.5)
                    else:
                        correction_factor = 1.2  # Fallback conservador

                    correction_factor = min(
                        correction_factor, 1.6
                    )  # Máximo 1.6x para hembras
                    correction_reason = f"peso en rango muy bajo, posible hembra ({position_in_range:.1%})"
                    should_correct = True
                # Si está dentro del rango de hembras, no corregir (es normal)
            else:
                # Probablemente un toro grande subestimado, aplicar corrección más agresiva
                base_factor = real_max / weight_max
                position_factor = (
                    1.0 + (0.25 - position_in_range) * 2.0
                )  # Entre 1.0 y 1.5
                correction_factor = base_factor * position_factor
                correction_reason = (
                    f"peso en rango muy bajo, posible toro ({position_in_range:.1%})"
                )
                should_correct = True

        # Caso 3: Peso en el rango bajo-medio (25-40% del rango)
        # Corrección muy conservadora para animales que podrían ser grandes pero no extremos
        # Esto cubre el caso de vacas adultas que están en el rango bajo pero normal
        # Solo aplicar si el peso está claramente por debajo del rango típico de hembras
        elif position_in_range < 0.4:
            # Factor base muy conservador (reducir 30% para evitar sobrecorregir hembras)
            # Solo aplicar corrección moderada
            base_factor = (real_max / weight_max) * 0.7
            position_factor = 1.0 + (0.4 - position_in_range) * 0.3  # Entre 1.0 y 1.045
            correction_factor = base_factor * position_factor
            # Limitar corrección máxima a 1.5x para este caso (muy conservador)
            correction_factor = min(correction_factor, 1.5)
            correction_reason = f"peso en rango bajo-medio ({position_in_range:.1%})"
            should_correct = True

        # Caso 4: Peso en el rango medio-bajo (40-60% del rango)
        # Solo aplicar corrección muy conservadora si el máximo real es significativamente mayor
        # y el peso está en la parte baja de este rango
        elif position_in_range < 0.6 and (real_max / weight_max) > 1.4:
            # Corrección muy conservadora para rangos medios
            base_factor = real_max / weight_max
            position_factor = 1.0 + (0.6 - position_in_range) * 0.2  # Entre 1.0 y 1.04
            correction_factor = base_factor * position_factor * 0.85  # Reducir 15% más
            correction_reason = f"peso en rango medio-bajo ({position_in_range:.1%})"
            should_correct = True

        # Caso 5: Peso en el rango medio (60-80% del rango) pero subestimado para toro de élite
        # Si el peso está por debajo del 75% del máximo del modelo y el máximo real es >1.5x mayor,
        # probablemente es un toro grande subestimado
        elif (
            position_in_range >= 0.6
            and position_in_range < 0.8
            and raw_weight < weight_max * 0.75
            and (real_max / weight_max) > 1.5
        ):
            # Verificar si NO es probablemente una hembra
            is_likely_female = female_min * 0.9 <= raw_weight <= female_max * 1.1

            if not is_likely_female:
                # Probablemente un toro grande subestimado
                # Para toros en rango medio, aplicar corrección más agresiva
                # Objetivo: llevar hacia el rango típico de toros (480-650 para Nelore)
                # pero considerando que toros de élite pueden ser más pesados

                # Calcular factor basado en la distancia al máximo real
                # Si el peso está en 60-80% del rango del modelo pero debería estar cerca del máximo real
                target_weight_elite = (
                    float(real_max) * 0.85
                )  # Objetivo: 85% del máximo real (toro de élite)
                distance_to_target = target_weight_elite - raw_weight
                max_possible_distance = float(real_max) - float(weight_min)

                if max_possible_distance > 0:
                    # Factor progresivo: más corrección cuanto más lejos esté del objetivo
                    correction_ratio = min(
                        distance_to_target / max_possible_distance, 1.0
                    )
                    # Factor base: relación máximo real / máximo modelo
                    base_factor = real_max / weight_max
                    # Factor adicional basado en la distancia (entre 1.0 y 1.3x)
                    distance_factor = 1.0 + (correction_ratio * 0.3)
                    correction_factor = base_factor * distance_factor
                else:
                    # Fallback: usar factor base con ajuste conservador
                    base_factor = real_max / weight_max
                    position_factor = 1.0 + (0.8 - position_in_range) * 0.3
                    correction_factor = base_factor * position_factor * 0.9

                correction_factor = min(
                    correction_factor, 2.8
                )  # Máximo 2.8x para este caso
                correction_reason = f"peso en rango medio, posible toro subestimado ({position_in_range:.1%})"
                should_correct = True

        if should_correct:
            # Limitar el factor de corrección a un máximo razonable (3.5x para casos extremos)
            # Esto permite corregir animales de 1000+ kg estimados en ~300 kg
            # Toros reproductores de élite pueden requerir correcciones más agresivas
            correction_factor = min(correction_factor, 3.5)

            corrected_weight = raw_weight * correction_factor

            # Asegurar que no exceda el máximo real conocido
            # Pero permitir hasta un 10% más para toros excepcionales
            max_allowed = real_max * 1.1
            corrected_weight = min(corrected_weight, max_allowed)

            # Si la corrección resultó en un peso muy alto, podría ser un toro de élite
            if corrected_weight > weight_max * 1.5:
                print(
                    f"🔧 Corrección aplicada (animal excepcional): {raw_weight:.1f} kg → {corrected_weight:.1f} kg "
                    f"(factor: {correction_factor:.2f}x, raza: {breed.value}, "
                    f"razón: {correction_reason}, posible toro reproductor de élite)"
                )
            else:
                print(
                    f"🔧 Corrección aplicada: {raw_weight:.1f} kg → {corrected_weight:.1f} kg "
                    f"(factor: {correction_factor:.2f}x, raza: {breed.value}, "
                    f"razón: {correction_reason})"
                )

            return corrected_weight

        # Si el peso está en el rango alto del modelo (80-100%), no corregir
        # El modelo probablemente está estimando correctamente

        # Si el peso está por encima del máximo del modelo pero dentro de lo razonable,
        # aceptarlo (el modelo puede estar extrapolando correctamente)
        if raw_weight > weight_max and raw_weight <= real_max:
            return raw_weight

        # Si el peso está por encima del máximo real conocido, limitarlo
        if raw_weight > real_max:
            print(
                f"⚠️ Peso limitado: {raw_weight:.1f} kg → {real_max:.1f} kg "
                f"(máximo conocido para {breed.value})"
            )
            return real_max

        return raw_weight

    def _calculate_confidence(self, weight: float, breed: BreedType) -> float:
        """
        Calcula confidence basado en peso estimado y rango típico de la raza.

        TODO: Mejorar con confidence real del modelo si está disponible.
        """
        # Rangos típicos por raza (alineados con entrenamiento ML)
        # Basados en LIFESTAGE_WEIGHT_RANGES del notebook Colab
        breed_ranges = {
            BreedType.NELORE: (
                250,
                650,
            ),  # novillo: 250-380, vaca: 380-520, toro: 480-650
            BreedType.BRAHMAN: (
                260,
                680,
            ),  # novillo: 260-400, vaca: 390-540, toro: 500-680
            BreedType.GUZERAT: (
                240,
                650,
            ),  # novillo: 240-360, vaca: 360-520, toro: 480-650
            BreedType.SENEPOL: (
                280,
                620,
            ),  # novillo: 280-400, vaca: 360-480, toro: 500-620
            BreedType.GIROLANDO: (
                240,
                640,
            ),  # novilla: 240-340, vaca: 420-580, toro: 500-640
            BreedType.GYR_LECHERO: (
                220,
                620,
            ),  # novilla: 220-320, vaca: 380-520, toro: 470-620
            BreedType.SINDI: (150, 380),  # novilla: 150-230, vaca: 260-380
        }

        weight_min, weight_max = breed_ranges.get(breed, (300, 700))

        # Si está en rango típico, confidence alto
        if weight_min <= weight <= weight_max:
            return 0.92
        if weight < weight_min * 0.8 or weight > weight_max * 1.2:
            return 0.75  # Fuera de rango, confidence menor
        return 0.85  # Cerca del rango

    def get_strategy_name(self) -> str:
        """Retorna nombre de la estrategia."""
        return "deep_learning_tflite"

    def is_available(self) -> bool:
        """
        Verifica si la estrategia está disponible.

        Returns:
            True si hay modelo TFLite disponible
        """
        try:
            self._ensure_model_loaded()
            return True
        except Exception:
            return False

    def get_loaded_models(self) -> dict:
        """
        Obtiene información de modelos cargados.

        Returns:
            Dict con info de modelos ML
        """
        return {
            "total_loaded": 1 if self._model is not None else 0,
            "models": ["generic"] if self._model is not None else [],
            "strategy": self.get_strategy_name(),
        }

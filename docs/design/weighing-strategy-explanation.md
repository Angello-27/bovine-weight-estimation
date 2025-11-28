# Estrategia de Pesaje: Por Hato, Raza y Edad

**Objetivo**: Explicar por qué el sistema organiza el pesaje por grupos (hato), raza y categoría de edad  
**Fecha**: 2024-12-XX

---

## 🎯 Razones Fundamentales

### 1. **Pesaje por Hato (Grupo)**

#### Eficiencia Operativa
- **Tiempo optimizado**: En lugar de pesaje individual disperso, se agrupan animales del mismo potrero/finca
- **Reducción de desplazamientos**: Se pesa un grupo completo en una sesión
- **Organización**: Facilita la coordinación de personal y equipos

#### Casos de Uso
```
Ejemplo: Sesión de pesaje masivo
- Potrero Norte: 50 animales (Brahman + Nelore)
- Potrero Sur: 30 animales (Guzerat)
- Potrero Este: 20 animales (Vaquillonas)

En lugar de:
❌ Ir a Potrero Norte → pesear 1 animal → ir a Potrero Sur → pesear 1 animal...

Se hace:
✅ Ir a Potrero Norte → pesear los 50 animales → ir a Potrero Sur → pesear los 30...
```

#### Beneficios
- **Reducción de tiempo**: De 2-3 días para 20 animales → <2 horas para 20 animales
- **Menor estrés animal**: Agrupar reduce movimientos innecesarios
- **Mejor planificación**: Se puede programar sesiones por potrero/finca

---

### 2. **Pesaje por Raza**

#### Razón Técnica: Modelos ML Específicos

**Cada raza tiene características morfológicas distintas**:
- **Nelore**: Cuerpo más alargado, joroba pronunciada
- **Brahman**: Tamaño grande, cuello largo
- **Guzerat**: Doble propósito, estructura diferente
- **Senepol**: Compacto, adaptado al calor

#### Modelos TFLite por Raza

```python
# Cada raza tiene su modelo ML entrenado específicamente
Modelos disponibles:
- brahman-v1.0.0.tflite
- nelore-v1.0.0.tflite
- guzerat-v1.0.0.tflite
- senepol-v1.0.0.tflite
- girolando-v1.0.0.tflite
- gyr_lechero-v1.0.0.tflite
- sindi-v1.0.0.tflite
```

#### Precisión Mejorada

| Estrategia | Precisión | Razón |
|-----------|-----------|-------|
| **Modelo único** | ~88% (R²) | No captura diferencias morfológicas |
| **Modelo por raza** | ≥95% (R²) | Entrenado específicamente para cada raza |

#### Fórmulas Morfométricas por Raza

Incluso en el sistema híbrido (Sprint 1-2), las fórmulas son específicas:

```python
# Ejemplo: Fórmulas diferentes por raza
def estimate_weight_brahman(length, height):
    return (length * height * 0.85) / 1000  # Coeficiente específico

def estimate_weight_nelore(length, height):
    return (length * height * 0.92) / 1000  # Coeficiente diferente
```

#### Beneficios
- **Mayor precisión**: ≥95% vs ~88% con modelo genérico
- **Validación específica**: Rangos de peso esperados por raza
- **Mejor gestión**: Diferentes razas tienen diferentes necesidades nutricionales

---

### 3. **Pesaje por Categoría de Edad (Tiempo de Vida)**

#### 4 Categorías de Edad

```python
1. Terneros (<8 meses)
   - Peso esperado: 50-200 kg
   - Crecimiento rápido
   - Requiere validación de rango

2. Vaquillonas/Torillos (6-18 meses)
   - Peso esperado: 200-350 kg
   - Etapa de desarrollo
   - Validación crítica para cruces

3. Vaquillonas/Toretes (19-30 meses)
   - Peso esperado: 350-500 kg
   - Pre-reproductivos
   - Decisión de cruce

4. Vacas/Toros (>30 meses)
   - Peso esperado: 400-800 kg
   - Adultos reproductivos
   - Monitoreo de salud
```

#### Razones de Validación

**1. Detección de Anomalías**
```python
# Ejemplo: Ternero de 6 meses con peso de 500 kg
if age_category == AgeCategory.TERNEROS:
    if weight > 250:  # Límite superior esperado
        raise ValidationError("Peso fuera de rango esperado para ternero")
```

**2. Crecimiento Diferenciado**
- **Terneros**: Crecen ~1-2 kg/día
- **Vaquillonas**: Crecen ~0.5-1 kg/día
- **Adultos**: Mantienen peso ±5%

**3. Decisiones de Negocio**
- **Cruces**: Vaquillonas de 19-30 meses deben pesar 350-500 kg
- **Venta**: Terneros listos para venta >200 kg
- **Reproducción**: Vacas adultas deben mantener peso reproductivo

#### Beneficios
- **Validación automática**: Detecta errores de estimación
- **Alertas inteligentes**: Pérdida de peso en terneros es crítica
- **Mejor gestión**: Diferentes estrategias nutricionales por edad

---

## 📊 Ejemplo Práctico: Sesión de Pesaje

### Escenario Real: Hacienda Gamelera

```
Sesión: Pesaje Potrero Norte - Viernes 20 Dic 2024, 8:00 AM

Grupo 1: Terneros Brahman (15 animales)
├─ Raza: Brahman
├─ Edad: 4-7 meses (Terneros)
├─ Modelo ML: brahman-v1.0.0.tflite
├─ Validación: Peso esperado 80-180 kg
└─ Tiempo estimado: 15 animales × 3 min = 45 min

Grupo 2: Vaquillonas Nelore (20 animales)
├─ Raza: Nelore
├─ Edad: 12-16 meses (Vaquillonas/Torillos)
├─ Modelo ML: nelore-v1.0.0.tflite
├─ Validación: Peso esperado 250-400 kg
└─ Tiempo estimado: 20 animales × 3 min = 60 min

Grupo 3: Vacas Guzerat (15 animales)
├─ Raza: Guzerat
├─ Edad: 36-60 meses (Vacas/Toros)
├─ Modelo ML: guzerat-v1.0.0.tflite
├─ Validación: Peso esperado 450-700 kg
└─ Tiempo estimado: 15 animales × 3 min = 45 min

Total: 50 animales en ~2.5 horas
```

---

## 🔄 Flujo de Trabajo Optimizado

### 1. Planificación (Cronograma)
```
Alert programado:
- Tipo: SCHEDULED_WEIGHING
- Fecha: 20 Dic 2024, 8:00 AM
- Grupo: Potrero Norte
- Animales: 50 (Brahman + Nelore + Guzerat)
- Recordatorios: 7 días antes, 1 día antes
```

### 2. Ejecución
```
1. Llegar a Potrero Norte
2. Agrupar por raza:
   - Primero: Terneros Brahman (15)
   - Segundo: Vaquillonas Nelore (20)
   - Tercero: Vacas Guzerat (15)
3. Para cada grupo:
   - Cargar modelo ML específico de raza
   - Validar categoría de edad
   - Estimar peso con validación de rango
```

### 3. Validación Automática
```python
# El sistema valida automáticamente:
if animal.breed == BreedType.BRAHMAN:
    model = load_model("brahman-v1.0.0.tflite")
    
if animal.age_category == AgeCategory.TERNEROS:
    if estimated_weight > 250:
        alert = create_alert(
            type=AlertType.WEIGHT_ANOMALY,
            message="Peso fuera de rango para ternero"
        )
```

---

## 💡 Beneficios Combinados

### Eficiencia
- **Tiempo**: 2-3 días → <2 horas (80% reducción)
- **Organización**: Sesiones planificadas por grupo
- **Precisión**: ≥95% con modelos específicos por raza

### Gestión Inteligente
- **Alertas automáticas**: Detecta anomalías por edad/raza
- **Reportes agrupados**: Análisis por hato, raza, edad
- **Planificación**: Cronograma optimizado por ubicación

### Validación Robusta
- **Rangos de peso**: Validación automática por edad
- **Modelos específicos**: Precisión mejorada por raza
- **Detección de errores**: Alertas cuando peso está fuera de rango

---

## 📋 Resumen

| Criterio | Razón | Beneficio |
|----------|-------|-----------|
| **Por Hato** | Eficiencia operativa | Reducción 80% tiempo |
| **Por Raza** | Modelos ML específicos | Precisión ≥95% |
| **Por Edad** | Validación y gestión | Detección de anomalías |

**Conclusión**: La estrategia de pesaje por hato, raza y edad optimiza tiempo, mejora precisión y permite gestión inteligente del ganado.


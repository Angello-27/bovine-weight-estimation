# 01. Contexto del Sistema

## Contexto del Proyecto

**Cliente**: Hacienda Gamelera  
**Propietario**: Bruno Brito Macedo  
**Ubicación**: San Ignacio de Velasco, Bolivia  
**Escala**: 500 cabezas de ganado bovino

### Características de la Operación

- **Ubicación GPS**: 15°51′34.2′′S, 60°47′52.4′′W
- **Extensión**: 48.5 hectáreas
- **Hato**: 500 cabezas de ganado bovino
- **Razas principales soportadas**:
  - Brahman
  - Nelore
  - Angus
  - Cebuinas (Bos indicus)
  - Criollo (Bos taurus)
  - Pardo Suizo
  - Jersey
- **Categorías de manejo por edad**:
  - Terneros (<8 meses)
  - Vaquillonas/torillos (6-18 meses)
  - Vaquillonas/toretes (19-30 meses)
  - Vacas/toros (>30 meses)

### Situación Actual (Antes del Sistema)

#### Proceso de Pesaje Tradicional

- **Método actual**: Básculas mecánicas y cinta bovinométrica
- **Tiempo de procesamiento**: 2-3 días para procesar 20 animales
- **Calibración diaria**: 30-45 minutos de preparación
- **Coordinación de personal**: 1-2 horas de organización
- **Error de estimación**: 5-20 kg con fórmula Schaeffer
- **Tasa de reintento**: 1 de cada 10 animales por lecturas inestables

#### Limitaciones Identificadas

- Dependencia de equipos especializados costosos
- Requerimiento de personal técnico especializado
- Proceso manual propenso a errores humanos
- Tiempo excesivo de procesamiento
- Dificultad para mantener registros históricos
- Imposibilidad de procesamiento en condiciones climáticas adversas

#### Método Actual de Estimación (Fórmula de Schaeffer)

Para animales en observación semanal, se utiliza la cinta bovinométrica con la fórmula:

Peso (kg) = (PT² × LC) / 10838

Donde:

- **PT**: Perímetro Torácico (en cm)
- **LC**: Longitud del Cuerpo (en cm)

**Limitaciones del método**:

- Error de medición: 5-20 kg por animal
- Dependencia de habilidad del operario
- Tiempo requerido: 8-10 minutos por animal
- Riesgo de errores en cálculo manual
- Problemas en dosificación médica (errores de peso)
- Riesgos en decisiones de cruce (peso subestimado en vaquillas)

### Solución Propuesta (Después del Sistema)

#### Objetivos Específicos del Sistema

- **Reducción de tiempo**: <2 horas para procesar 20 animales
- **Precisión objetivo**: >95% en estimación de peso
- **Eliminación de**: calibración diaria y coordinación extensa de personal
- **Método innovador**: captura continua de fotogramas con dispositivos móviles

#### Características Técnicas Específicas

- **Captura continua**: No es captura manual de fotografías individuales
- **Procesamiento inteligente**: Evaluación en tiempo real de calidad, iluminación y enfoque
- **Selección automática**: Mejor fotograma seleccionado automáticamente
- **Procesamiento especializado**: Según tipo de raza específica del ganado

## Diagrama C4 Nivel 1 - Contexto del Sistema

### Descripción del Sistema

El **Sistema de Estimación de Peso Bovino con IA** es una solución tecnológica integral desarrollada específicamente para la Hacienda Gamelera, que permite estimar el peso de bovinos utilizando inteligencia artificial, eliminando la necesidad de equipos de pesaje tradicionales y reduciendo significativamente el tiempo de procesamiento.

### Actores del Sistema

#### 1. Ganadero (Bruno Brito Macedo - Hacienda Gamelera)

- **Rol**: Usuario principal y propietario del sistema
- **Responsabilidades**:
  - Captura continua de fotogramas de bovinos
  - Registro de datos básicos de animales
  - Consulta de estimaciones de peso en tiempo real
  - Revisión de reportes y análisis de crecimiento
  - Configuración de alertas y recordatorios personalizados
- **Necesidades específicas**:
  - Interfaz intuitiva para uso en campo
  - Funcionalidad offline para operación rural
  - Reportes claros para toma de decisiones
  - Sincronización automática de datos
  - Procesamiento rápido para 500 cabezas de ganado

#### 2. Sistema de Estimación de Peso Bovino

- **Rol**: Sistema principal que procesa y analiza datos
- **Responsabilidades**:
  - Captura continua de fotogramas durante períodos determinados
  - Procesamiento automático con modelos de IA especializados
  - Evaluación en tiempo real de calidad de imagen
  - Selección automática del mejor fotograma
  - Estimación de peso según raza específica
  - Gestión de datos de animales y pesajes históricos
  - Generación de reportes y análisis de crecimiento
  - Sincronización automática entre dispositivos
- **Características técnicas**:
  - Arquitectura móvil con backend en la nube
  - Procesamiento local de IA con TensorFlow Lite
  - Almacenamiento seguro en la nube
  - Funcionalidad offline completa
  - Optimización para 500 cabezas de ganado


### Relaciones Externas

#### Ganadero ↔ Sistema

- **Flujo de datos**:
  - Ganadero captura fotogramas continuos de animales
  - Sistema procesa y devuelve estimaciones de peso en tiempo real
  - Sincronización bidireccional de datos históricos
- **Protocolos**: HTTPS, JSON, imágenes optimizadas
- **Frecuencia**: Diaria/semanal según necesidades operativas


### Contexto Tecnológico

#### Entorno Operativo

- **Ubicación**: Hacienda Gamelera, San Ignacio de Velasco, Bolivia
- **Conectividad**: Intermitente (3G/4G limitado, WiFi en oficinas)
- **Dispositivos**: Smartphones Android/iOS del personal
- **Condiciones**: Clima tropical, exposición a elementos naturales
- **Escala**: 500 cabezas de ganado bovino

#### Requisitos No Funcionales Específicos

- **Disponibilidad**: 99% uptime para funcionalidad offline
- **Rendimiento**: Procesamiento de fotogramas < 3 segundos
- **Escalabilidad**: Soporte para 500+ animales con crecimiento futuro
- **Precisión**: >95% de exactitud en estimación de peso
- **Usabilidad**: Interfaz intuitiva para personal no técnico
- **Durabilidad**: Resistencia a condiciones climáticas tropicales

### Alcance del Sistema

#### Incluido

- **Gestión de Datos (Área 1)**:
  - **Captura continua**: 10-15 fotogramas por segundo durante 3-5 segundos
  - **Evaluación en tiempo real**: Cada fotograma es evaluado según criterios de:
    - Nitidez (sharpness > 0.7)
    - Iluminación (brightness 0.4-0.8)
    - Contraste (contrast > 0.5)
    - Visibilidad de silueta (silhouette_visibility > 0.8)
    - Ángulo apropiado (angle_score > 0.6)
  - **Selección automática**: Score global ponderado (Silueta 40%, Nitidez 30%, Iluminación 20%, Ángulo 10%)
  - **Procesamiento por raza**: Modelos ML específicos para las 7 razas bovinas
  - **Registro digital**: Automático con fecha, hora, ubicación GPS, precisión >95%
- **Análisis y Reportes**: Historial completo, gráficos de evolución, comparativas entre animales
- **Monitoreo y Planificación**: Alertas automáticas, recordatorios, calendario integrado
- **Funcionalidades de Usuario**: Búsqueda avanzada, listas personalizadas, personalización de interfaz
- **Operación y Respaldos**: Funcionamiento offline, sincronización automática, respaldos automáticos

#### Excluido

- Gestión financiera del negocio ganadero
- Control de inventario de insumos y medicamentos
- Gestión de personal y nóminas
- Integración con sistemas contables externos
- Control de enfermedades (más allá de registros básicos)
- Gestión de ventas y comercialización

### Beneficios Esperados

#### Para la Hacienda Gamelera

- **Reducción de costos**: Eliminación de equipos de pesaje especializados
- **Ahorro de tiempo**: De 2-3 días a <2 horas para 20 animales
- **Mayor precisión**: >95% vs 5-20 kg de error actual
- **Mejor trazabilidad**: Registros digitales automáticos
- **Toma de decisiones**: Datos históricos y análisis de crecimiento
- **Trazabilidad digital**: Registros históricos completos


### Métricas de Éxito

#### Métricas Operativas

- **Tiempo de procesamiento**: <2 horas para 20 animales (vs 2-3 días actual) - Reducción de 80%
- **Precisión de estimación**: >95% (vs error actual de 5-20 kg con fórmula Schaeffer)
- **Error absoluto promedio**: <5 kg por animal
- **Coeficiente de determinación (R²)**: ≥0.95
- **Tiempo de captura y procesamiento**: <3 segundos por estimación
- **Eliminación de reintentos**: 0% (vs 10% actual que requería 2-3 intentos)
  - *Justificación: La captura continua evalúa 30-75 fotogramas y selecciona automáticamente el mejor, eliminando completamente la necesidad de reintentos*
- **Eliminación de calibración diaria**: Ahorro de 30-45 minutos por jornada
- **Disponibilidad del sistema**: >99% uptime offline

#### Métricas de Negocio

- **Reducción de tiempo operativo**: 80% (de 2-3 días a <2 horas para 20 animales)
- **Ahorro en calibración**: 30-45 minutos diarios eliminados
- **Reducción de personal requerido**: De 3-4 personas (capataz, vaquero, peón) a 1 operador con smartphone
- **Mejora de precisión**: De ±5-20 kg (fórmula Schaeffer) a >95% con error <5 kg
- **Eliminación de reintentos**: De 10% de animales requiriendo 2-3 intentos a 0%
- **Cobertura de razas**: 7 razas bovinas soportadas
- **Validación en campo**: 50 animales mínimo en condiciones reales
- **Satisfacción del usuario**: >90% (a validar en pruebas de campo)
- **Trazabilidad digital**: 100% de registros históricos completos

## Decisiones Técnicas Validadas

- **Offline-first** (CONFIRMADO: zona rural sin conectividad estable)
- **Móvil** (CONFIRMADO: Bruno Brito Macedo tiene smartphones Android/iOS)
- **Precisión >95%** (POR VALIDAR en Sprint 1)
- **Captura continua** (CONFIRMADO: 10-15 FPS durante 3-5 segundos)
- **7 razas bovinas** (CONFIRMADO: Brahman, Nelore, Angus, Cebuinas, Criollo, Pardo Suizo, Jersey)

## Decisiones Técnicas Pendientes

- **Stack específico** (Flutter vs React Native - decidir en Sprint 1)
- **Base de datos** (MongoDB vs PostgreSQL - decidir cuando sea necesario)
- **Arquitectura interna** (emergente según necesidades reales)
- **Modelos ML específicos** (TensorFlow Lite vs otros - validar en Sprint 1)
- **Estrategia de sincronización** (last-write-wins vs otros - implementar según necesidad)
- **UI/UX específica** (emergente según feedback de Bruno Brito Macedo)

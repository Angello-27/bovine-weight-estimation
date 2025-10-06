# 05. Decisiones Tecnológicas (ADRs)

## Architecture Decision Records (ADRs)

### ADR-001: Selección de Flutter para la Aplicación Móvil

**Fecha**: 2024-01-15  
**Estado**: Aceptado  
**Decisor**: Equipo de Arquitectura  

#### Contexto ADR-001

Necesitamos desarrollar una aplicación móvil que funcione en Android e iOS para el sistema de estimación de peso bovino. La aplicación debe:

- Funcionar offline en condiciones rurales
- Procesar imágenes en tiempo real
- Tener una interfaz intuitiva para usuarios no técnicos
- Sincronizar datos cuando hay conectividad

#### Opciones Consideradas ADR-001

1. **Flutter (Dart)**
2. **React Native (JavaScript)**
3. **Desarrollo Nativo (Kotlin/Swift)**
4. **Xamarin (C#)**

#### Decisión ADR-001

Se selecciona **Flutter** como framework principal.

#### Justificación ADR-001

- **Rendimiento**: Compilación nativa con AOT, rendimiento cercano al nativo
- **Desarrollo**: Un solo código base para Android e iOS
- **Ecosistema**: Amplio soporte para ML (TFLite, ML Kit)
- **Offline**: Excelente soporte para funcionalidad offline
- **UI**: Material Design y Cupertino widgets nativos
- **Comunidad**: Crecimiento rápido y soporte de Google
- **Mantenimiento**: Menor complejidad de mantenimiento

#### Consecuencias ADR-001

- **Positivas**: Desarrollo más rápido, menor costo, mejor rendimiento
- **Negativas**: Dependencia de Google, curva de aprendizaje para Dart
- **Riesgos**: Cambios en la estrategia de Google con Flutter

---

### ADR-002: Implementación de Clean Architecture

**Fecha**: 2024-01-15  
**Estado**: Aceptado  
**Decisor**: Equipo de Arquitectura  

#### Contexto ADR-002

Necesitamos una arquitectura que permita:

- Separación clara de responsabilidades
- Testabilidad de componentes
- Independencia de frameworks
- Escalabilidad del código

#### Opciones Consideradas ADR-002

1. **Clean Architecture**
2. **MVC (Model-View-Controller)**
3. **MVVM (Model-View-ViewModel)**
4. **Arquitectura Simple (sin capas)**

#### Decisión ADR-002

Se implementa **Clean Architecture** con las siguientes capas:

- **Presentation**: UI, Widgets, Providers
- **Domain**: Entities, Use Cases, Repository Interfaces
- **Data**: Models, Repository Implementations, Data Sources

#### Justificación ADR-002

- **Separación**: Cada capa tiene responsabilidades específicas
- **Testabilidad**: Fácil testing de lógica de negocio
- **Independencia**: La lógica de negocio no depende de frameworks
- **Mantenibilidad**: Código más fácil de mantener y extender
- **SOLID**: Cumple con los principios SOLID

#### Consecuencias ADR-002

- **Positivas**: Código más limpio, mejor testabilidad, mayor mantenibilidad
- **Negativas**: Mayor complejidad inicial, más archivos
- **Riesgos**: Over-engineering si no se maneja correctamente

---

### ADR-003: Selección de MongoDB como Base de Datos

**Fecha**: 2024-01-15  
**Estado**: Aceptado  
**Decisor**: Equipo de Arquitectura  

#### Contexto ADR-003

Necesitamos una base de datos que soporte:

- Datos semi-estructurados (metadatos de animales)
- Escalabilidad horizontal
- Consultas geográficas (ubicación de fincas)
- Flexibilidad en el esquema

#### Opciones Consideradas ADR-003

1. **MongoDB (NoSQL)**
2. **PostgreSQL (SQL)**
3. **MySQL (SQL)**
4. **Firebase Firestore (NoSQL)**

#### Decisión ADR-003

Se selecciona **MongoDB** como base de datos principal.

#### Justificación ADR-003

- **Flexibilidad**: Esquema flexible para datos variables
- **Escalabilidad**: Sharding nativo para escalabilidad horizontal
- **Geográfico**: Soporte nativo para consultas geográficas
- **JSON**: Almacenamiento nativo en JSON
- **Agregaciones**: Pipeline de agregación potente
- **Rendimiento**: Buen rendimiento para consultas complejas

#### Consecuencias ADR-003

- **Positivas**: Mayor flexibilidad, mejor escalabilidad, consultas geográficas
- **Negativas**: Curva de aprendizaje, menos herramientas de administración
- **Riesgos**: Consistencia eventual, menos madurez que SQL

---

### ADR-004: Uso de TensorFlow Lite para Inferencia Local

**Fecha**: 2024-01-15  
**Estado**: Aceptado  
**Decisor**: Equipo de Arquitectura  

#### Contexto ADR-004

Necesitamos ejecutar modelos de IA para estimación de peso:

- Funcionamiento offline en condiciones rurales
- Bajo consumo de recursos en dispositivos móviles
- Procesamiento en tiempo real
- Actualización de modelos sin reinstalar la app

#### Opciones Consideradas ADR-004

1. **TensorFlow Lite (Local)**
2. **API de Inferencia Remota**
3. **Core ML (iOS) / ML Kit (Android)**
4. **PyTorch Mobile**

#### Decisión ADR-004

Se utiliza **TensorFlow Lite** para inferencia local.

#### Justificación ADR-004

- **Offline**: Funciona completamente offline (crítico en San Ignacio de Velasco)
- **Conectividad rural**: Áreas de pastoreo sin cobertura 3G/4G constante
- **Latencia**: Sin latencia de red en zonas remotas de Bolivia
- **Costo**: Ahorro en datos móviles (costosos en áreas rurales)
- **Rendimiento**: Procesamiento en tiempo real sin dependencia de internet
- **Privacidad**: Datos no salen del dispositivo
- **Flexibilidad**: Soporte para modelos específicos por raza boliviana

#### Consecuencias ADR-004

- **Positivas**: Funcionamiento offline, menor latencia, mayor privacidad
- **Negativas**: Limitaciones de hardware, modelos más pequeños
- **Riesgos**: Rendimiento variable según dispositivo

---

### ADR-005: Selección de Provider para Gestión de Estado

**Fecha**: 2024-01-15  
**Estado**: Aceptado  
**Decisor**: Equipo de Arquitectura  

#### Contexto ADR-005

Necesitamos un patrón de gestión de estado que:

- Sea fácil de entender y usar
- Tenga buen rendimiento
- Soporte funcionalidad offline
- Sea compatible con Clean Architecture

#### Opciones Consideradas ADR-005

1. **Provider**
2. **Bloc/Cubit**
3. **Riverpod**
4. **GetX**
5. **Estado Simple (setState)**

#### Decisión ADR-005

Se selecciona **Provider** como patrón de gestión de estado.

#### Justificación ADR-005

- **Simplicidad**: Fácil de entender y implementar
- **Rendimiento**: Buen rendimiento con ChangeNotifier
- **Integración**: Integración nativa con Flutter
- **Testing**: Fácil de testear
- **Comunidad**: Amplia adopción y documentación
- **Flexibilidad**: Soporte para múltiples providers

#### Consecuencias ADR-005

- **Positivas**: Fácil aprendizaje, buen rendimiento, amplia comunidad
- **Negativas**: Puede volverse complejo en apps grandes
- **Riesgos**: Posible migración a Riverpod en el futuro

---

### ADR-006: Uso de FastAPI para el Backend

**Fecha**: 2024-01-15  
**Estado**: Aceptado  
**Decisor**: Equipo de Arquitectura  

#### Contexto ADR-006

Necesitamos un backend que:

- Proporcione APIs REST
- Tenga buen rendimiento
- Sea fácil de desarrollar y mantener
- Soporte procesamiento de imágenes
- Tenga documentación automática

#### Opciones Consideradas ADR-006

1. **FastAPI (Python)**
2. **Django REST Framework (Python)**
3. **Node.js + Express**
4. **Spring Boot (Java)**
5. **Go + Gin**

#### Decisión ADR-006

Se selecciona **FastAPI** como framework del backend.

#### Justificación ADR-006

- **Rendimiento**: Alto rendimiento, comparable a Node.js
- **Desarrollo**: Desarrollo rápido con type hints
- **Documentación**: Documentación automática con OpenAPI
- **Validación**: Validación automática con Pydantic
- **Async**: Soporte nativo para programación asíncrona
- **ML**: Excelente integración con librerías de ML

#### Consecuencias ADR-006

- **Positivas**: Desarrollo rápido, buena documentación, alto rendimiento
- **Negativas**: Menor madurez que Django, dependencia de Python
- **Riesgos**: Cambios en el ecosistema de Python

---

### ADR-007: Implementación de Atomic Design

**Fecha**: 2024-01-15  
**Estado**: Aceptado  
**Decisor**: Equipo de Arquitectura  

#### Contexto ADR-007

Necesitamos un sistema de diseño que:

- Promueva la reutilización de componentes
- Mantenga consistencia en la UI
- Facilite el mantenimiento
- Escale con el crecimiento de la aplicación

#### Opciones Consideradas ADR-007

1. **Atomic Design**
2. **Design System Tradicional**
3. **Componentes Ad-hoc**
4. **Material Design Components**

#### Decisión ADR-007

Se implementa **Atomic Design** con la siguiente estructura:

- **Atoms**: Componentes básicos (botones, inputs, textos)
- **Molecules**: Combinaciones de átomos (formularios, tarjetas)
- **Organisms**: Secciones complejas (headers, sidebars)
- **Templates**: Layouts de página
- **Pages**: Instancias específicas

#### Justificación ADR-007

- **Reutilización**: Componentes altamente reutilizables
- **Consistencia**: Diseño consistente en toda la aplicación
- **Mantenimiento**: Fácil mantenimiento y actualización
- **Escalabilidad**: Escala bien con el crecimiento
- **Colaboración**: Mejor colaboración entre diseñadores y desarrolladores

#### Consecuencias ADR-007

- **Positivas**: Mayor reutilización, mejor consistencia, fácil mantenimiento
- **Negativas**: Overhead inicial, posible over-engineering
- **Riesgos**: Complejidad innecesaria para componentes simples

---

### ADR-008: Uso de AWS S3 para Almacenamiento de Archivos

**Fecha**: 2024-01-15  
**Estado**: Aceptado  
**Decisor**: Equipo de Arquitectura  

#### Contexto ADR-008

Necesitamos almacenar:

- Imágenes originales y procesadas
- Modelos de ML
- Backups de datos
- Archivos de configuración

#### Opciones Consideradas ADR-008

1. **AWS S3**
2. **Google Cloud Storage**
3. **Azure Blob Storage**
4. **Almacenamiento Local del Servidor**

#### Decisión ADR-008

Se utiliza **AWS S3** para almacenamiento de archivos.

#### Justificación ADR-008

- **Escalabilidad**: Escalabilidad ilimitada
- **Durabilidad**: 99.999999999% de durabilidad
- **Rendimiento**: Alto rendimiento y baja latencia
- **Costo**: Modelo de precios flexible
- **Integración**: Buena integración con otros servicios AWS
- **CDN**: Integración con CloudFront para distribución global

#### Consecuencias ADR-008

- **Positivas**: Alta escalabilidad, gran durabilidad, buen rendimiento
- **Negativas**: Dependencia de AWS, costos variables
- **Riesgos**: Vendor lock-in, cambios en precios

---

### ADR-009: Implementación de Arquitectura Offline-First

**Fecha**: 2024-01-15  
**Estado**: Aceptado  
**Decisor**: Equipo de Arquitectura  

#### Contexto ADR-009

La Hacienda Gamelera está en San Ignacio de Velasco, área rural con:

- Conectividad intermitente (3G/4G irregular)
- Sin WiFi en campos de pastoreo
- Necesidad de operar completamente sin conexión
- Sincronización cuando hay conectividad disponible

#### Opciones Consideradas ADR-009

1. **Offline-First (SQLite local + sincronización)**
2. **Online-Only (requiere conexión permanente)**
3. **Hybrid (funciones básicas offline, avanzadas online)**
4. **Cache-First (con fallback a offline)**

#### Decisión ADR-009

Se implementa **arquitectura Offline-First** con SQLite como fuente de verdad local.

#### Justificación ADR-009

- **Realidad del campo**: Sin conectividad garantizada en áreas de pastoreo
- **Continuidad operativa**: Trabajo sin interrupciones por falta de señal
- **Experiencia de usuario**: Sin frustraciones por errores de conexión
- **Eficiencia**: Procesamiento local más rápido que round-trip al servidor
- **Costo**: Ahorro en consumo de datos móviles

#### Estrategia de Sincronización

- **Patrón**: Queue de operaciones pendientes con retry automático
- **Resolución de conflictos**: Last-Write-Wins basado en timestamps
- **Indicador visual**: Estado de sincronización siempre visible
- **Prioridad**: Datos críticos (pesajes) se sincronizan primero

#### Consecuencias ADR-009

- **Positivas**: Funcionamiento en campo sin conexión, mejor UX, menor frustración
- **Negativas**: Complejidad de sincronización, posibles conflictos de datos
- **Riesgos**: Conflictos si múltiples usuarios modifican mismo animal offline

---

### ADR-010: Procesamiento de Fotogramas en Tiempo Real

**Fecha**: 2024-01-15  
**Estado**: Aceptado  
**Decisor**: Equipo de Arquitectura  

#### Contexto ADR-010

Necesitamos capturar bovinos en movimiento en la Hacienda Gamelera:

- **Razas presentes**: Brahman, Nelore, Angus, Cebuinas (Bos indicus), Criollo (Bos taurus), Pardo Suizo, Jersey
- **Categorías de edad**: 4 categorías específicas según edad
- Animales no permanecen quietos
- Condiciones de iluminación variables
- Ángulos no siempre óptimos
- Usuario no experto en fotografía

#### Opciones Consideradas ADR-010

1. **Captura Continua + Evaluación en Tiempo Real**
2. **Captura Manual con Guías Visuales**
3. **Ráfaga de Fotos + Selección Manual**
4. **Video + Post-procesamiento**

#### Decisión ADR-010

Se implementa **captura continua con evaluación en tiempo real** de fotogramas.

#### Justificación ADR-010

- **Automatización**: Usuario solo apunta, el sistema selecciona
- **Calidad**: Evaluación objetiva de múltiples criterios
- **Velocidad**: Selección en tiempo real, sin esperas
- **Precisión**: Mejor fotograma = mejor estimación de peso
- **UX**: Experiencia simple para usuarios no técnicos

#### Especificaciones Técnicas

- **FPS**: 10-15 fotogramas por segundo
- **Duración**: 3-5 segundos de captura continua
- **Criterios de evaluación**:
  - Nitidez (sharpness > 0.7)
  - Iluminación (brightness 0.4-0.8)
  - Visibilidad de silueta (silhouette_visibility > 0.8)
  - Ángulo apropiado (angle_score > 0.6)
- **Selección**: Score global ponderado, mejor fotograma gana

#### Consecuencias ADR-010

- **Positivas**: Mejor calidad de estimación, UX simplificada, automatización
- **Negativas**: Mayor procesamiento, consumo de batería, más almacenamiento temporal
- **Riesgos**: Rendimiento en dispositivos de gama baja

---

### ADR-011: Versionado y Distribución de Modelos ML

**Fecha**: 2024-01-15  
**Estado**: Aceptado  
**Decisor**: Equipo de Arquitectura  

#### Contexto ADR-011

Los modelos de ML deben:

- Actualizarse sin reinstalar la app
- Mejorar con nuevos datos de entrenamiento
- Soportar múltiples razas bovinas
- Garantizar integridad y seguridad

#### Opciones Consideradas ADR-011

1. **Descarga desde S3 con manifest.json versionado**
2. **Modelos embebidos en la app (actualización via store)**
3. **API remota de inferencia (sin modelos locales)**
4. **Peer-to-peer entre dispositivos**

#### Decisión ADR-011

Se implementa **descarga desde S3 con sistema de versionado mediante manifest.json**.

#### Justificación ADR-011

- **Flexibilidad**: Actualización sin pasar por app stores
- **Rapidez**: Deploy de nuevos modelos en minutos
- **Rollback**: Fácil volver a versión anterior si falla
- **Razas específicas**: Diferentes modelos por raza
- **Validación**: Checksum MD5 garantiza integridad

#### Estructura de Versionado

```json
{
  "version": "1.2.0",
  "models": {
    "brahman": {
      "url": "s3://models/brahman-v1.2.0.tflite",
      "md5": "abc123...",
      "size_mb": 4.5,
      "min_app_version": "1.0.0"
    },
    "nelore": {
      "url": "s3://models/nelore-v1.2.0.tflite",
      "md5": "def456...",
      "size_mb": 4.2,
      "min_app_version": "1.0.0"
    },
    "angus": {
      "url": "s3://models/angus-v1.2.0.tflite",
      "md5": "ghi789...",
      "size_mb": 4.3,
      "min_app_version": "1.0.0"
    },
    "cebuinas": {
      "url": "s3://models/cebuinas-v1.2.0.tflite",
      "md5": "jkl012...",
      "size_mb": 4.4,
      "min_app_version": "1.0.0"
    },
    "criollo": {
      "url": "s3://models/criollo-v1.2.0.tflite",
      "md5": "mno345...",
      "size_mb": 4.1,
      "min_app_version": "1.0.0"
    },
    "pardo_suizo": {
      "url": "s3://models/pardo-suizo-v1.2.0.tflite",
      "md5": "pqr678...",
      "size_mb": 4.6,
      "min_app_version": "1.0.0"
    },
    "jersey": {
      "url": "s3://models/jersey-v1.2.0.tflite",
      "md5": "stu901...",
      "size_mb": 4.0,
      "min_app_version": "1.0.0"
    }
  },
  "release_notes": "Mejora precisión en animales jóvenes para las 7 razas de la Hacienda Gamelera"
}
```

#### Flujo de Actualización

1. App verifica versión local vs manifest.json en S3
2. Si hay nueva versión, descarga en background
3. Valida integridad con MD5 checksum
4. Reemplaza modelo local después de validación exitosa
5. Notifica al usuario de nueva versión disponible

#### Consecuencias ADR-011

- **Positivas**: Mejora continua sin fricciones, soporte multi-raza, seguridad
- **Negativas**: Dependencia de S3, consumo de datos para descargas
- **Riesgos**: Modelos corruptos si falla validación

---

### ADR-012: Categorización por Edad de Bovinos

**Fecha**: 2024-01-15  
**Estado**: Aceptado  
**Decisor**: Equipo de Arquitectura  

#### Contexto ADR-012

El manejo ganadero en la Hacienda Gamelera requiere categorización específica por edad:

- Diferentes protocolos nutricionales según edad
- Dosificación de medicamentos varía por categoría
- Momentos críticos de crecimiento en cada etapa
- Requisitos SENASAG de registro por categoría
- Competencias ASOCEBU tienen categorías de edad

#### Opciones Consideradas ADR-012

1. **4 Categorías Específicas (según práctica ganadera)**
2. **Categorización Simple (ternero/adulto)**
3. **Categorización Continua (meses de edad)**
4. **Categorización por Peso (sin considerar edad)**

#### Decisión ADR-012

Se implementan **4 categorías específicas** basadas en la práctica ganadera:

1. **Terneros**: <8 meses
2. **Vaquillonas/Torillos**: 6-18 meses
3. **Vaquillonas/Toretes**: 19-30 meses
4. **Vacas/Toros**: >30 meses

#### Justificación ADR-012

- **Práctica establecida**: Estas son las categorías usadas en la Hacienda Gamelera
- **Momentos críticos**: Capturan etapas clave de desarrollo (destete, pubertad, madurez)
- **Dosificación médica**: Veterinarios dosifican según estas categorías
- **Nutrición**: Planes nutricionales específicos por categoría
- **Comercialización**: Mercado define precios por estas categorías
- **Competencias**: ASOCEBU usa categorías similares

#### Implementación ADR-012

- Cálculo automático basado en `birth_date`
- Campo `age_category_id` en entidad Animal
- Validación de peso esperado según categoría y raza
- Alertas cuando animal no alcanza peso esperado para su categoría

#### Consecuencias ADR-012

- **Positivas**: Alineación con práctica ganadera real, mejor dosificación médica
- **Negativas**: Complejidad adicional en modelo de datos
- **Riesgos**: Rangos de edad pueden variar según raza (se mitiga con configuración por raza)

---

### ADR-013: Integración con Normativa Boliviana (SENASAG/REGENSA)

**Fecha**: 2024-01-15  
**Estado**: Aceptado  
**Decisor**: Equipo de Arquitectura  

#### Contexto ADR-013

La ganadería en Bolivia está regulada por:

- **SENASAG**: Servicio Nacional de Sanidad Agropecuaria e Inocuidad Alimentaria
- **REGENSA**: Reglamento General de Sanidad Animal (capítulos 3.10 y 7.1)
- **Gran Paitití**: Sistema gubernamental de registro digital
- **GMA**: Guía de Movimiento Animal (requisito obligatorio)

**Requisitos específicos REGENSA (caps 3.10 y 7.1)**:

- Centros de concentración animal deben tener:
  - Rampas antideslizantes y pasillos de mínimo 1.6m
  - Al menos 2m² por animal en corrales
  - Sistemas de desinfección de vehículos
  - Corrales de cuarentena
  - Prohibición de instrumentos que provoquen dolor durante manejo

#### Opciones Consideradas ADR-013

1. **Integración Directa con APIs Gubernamentales**
2. **Exportación Manual (usuario descarga y sube)**
3. **Integración Híbrida (generación automática + envío manual)**
4. **No Integración (usuario maneja trámites por separado)**

#### Decisión ADR-013

Se implementa **Integración Híbrida**:

- **Generación automática** de reportes en formato SENASAG
- **Generación automática** de GMA con datos completos
- **Validación automática** de cumplimiento REGENSA (caps 3.10 y 7.1)
- **Envío manual** a Gran Paitití (usuario aprueba antes de enviar)

#### Justificación ADR-013

- **Cumplimiento obligatorio**: Sin estos reportes, no se puede mover ganado legalmente
- **Reducción de errores**: Generación automática elimina errores de transcripción
- **Trazabilidad**: Registro digital completo para auditorías
- **Flexibilidad**: Usuario revisa antes de enviar (seguridad)
- **Comercialización**: Requisito para venta y exportación
- **Competencias ASOCEBU**: Requieren certificaciones SENASAG

#### Implementación ADR-013

**Entidades nuevas**:

- `SENASAGReport`: Reportes generados
- `GMA`: Guías de Movimiento Animal
- Campos de cumplimiento en `Farm`

**Servicios nuevos**:

- `SENASAGReportGenerator`: Genera reportes en PDF/CSV/XML
- `GMAGenerator`: Genera GMA con validación REGENSA
- `REGENSAValidator`: Valida cumplimiento capítulos 3.10 y 7.1
- `GranPaititiConnector`: Interfaz para envío a plataforma gubernamental

**Formatos de exportación**:

- PDF: Para presentación y archivo
- CSV: Para análisis y procesamiento
- XML: Para integración con Gran Paitití

#### Consecuencias ADR-013

- **Positivas**: Cumplimiento normativo automático, ahorro de tiempo, reduce multas
- **Negativas**: Complejidad adicional, dependencia de formatos gubernamentales
- **Riesgos**: Cambios en formatos SENASAG requieren actualización del sistema

---

### ADR-014: Métricas de Precisión y Rendimiento del Sistema

**Fecha**: 2024-01-15  
**Estado**: Aceptado  
**Decisor**: Equipo de Arquitectura  

#### Contexto ADR-014

El marco SCRUM del proyecto define métricas específicas de éxito:

- **Precisión del modelo**: ≥95% de exactitud
- **Error absoluto promedio**: <5 kg por animal
- **R² (coeficiente de determinación)**: ≥0.95
- **Tiempo de procesamiento**: <3 segundos
- **Validación en campo**: 50 animales mínimo
- **Mejora vs método actual**: Fórmula Schaeffer tiene error de 5-20 kg

#### Opciones Consideradas ADR-014

1. **Métricas Estrictas** (≥95%, <5kg, <3s)
2. **Métricas Relajadas** (≥90%, <10kg, <5s)
3. **Métricas Progresivas** (empezar con 85%, aumentar gradualmente)
4. **Sin Métricas Específicas** (evaluar cualitativamente)

#### Decisión ADR-014

Se establecen **Métricas Estrictas** como criterio de aceptación:

- **Precisión**: ≥95% de exactitud
- **Error absoluto promedio**: <5 kg por animal
- **R²**: ≥0.95 (explica 95% de variabilidad)
- **RMSE**: <8 kg (Root Mean Square Error)
- **MAPE**: <3% (Mean Absolute Percentage Error)
- **Tiempo de procesamiento**: <3 segundos por estimación
- **Validación**: 50 animales en condiciones reales de campo

#### Justificación ADR-014

**Por qué 95% de precisión:**

- Fórmula Schaeffer actual: 5-20 kg de error (85-95% de precisión variable)
- Requisito para dosificación médica segura: máximo 5 kg error
- Competencias ASOCEBU requieren mediciones precisas
- Decisiones comerciales basadas en peso exacto

**Por qué <3 segundos:**

- Procesamiento de 20 animales en <2 horas requiere ~6 min/animal
- Usuario espera feedback inmediato (<5s es aceptable)
- Captura continua 3-5s + procesamiento 3s = <8s total
- Competitivo vs pesaje tradicional (5-10 min por animal)

**Por qué R² ≥ 0.95:**

- Estándar académico para modelos de estimación de peso bovino
- Weber et al. (2020) logró R²=0.98 en vacas lecheras
- Toledo (2025) logró R²=0.99 con YOLOv8
- 0.95 es alcanzable y suficiente para aplicación práctica

**Por qué 50 animales en validación:**

- Representatividad estadística mínima
- Cobertura de 7 razas y 4 categorías de edad
- Condiciones variables de campo (iluminación, terreno, clima)
- Factible en Hacienda Gamelera (500 cabezas)

#### Consecuencias ADR-014

- **Positivas**: Criterios claros de aceptación, confianza del usuario, calidad garantizada
- **Negativas**: Requiere dataset de entrenamiento robusto, validación exhaustiva
- **Riesgos**: Algunas razas o categorías pueden no alcanzar 95% inicialmente

---

### Resumen de Decisiones

| Decisión | Tecnología | Justificación Principal |
|----------|------------|------------------------|
| Framework Móvil | Flutter | Rendimiento y desarrollo cross-platform |
| Arquitectura | Clean Architecture | Separación de responsabilidades y testabilidad |
| Base de Datos | MongoDB | Flexibilidad y escalabilidad |
| ML Local | TensorFlow Lite | Funcionamiento offline |
| Estado | Provider | Simplicidad y rendimiento |
| Backend | FastAPI | Rendimiento y desarrollo rápido |
| Diseño | Atomic Design | Reutilización y consistencia |
| Storage | AWS S3 | Escalabilidad y durabilidad |
| Offline-First | SQLite + Sync | Funcionamiento en campo rural |
| Captura | Continua + Tiempo Real | Automatización y calidad |
| Modelos ML | Versionado S3 | Actualización sin fricciones |
| Categorías Edad | 4 Categorías Específicas | Alineación con práctica ganadera |
| Normativa | Integración Híbrida | Cumplimiento SENASAG/REGENSA |
| Métricas | Estrictas (≥95%, <3s) | Calidad garantizada |

### Próximas Decisiones Pendientes

1. **Autenticación y Seguridad**:
   - JWT local vs OAuth2 vs Biometría
   - Gestión de sesiones offline
   - Encriptación de SQLite
   - Roles: Admin (Bruno Brito) vs Empleados

2. **Sistema de Notificaciones**:
   - Push notifications (Firebase Cloud Messaging)
   - Notificaciones locales para alertas offline
   - Estrategia de priorización
   - Alertas SENASAG/REGENSA (vencimiento GMA, inspecciones)

3. **Validación del Modelo con 50 Animales**:
   - Protocolo de validación en campo
   - Selección de animales (distribución por raza y edad)
   - Métricas a registrar por animal
   - Comparación con peso real en báscula

4. **Estrategia de Testing**:
   - Unit tests (coverage mínimo 80%)
   - Integration tests para sincronización y normativa
   - E2E tests para flujos críticos (captura, estimación, GMA)
   - Testing de modelos ML por cada una de las 7 razas

5. **CI/CD Pipeline**:
   - GitHub Actions vs AWS CodePipeline
   - Despliegue a TestFlight/Play Console
   - Automatización de deploy de 7 modelos ML a S3
   - Validación automática de métricas (≥95%, <3s)

6. **Monitoreo y Observabilidad**:
   - Logging: CloudWatch vs ELK Stack
   - Métricas: Precisión real por raza y categoría de edad
   - Error tracking: Sentry vs Crashlytics
   - Dashboard para Bruno Brito Macedo

7. **Gestión de Almacenamiento Local**:
   - Límites: Modelos (7×4MB=28MB), Imágenes, DB SQLite
   - Estrategia de limpieza automática
   - Compresión de imágenes antiguas
   - Migración a almacenamiento externo

8. **Preparación para Competencias ASOCEBU**:
   - Exportación de datos históricos
   - Reportes de rendimiento por categoría
   - Certificaciones de peso
   - Integración con sistema ASOCEBU

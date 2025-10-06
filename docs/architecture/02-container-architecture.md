# 02. Arquitectura de Contenedores

## Contexto Específico del Proyecto

**Ubicación**: Hacienda Gamelera (15°51′34.2′′S, 60°47′52.4′′W)  
**Área**: 48.5 hectáreas en San Ignacio de Velasco, Santa Cruz, Bolivia  
**Hato**: 500 cabezas de ganado bovino

Este sistema reemplaza el método de pesaje tradicional que utiliza:

- Básculas mecánicas y cinta bovinométrica
- Fórmula de Schaeffer: Peso (kg) = (PT² × LC) / 10838
- Error actual: 5-20 kg por animal
- Tiempo actual: 2-3 días para 20 animales

**Objetivo**: Reducir a <2 horas con precisión >95% (error <5 kg)

**Razas soportadas**: Brahman, Nelore, Angus, Cebuinas (Bos indicus), Criollo (Bos taurus), Pardo Suizo, Jersey

**Stakeholders**: Bruno Brito Macedo (propietario), SENASAG, REGENSA, ASOCEBU

## Diagrama C4 Nivel 2 - Contenedores del Sistema

### Descripción de la Arquitectura

El sistema está compuesto por 5 contenedores principales que trabajan en conjunto para proporcionar la funcionalidad de estimación de peso bovino con IA, optimizado para operación rural en Bolivia.

### Contenedores del Sistema

#### 1. App Flutter (Mobile Application)

- **Tecnología**: Flutter/Dart
- **Responsabilidades**:
  - **Captura CONTINUA de fotogramas** (no fotos individuales)
  - **Evaluación en tiempo real** de calidad de fotogramas
  - **Selección automática** del mejor fotograma
  - **Procesamiento según raza específica** del animal
  - Gestión de datos locales con SQLite (offline-first)
  - Ejecución de modelos TFLite por raza
  - Sincronización inteligente con resolución de conflictos
  - Funcionalidad completa sin conexión a internet
- **Características**:
  - Arquitectura Clean Architecture
  - Patrón Provider para gestión de estado
  - Atomic Design para componentes UI
  - Almacenamiento local con SQLite
  - **Estrategia Offline-First**

#### Estrategia Offline-First

- **SQLite como fuente de verdad local**
- **Operación completa sin conectividad**
- **Queue de sincronización con retry automático**
- **Resolución de conflictos**: last-write-wins con timestamps
- **Indicador visual de estado de sincronización**

#### 2. Backend API (FastAPI)

- **Tecnología**: Python FastAPI
- **Responsabilidades**:
  - API REST para gestión de datos
  - Autenticación y autorización
  - Procesamiento de imágenes
  - **Gestión de modelos ML por raza**
  - Sincronización de datos
  - Generación de reportes
  - **Versionado y distribución de modelos**
- **Características**:
  - Arquitectura por capas (Routes, Services, Models)
  - Validación de datos con Pydantic
  - Documentación automática con OpenAPI
  - Logging estructurado
- **Comunicación**:
  - HTTPS con App Flutter
  - MongoDB para persistencia
  - S3 para almacenamiento de archivos

#### 3. MongoDB (Database)

- **Tecnología**: MongoDB
- **Responsabilidades**:
  - Almacenamiento de datos de animales
  - Persistencia de pesajes e historial
  - Gestión de usuarios y configuraciones
  - **Almacenamiento de metadatos de sesiones de captura**
  - **Registros de calidad de fotogramas**
  - Índices para consultas optimizadas
- **Características**:
  - Esquema flexible para datos variables
  - Replicación para alta disponibilidad
  - Sharding para escalabilidad
  - Agregaciones para reportes
- **Comunicación**:
  - TCP/IP con Backend API
  - Autenticación con credenciales

#### 4. TFLite (Machine Learning Engine)

- **Tecnología**: TensorFlow Lite
- **Responsabilidades**:
  - **Ejecución de modelos específicos por raza**:
    - Brahman, Nelore, Angus, Cebuinas, Criollo, Pardo Suizo, Jersey
  - **Procesamiento por categoría de edad**:
    - Terneros (<8 meses)
    - Vaquillonas/Torillos (6-18 meses)
    - Vaquillonas/Toretes (19-30 meses)
    - Vacas/Toros (>30 meses)
  - **Métricas de rendimiento**:
    - Precisión objetivo: ≥95% (R² ≥ 0.95)
    - Error absoluto: <5 kg
    - Tiempo procesamiento: <3 segundos
  - Estimación de peso a partir de fotogramas seleccionados
  - **Procesamiento de imágenes (preprocessing)**
  - Optimización de rendimiento en móvil
  - Gestión de memoria eficiente
  - **Carga dinámica de modelos actualizados**
- **Características**:
  - **Modelos optimizados por raza bovina**
  - Procesamiento en tiempo real
  - Bajo consumo de recursos
  - Soporte para GPU (opcional)
- **Comunicación**:
  - Local con App Flutter
  - Descarga de modelos desde S3

#### 5. AWS S3 (Cloud Storage)

- **Tecnología**: Amazon S3
- **Responsabilidades**:
  - **Almacenamiento de modelos ML versionados**
  - **Distribución de manifest.json con versiones**
  - Almacenamiento de imágenes originales
  - Backup de datos críticos
  - CDN para descarga rápida
  - **Gestión de versiones de modelos por raza**
- **Características**:
  - Almacenamiento escalable
  - Redundancia geográfica
  - Políticas de retención
  - Encriptación en reposo
- **Comunicación**:
  - HTTPS con App Flutter y Backend API
  - Autenticación con IAM

### Especificaciones Técnicas de Captura Continua

#### Parámetros de Captura

- **FPS**: 10-15 fotogramas por segundo
- **Duración**: 3-5 segundos de captura continua
- **Total fotogramas**: 30-75 fotogramas por sesión
- **Almacenamiento temporal**: ~5-10 MB por sesión

#### Criterios de Evaluación en Tiempo Real

- **Nitidez** (sharpness): >0.7 (escala 0-1)
- **Iluminación** (brightness): 0.4-0.8 (escala 0-1)
- **Contraste** (contrast): >0.5 (escala 0-1)
- **Visibilidad de silueta**: >0.8 (escala 0-1)
- **Ángulo apropiado**: >0.6 (escala 0-1)
- **Score global**: Promedio ponderado de todos los criterios

#### Selección del Mejor Fotograma

- **Algoritmo**: Score global ponderado
- **Pesos**: Silueta (40%), Nitidez (30%), Iluminación (20%), Ángulo (10%)
- **Umbral mínimo**: Score global >0.65 para aceptación

### Protocolos de Comunicación

#### HTTPS (App Flutter ↔ Backend API)

- **Propósito**: Comunicación segura de datos
- **Datos transmitidos**:
  - Datos de animales (JSON)
  - **Metadatos de sesiones de captura**
  - **Resultados de sincronización**
  - Configuraciones de usuario
  - Reportes y análisis
- **Seguridad**: TLS 1.3, autenticación JWT
- **Frecuencia**: Sincronización periódica y bajo demanda

#### TCP/IP (Backend API ↔ MongoDB)

- **Propósito**: Persistencia de datos
- **Datos transmitidos**:
  - Documentos JSON
  - **Consultas de agregación para reportes**
  - Índices y configuraciones
- **Seguridad**: Autenticación con credenciales
- **Frecuencia**: Continuo según operaciones

#### HTTPS (App Flutter ↔ S3)

- **Propósito**: **Descarga de modelos y archivos**
- **Datos transmitidos**:
  - **Modelos TFLite por raza**
  - **Manifest.json con versiones**
  - Imágenes de respaldo
  - Configuraciones globales
- **Seguridad**: IAM roles y políticas
- **Frecuencia**: Bajo demanda y actualizaciones

#### Local IPC (App Flutter ↔ TFLite)

- **Propósito**: Ejecución de inferencia local
- **Datos transmitidos**:
  - **Fotogramas seleccionados**
  - **Parámetros de raza específica**
  - Resultados de inferencia
  - Configuraciones del modelo
- **Seguridad**: Memoria compartida local
- **Frecuencia**: Tiempo real durante captura

### Flujos de Datos Principales

#### 1. Estimación de Peso

```text
Ganadero → App Flutter (captura continua) → 
Evaluación en tiempo real de fotogramas → 
Selección del mejor fotograma → 
TFLite (modelo según raza) → 
Resultado → 
SQLite (local) → 
[cuando hay conexión] Backend API → MongoDB
```

#### 2. Sincronización de Datos

```text
App Flutter (SQLite) ↔ Backend API ↔ MongoDB
```

#### 3. Descarga de Modelos

```text
S3 → App Flutter → TFLite (almacenamiento local)
```

#### 4. Backup de Imágenes

```text
App Flutter → Backend API → S3
```

#### 5. Descarga y Versionado de Modelos

```text
Backend API → S3 (manifest.json con versiones) → 
App Flutter (verifica versión local) → 
[si hay nueva versión] Descarga modelo → 
Validación de integridad → 
Almacenamiento local → 
TFLite carga nuevo modelo
```

### Consideraciones de Seguridad

#### Autenticación y Autorización

- JWT tokens para API
- IAM roles para S3
- Credenciales MongoDB
- **Biometría opcional en móvil**

#### Encriptación

- TLS 1.3 en tránsito
- AES-256 en reposo (S3, MongoDB)
- **Encriptación local (SQLite)**

#### Privacidad de Datos

- **Anonimización de imágenes**
- Políticas de retención
- **Cumplimiento normativa boliviana**
- Auditoría de accesos

### Escalabilidad y Rendimiento

#### App Flutter

- **Caché inteligente de datos**
- **Procesamiento asíncrono de fotogramas**
- **Optimización de memoria para captura continua**
- **Lazy loading de componentes**

#### Backend API

- Load balancing horizontal
- **Caché Redis (futuro)**
- Connection pooling
- **Async processing para ML**

#### MongoDB

- **Sharding por región**
- Índices optimizados
- Replicación read-only
- **Agregaciones eficientes para reportes**

#### S3

- **CDN CloudFront**
- **Compresión de archivos**
- Políticas de lifecycle
- **Multipart uploads para modelos grandes**

### Consideraciones Específicas para Bolivia

#### Conectividad Rural

- **Funcionamiento offline-first**
- **Sincronización cuando hay señal**
- **Compresión de datos para ahorro**
- **Retry automático con backoff**

#### Integración con Normativa Boliviana

**SENASAG**:

- Exportación automática de reportes de inventario
- Certificados de trazabilidad ganadera
- Formato: PDF, CSV, XML según estándar SENASAG

**REGENSA (Capítulos 3.10 y 7.1)**:

- Integración con Sistema Gran Paitití
- Generación automática de GMA (Guía de Movimiento Animal)
- Registro digital de todos los pesajes con timestamp y ubicación GPS
- Cumplimiento de requisitos de centros de concentración animal

**ASOCEBU**:

- Exportación de datos para competencias ganaderas
- Reportes de rendimiento por categoría
- Historial de crecimiento para certificaciones

#### Condiciones de Campo

- **Resistencia a condiciones climáticas**
- **Optimización para batería**
- **Interfaz simple para usuarios rurales**
- **Funcionamiento con guantes**

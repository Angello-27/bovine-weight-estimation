# Estándares de Despliegue y DevOps

## Contexto del Proyecto

**Proyecto**: Sistema de Estimación de Peso Bovino con IA  
**Cliente**: Hacienda Gamelera (Bruno Brito Macedo)  
**Infraestructura**: Docker + AWS (S3, EC2) + MongoDB Atlas  
**Ambientes**: Development, Staging, Production

## Principios Fundamentales DevOps

1. **Infrastructure as Code**: Docker Compose, configuraciones versionadas
2. **CI/CD Automatizado**: GitHub Actions para tests y deploy
3. **Monitoreo Continuo**: Métricas de performance y disponibilidad
4. **Backups Automáticos**: Diarios incrementales a S3
5. **Zero Downtime**: Deployments sin interrupciones

---

## Arquitectura de Infraestructura

### Stack Tecnológico

| Componente | Tecnología | Propósito |
|------------|------------|-----------|
| **Contenedores** | Docker + Docker Compose | Orquestación local y producción |
| **Cloud Storage** | AWS S3 / MinIO | Modelos TFLite, backups, logs |
| **Base de datos** | MongoDB Atlas | Producción cloud |
| **CI/CD** | GitHub Actions | Tests, lint, deploy automático |
| **Reverse Proxy** | NGINX | HTTPS, SSL/TLS |
| **SSL Certificates** | Let's Encrypt / Certbot | HTTPS automático |
| **Monitoreo** | Prometheus + Grafana | Métricas backend y ML |
| **Logs** | Loguru + ELK Stack | Logs estructurados centralizados |
| **Backups** | rclone + cron | Copias automáticas a S3 |

---

## Docker Compose (Local Development)

```yaml
# docker-compose.yml

version: '3.9'

services:
  # Backend FastAPI
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: bovine-backend
    ports:
      - "8000:8000"
    env_file:
      - ./backend/.env
    environment:
      - MONGODB_URL=mongodb://mongodb:27017
      - MONGODB_DB_NAME=bovine_weight_estimation
      - AWS_S3_ENDPOINT_URL=http://minio:9000  # MinIO local
    volumes:
      - ./backend:/app
      - ./models:/app/models:ro  # Modelos TFLite (read-only)
    depends_on:
      - mongodb
      - minio
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    networks:
      - bovine-network
  
  # MongoDB
  mongodb:
    image: mongo:7.0
    container_name: bovine-mongodb
    ports:
      - "27017:27017"
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=admin123
      - MONGO_INITDB_DATABASE=bovine_weight_estimation
    volumes:
      - mongodb_data:/data/db
      - ./backend/app/database/seed_data.js:/docker-entrypoint-initdb.d/seed.js:ro
    networks:
      - bovine-network
  
  # MinIO (S3-compatible storage local)
  minio:
    image: minio/minio:latest
    container_name: bovine-minio
    ports:
      - "9000:9000"      # API
      - "9001:9001"      # Console
    environment:
      - MINIO_ROOT_USER=minioadmin
      - MINIO_ROOT_PASSWORD=minioadmin
    volumes:
      - minio_data:/data
    command: server /data --console-address ":9001"
    networks:
      - bovine-network
  
  # MLflow (tracking experimentos ML)
  mlflow:
    build:
      context: ./ml-training
      dockerfile: Dockerfile.mlflow
    container_name: bovine-mlflow
    ports:
      - "5000:5000"
    environment:
      - MLFLOW_BACKEND_STORE_URI=sqlite:///mlflow.db
      - MLFLOW_ARTIFACT_ROOT=/mlflow/artifacts
    volumes:
      - mlflow_data:/mlflow
      - ./models:/mlflow/models:ro
    command: mlflow server --host 0.0.0.0 --port 5000
    networks:
      - bovine-network

volumes:
  mongodb_data:
  minio_data:
  mlflow_data:

networks:
  bovine-network:
    driver: bridge
```

### Dockerfile Backend

```dockerfile
# backend/Dockerfile

FROM python:3.11-slim

LABEL maintainer="Hacienda Gamelera <dev@haciendagamelera.com>"
LABEL description="Backend API - Sistema Estimación Peso Bovino IA"
LABEL version="1.0.0"

# Working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Crear usuario no-root para seguridad
RUN useradd -m -u 1000 bovine && \
    chown -R bovine:bovine /app

USER bovine

# Exponer puerto
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Comando por defecto
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Ambientes

### 1. Development (Local)

```env
# backend/.env.development

APP_NAME=Sistema Estimación Peso Bovino IA (Dev)
APP_VERSION=1.0.0
DEBUG=True

# MongoDB local
MONGODB_URL=mongodb://admin:admin123@localhost:27017
MONGODB_DB_NAME=bovine_weight_estimation_dev

# JWT
JWT_SECRET_KEY=dev-secret-key-change-in-production
JWT_ALGORITHM=HS256

# MinIO local (S3-compatible)
AWS_S3_ENDPOINT_URL=http://localhost:9000
AWS_ACCESS_KEY_ID=minioadmin
AWS_SECRET_ACCESS_KEY=minioadmin
AWS_S3_BUCKET_NAME=bovine-ml-models-dev

# Gran Paitití (sandbox)
GRAN_PAITITI_API_URL=https://sandbox.granpaititi.gob.bo/api/v1
GRAN_PAITITI_API_KEY=sandbox-key

# SMTP (Mailtrap para desarrollo)
SMTP_HOST=smtp.mailtrap.io
SMTP_PORT=2525
SMTP_USER=your-mailtrap-user
SMTP_PASSWORD=your-mailtrap-password

# Logs
LOG_LEVEL=DEBUG
```

### 2. Staging (Pre-producción)

```env
# backend/.env.staging

APP_NAME=Sistema Estimación Peso Bovino IA (Staging)
APP_VERSION=1.0.0
DEBUG=False

# MongoDB Atlas (cluster staging)
MONGODB_URL=mongodb+srv://staging:PASSWORD@cluster-staging.mongodb.net/
MONGODB_DB_NAME=bovine_weight_estimation_staging

# JWT (generar nuevo)
JWT_SECRET_KEY=staging-secret-key-secure-random-string
JWT_ALGORITHM=HS256

# AWS S3 (bucket staging)
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_S3_BUCKET_NAME=bovine-ml-models-staging
AWS_REGION=us-east-1

# Gran Paitití (sandbox)
GRAN_PAITITI_API_URL=https://sandbox.granpaititi.gob.bo/api/v1
GRAN_PAITITI_API_KEY=staging-api-key

# SMTP (real, limitado)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=noreply@haciendagamelera.com
SMTP_PASSWORD=app-specific-password

# Logs
LOG_LEVEL=INFO
```

### 3. Production (Hacienda Gamelera)

```env
# backend/.env.production

APP_NAME=Sistema Estimación Peso Bovino IA
APP_VERSION=1.0.0
DEBUG=False

# MongoDB Atlas (cluster producción)
MONGODB_URL=mongodb+srv://prod:SECURE_PASSWORD@cluster-prod.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=bovine_weight_estimation

# JWT (secreto fuerte, rotado mensualmente)
JWT_SECRET_KEY=production-super-secret-key-64-chars-minimum-rotated-monthly
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60

# AWS S3 (producción)
AWS_ACCESS_KEY_ID=PROD_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=PROD_SECRET_KEY
AWS_S3_BUCKET_NAME=bovine-ml-models-production
AWS_REGION=us-east-1

# Gran Paitití (producción)
GRAN_PAITITI_API_URL=https://granpaititi.gob.bo/api/v1
GRAN_PAITITI_API_KEY=production-api-key-hacienda-gamelera

# SMTP (producción)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=sistema@haciendagamelera.com
SMTP_PASSWORD=secure-app-password

# Logs
LOG_LEVEL=WARNING

# Monitoreo
SENTRY_DSN=https://public@sentry.io/project-id

# Backups
BACKUP_SCHEDULE=0 2 * * *  # 2 AM diario
BACKUP_S3_BUCKET=bovine-backups-production
```

---

## CI/CD Pipeline Completo

```yaml
# .github/workflows/ci-cd.yml

name: CI/CD Pipeline

on:
  push:
    branches: [ development, main ]
    tags: [ 'v*' ]
  pull_request:
    branches: [ development, main ]

env:
  FLUTTER_VERSION: '3.16.0'
  PYTHON_VERSION: '3.11'

jobs:
  # ==========================================
  # LINT
  # ==========================================
  
  lint-backend:
    name: Lint Backend (Python)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Install linters
        run: |
          cd backend
          pip install ruff black isort mypy
      
      - name: Run ruff
        run: cd backend && ruff check app/
      
      - name: Run black
        run: cd backend && black --check app/
      
      - name: Run isort
        run: cd backend && isort --check-only app/
      
      - name: Run mypy
        run: cd backend && mypy app/
  
  lint-mobile:
    name: Lint Mobile (Flutter)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: ${{ env.FLUTTER_VERSION }}
      
      - name: Install dependencies
        run: cd mobile && flutter pub get
      
      - name: Run analyzer
        run: cd mobile && flutter analyze
      
      - name: Run dart format
        run: cd mobile && dart format --set-exit-if-changed .
  
  # ==========================================
  # TESTS
  # ==========================================
  
  test-backend:
    name: Tests Backend
    runs-on: ubuntu-latest
    needs: [lint-backend]
    
    services:
      mongodb:
        image: mongo:7.0
        ports:
          - 27017:27017
        env:
          MONGO_INITDB_ROOT_USERNAME: test
          MONGO_INITDB_ROOT_PASSWORD: test
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Run unit tests
        run: |
          cd backend
          pytest tests/unit --cov=app --cov-report=xml --cov-report=term-missing
      
      - name: Run integration tests
        env:
          MONGODB_URL: mongodb://test:test@localhost:27017
        run: |
          cd backend
          pytest tests/integration --cov=app --cov-append --cov-report=xml
      
      - name: Check coverage >80%
        run: |
          cd backend
          pytest --cov=app --cov-fail-under=80
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml
          flags: backend
  
  test-mobile:
    name: Tests Mobile
    runs-on: ubuntu-latest
    needs: [lint-mobile]
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: ${{ env.FLUTTER_VERSION }}
      
      - name: Install dependencies
        run: cd mobile && flutter pub get
      
      - name: Run tests
        run: cd mobile && flutter test --coverage
      
      - name: Check coverage >80%
        run: |
          cd mobile
          lcov --summary coverage/lcov.info
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./mobile/coverage/lcov.info
          flags: mobile
  
  # ==========================================
  # BUILD
  # ==========================================
  
  build-mobile-android:
    name: Build Mobile (Android APK)
    runs-on: ubuntu-latest
    needs: [test-mobile]
    if: github.ref == 'refs/heads/main' || startsWith(github.ref, 'refs/tags/v')
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-java@v3
        with:
          distribution: 'zulu'
          java-version: '17'
      
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: ${{ env.FLUTTER_VERSION }}
      
      - name: Install dependencies
        run: cd mobile && flutter pub get
      
      - name: Build APK
        run: cd mobile && flutter build apk --release
      
      - name: Upload APK artifact
        uses: actions/upload-artifact@v3
        with:
          name: bovine-weight-app-${{ github.sha }}.apk
          path: mobile/build/app/outputs/flutter-apk/app-release.apk
  
  build-backend-image:
    name: Build Backend Docker Image
    runs-on: ubuntu-latest
    needs: [test-backend]
    if: github.ref == 'refs/heads/main' || startsWith(github.ref, 'refs/tags/v')
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: haciendagamelera/bovine-backend
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
  
  # ==========================================
  # DEPLOY
  # ==========================================
  
  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: [build-mobile-android, build-backend-image]
    if: startsWith(github.ref, 'refs/tags/v')
    environment: production
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy backend to AWS EC2
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ${{ secrets.EC2_USER }}
          key: ${{ secrets.EC2_SSH_KEY }}
          script: |
            cd /opt/bovine-weight-estimation
            docker-compose pull backend
            docker-compose up -d backend
            docker system prune -f
      
      - name: Upload APK to S3
        run: |
          aws s3 cp \
            mobile/build/app/outputs/flutter-apk/app-release.apk \
            s3://bovine-releases/${{ github.ref_name }}/bovine-weight-app-${{ github.ref_name }}.apk
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      
      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          files: mobile/build/app/outputs/flutter-apk/app-release.apk
          body: |
            ## Sistema de Estimación de Peso Bovino con IA v${{ github.ref_name }}
            
            **Cliente**: Hacienda Gamelera (Bruno Brito Macedo)
            **Ubicación**: San Ignacio de Velasco, Bolivia
            
            ### Cambios principales
            - Ver CHANGELOG.md para detalles completos
            
            ### Instalación
            1. Descargar bovine-weight-app-${{ github.ref_name }}.apk
            2. Instalar en dispositivo Android
            3. Permitir instalación de fuentes desconocidas
            4. Abrir app y login con credenciales
            
            ### Validación
            - ✅ Precisión >95% validada en campo
            - ✅ Cumplimiento normativo SENASAG/REGENSA/ASOCEBU
            - ✅ Funcionamiento offline 100%
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## Deployment Checklist

### Pre-deployment

```markdown
## Checklist Pre-deployment a Producción

### Código y Tests
- [ ] Todos los tests pasando (backend + mobile)
- [ ] Coverage >80% en backend y mobile
- [ ] Linting sin errores (ruff, black, flutter analyze)
- [ ] Code reviews aprobados
- [ ] Branch main actualizado con development

### Base de Datos
- [ ] Migraciones ejecutadas en staging
- [ ] Seed data de las 7 razas bovinas cargado
- [ ] Índices optimizados creados
- [ ] Backup reciente disponible (<24 horas)

### Modelos ML
- [ ] 7 modelos TFLite subidos a S3 production
- [ ] manifest.json actualizado con versiones correctas
- [ ] Métricas validadas: R² ≥0.95, MAE <5kg para cada raza
- [ ] Checksum MD5 verificado

### Configuración
- [ ] Variables de entorno de producción configuradas
- [ ] Secretos en AWS Secrets Manager / GitHub Secrets
- [ ] JWT secret key rotado
- [ ] CORS origins configurados correctamente
- [ ] Gran Paitití API credentials de producción

### Seguridad
- [ ] SSL/TLS certificado instalado (Let's Encrypt)
- [ ] NGINX reverse proxy configurado
- [ ] Firewall rules configuradas (solo 80, 443, 22)
- [ ] Backups automáticos configurados (cron)
- [ ] Logs rotación configurada

### Monitoreo
- [ ] Prometheus scraping configurado
- [ ] Grafana dashboards creados
- [ ] Alertas configuradas (Slack/Email)
- [ ] Health checks funcionando
- [ ] Uptime monitoring configurado

### Documentación
- [ ] README.md actualizado con guías de instalación
- [ ] CHANGELOG.md actualizado con cambios del release
- [ ] Guías de usuario para Bruno Brito Macedo
- [ ] Runbook de operaciones documentado
```

### Post-deployment

```markdown
## Checklist Post-deployment

### Validación Técnica (primeros 5 minutos)
- [ ] Health check pasando: GET /api/v1/health
- [ ] Swagger docs accesibles: /docs
- [ ] Login funciona con credenciales de producción
- [ ] Endpoint animales retorna datos: GET /api/v1/animals

### Smoke Tests (primeros 30 minutos)
- [ ] Crear animal de cada una de las 7 razas
- [ ] Estimar peso de animal (verificar confidence >95%)
- [ ] Generar reporte SENASAG PDF
- [ ] Crear GMA digital
- [ ] Exportar datos ASOCEBU

### Validación con Bruno (primeras 24 horas)
- [ ] Bruno puede login en app móvil
- [ ] Bruno puede ver sus 500 animales
- [ ] Bruno puede capturar y estimar peso
- [ ] Sistema funciona offline en Hacienda Gamelera
- [ ] Sincronización funciona al recuperar conexión

### Monitoreo (primera semana)
- [ ] CPU usage <70% promedio
- [ ] Memoria usage <80% promedio
- [ ] Latencia API p95 <500ms
- [ ] Tasa de error <1%
- [ ] Uptime >99.5%
- [ ] No errores críticos en logs
```

---

## Monitoreo con Prometheus + Grafana

### Métricas a Monitorear

```python
# app/core/monitoring.py

from prometheus_client import Counter, Histogram, Gauge, Info
import time

# Métricas de negocio (específicas Hacienda Gamelera)

weighing_estimations_total = Counter(
    'weighing_estimations_total',
    'Total de estimaciones de peso realizadas',
    ['breed_type', 'hacienda'],
)

weighing_estimation_precision = Histogram(
    'weighing_estimation_confidence',
    'Confidence score de estimaciones (debe ser ≥0.95)',
    ['breed_type'],
    buckets=[0.8, 0.85, 0.9, 0.95, 0.97, 0.99, 1.0],
)

weighing_estimation_duration_seconds = Histogram(
    'weighing_estimation_duration_seconds',
    'Tiempo de procesamiento de estimación (objetivo: <3s)',
    ['breed_type'],
    buckets=[0.5, 1.0, 2.0, 3.0, 5.0, 10.0],
)

weighing_estimation_error_kg = Histogram(
    'weighing_estimation_error_kg',
    'Error absoluto de estimación (objetivo: <5 kg)',
    ['breed_type'],
    buckets=[1.0, 2.0, 3.0, 5.0, 10.0, 20.0],
)

# Métricas de sistema

active_animals_gauge = Gauge(
    'active_animals_total',
    'Total de animales activos en sistema',
    ['hacienda', 'breed_type'],
)

senasag_reports_generated_total = Counter(
    'senasag_reports_generated_total',
    'Total de reportes SENASAG generados',
    ['format', 'hacienda'],
)

# Uso en código

async def estimate_weight(...):
    start_time = time.time()
    
    result = await ml_service.estimate(...)
    
    # Registrar métricas
    weighing_estimations_total.labels(
        breed_type=breed_type.value,
        hacienda="hacienda_gamelera",
    ).inc()
    
    weighing_estimation_precision.labels(
        breed_type=breed_type.value,
    ).observe(result.confidence)
    
    duration = time.time() - start_time
    weighing_estimation_duration_seconds.labels(
        breed_type=breed_type.value,
    ).observe(duration)
    
    return result
```

### Dashboard Grafana

```json
{
  "dashboard": {
    "title": "Sistema Peso Bovino - Hacienda Gamelera",
    "panels": [
      {
        "title": "Estimaciones por Raza (Últimas 24h)",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(weighing_estimations_total{hacienda='hacienda_gamelera'}[24h])) by (breed_type)"
          }
        ]
      },
      {
        "title": "Precisión Promedio por Raza (debe ser ≥95%)",
        "type": "gauge",
        "targets": [
          {
            "expr": "avg(weighing_estimation_confidence) by (breed_type)"
          }
        ],
        "thresholds": [
          { "value": 0.95, "color": "green" },
          { "value": 0.90, "color": "yellow" },
          { "value": 0.0, "color": "red" }
        ]
      },
      {
        "title": "Tiempo de Procesamiento p95 (objetivo: <3s)",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, weighing_estimation_duration_seconds_bucket)"
          }
        ]
      },
      {
        "title": "Animales Activos por Raza",
        "type": "pie",
        "targets": [
          {
            "expr": "sum(active_animals_gauge{hacienda='hacienda_gamelera'}) by (breed_type)"
          }
        ]
      }
    ]
  }
}
```

---

## Backups Automáticos

### Script de Backup

```bash
#!/bin/bash
# scripts/backup.sh - Backup diario automático a S3

set -e

echo "==========================================
"
echo "BACKUP DIARIO - HACIENDA GAMELERA"
echo "Fecha: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="

# Variables
BACKUP_DATE=$(date '+%Y%m%d_%H%M%S')
BACKUP_DIR="/tmp/bovine-backups"
S3_BUCKET="s3://bovine-backups-production/hacienda-gamelera"

# Crear directorio temporal
mkdir -p "$BACKUP_DIR"

# 1. Backup MongoDB
echo "\n1. Backing up MongoDB..."
docker exec bovine-mongodb mongodump \
  --out "$BACKUP_DIR/mongodb-$BACKUP_DATE" \
  --db bovine_weight_estimation \
  --gzip

# 2. Backup archivos locales (SQLite de app móvil si existe)
echo "\n2. Backing up local files..."
tar -czf "$BACKUP_DIR/files-$BACKUP_DATE.tar.gz" \
  backend/.env \
  models/manifest.json \
  logs/

# 3. Subir a S3
echo "\n3. Uploading to S3..."
rclone sync "$BACKUP_DIR" "$S3_BUCKET/daily/$BACKUP_DATE" \
  --progress \
  --transfers 4 \
  --checkers 8

# 4. Cleanup (mantener solo últimos 7 días localmente)
echo "\n4. Cleanup old backups..."
find "$BACKUP_DIR" -name "mongodb-*" -mtime +7 -exec rm -rf {} \;
find "$BACKUP_DIR" -name "files-*.tar.gz" -mtime +7 -exec rm -f {} \;

# 5. Verificar backup
echo "\n5. Verifying backup..."
rclone ls "$S3_BUCKET/daily/$BACKUP_DATE" | grep "mongodb-$BACKUP_DATE"

echo "\n=========================================="
echo "✅ BACKUP COMPLETADO"
echo "Ubicación: $S3_BUCKET/daily/$BACKUP_DATE"
echo "=========================================="
```

### Cron Job

```cron
# crontab -e

# Backup diario a las 2 AM (hora Bolivia UTC-4)
0 2 * * * /opt/bovine-weight-estimation/scripts/backup.sh >> /var/log/bovine-backup.log 2>&1

# Sincronización modelos ML desde S3 cada 6 horas
0 */6 * * * /opt/bovine-weight-estimation/scripts/sync-ml-models.sh >> /var/log/bovine-sync.log 2>&1
```

---

## NGINX Configuration

```nginx
# /etc/nginx/sites-available/bovine-api

upstream backend_servers {
    server localhost:8000;
}

server {
    listen 80;
    server_name api.haciendagamelera.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.haciendagamelera.com;
    
    # SSL Configuration (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/api.haciendagamelera.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.haciendagamelera.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Headers de seguridad
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Client max body size (para uploads de imágenes)
    client_max_body_size 50M;
    
    # Proxy a backend FastAPI
    location / {
        proxy_pass http://backend_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Health check
    location /health {
        access_log off;
        proxy_pass http://backend_servers/api/v1/health;
    }
    
    # Logs
    access_log /var/log/nginx/bovine-api-access.log;
    error_log /var/log/nginx/bovine-api-error.log;
}
```

---

## Deployment Steps (Manual)

### Deploy Backend a AWS EC2

```bash
# 1. Conectar a servidor
ssh -i ~/.ssh/hacienda-gamelera.pem ubuntu@ec2-xxx-xxx-xxx-xxx.compute-1.amazonaws.com

# 2. Actualizar código
cd /opt/bovine-weight-estimation
git fetch origin
git checkout tags/v1.0.0

# 3. Actualizar variables de entorno
cp .env.production .env
nano .env  # Verificar credenciales

# 4. Build y deploy con Docker Compose
docker-compose -f docker-compose.production.yml build backend
docker-compose -f docker-compose.production.yml up -d backend

# 5. Verificar que está corriendo
docker-compose ps
docker-compose logs -f backend

# 6. Health check
curl https://api.haciendagamelera.com/api/v1/health

# 7. Smoke tests
curl -X GET https://api.haciendagamelera.com/api/v1/animals \
  -H "Authorization: Bearer $TOKEN" | jq .

# 8. Monitorear logs primeros 5 minutos
docker-compose logs -f backend --tail=100
```

### Deploy App Móvil (Android)

```bash
# 1. Build APK release
cd mobile
flutter build apk --release --target-platform android-arm64

# 2. Subir a S3 para distribución
aws s3 cp build/app/outputs/flutter-apk/app-release.apk \
  s3://bovine-releases/v1.0.0/bovine-weight-app-v1.0.0.apk \
  --acl public-read

# 3. Generar URL de descarga
aws s3 presign s3://bovine-releases/v1.0.0/bovine-weight-app-v1.0.0.apk \
  --expires-in 604800  # 7 días

# 4. Enviar URL a Bruno Brito Macedo
echo "URL de descarga: $PRESIGNED_URL"

# 5. Instrucciones de instalación (enviar a Bruno)
cat << EOF
Instalación en Android:

1. Descargar APK desde: $PRESIGNED_URL
2. En dispositivo Android:
   - Ir a Configuración > Seguridad
   - Activar "Orígenes desconocidos" o "Instalar aplicaciones desconocidas"
3. Abrir archivo descargado
4. Tocar "Instalar"
5. Abrir app "Sistema Peso Bovino"
6. Login:
   - Email: bruno@haciendagamelera.com
   - Password: [proporcionada separadamente]

Soporte: dev@haciendagamelera.com
EOF
```

---

## Rollback Plan

### Procedimiento de Rollback

```bash
# Si deploy v1.1.0 tiene problemas, volver a v1.0.0

# 1. Conectar a servidor
ssh -i ~/.ssh/hacienda-gamelera.pem ubuntu@ec2-server

# 2. Verificar versión actual
cd /opt/bovine-weight-estimation
git describe --tags  # v1.1.0

# 3. Checkout versión anterior estable
git checkout tags/v1.0.0

# 4. Rebuild y redeploy
docker-compose -f docker-compose.production.yml build backend
docker-compose -f docker-compose.production.yml up -d backend

# 5. Verificar rollback exitoso
curl https://api.haciendagamelera.com/api/v1/health
# Debe retornar: {"version": "1.0.0", "status": "healthy"}

# 6. Restaurar base de datos (si necesario)
# Usar backup del día anterior
aws s3 cp s3://bovine-backups-production/hacienda-gamelera/daily/20241105_020000/mongodb.tar.gz .
tar -xzf mongodb.tar.gz
docker exec -i bovine-mongodb mongorestore --drop --gzip mongodb-backup/

# 7. Notificar a stakeholders
echo "Sistema revertido a v1.0.0. Investigando issues de v1.1.0."
```

---

## Despliegue de Modelos ML

### Actualización de Modelos TFLite

```bash
#!/bin/bash
# scripts/deploy-ml-models.sh

set -e

echo "=========================================="
echo "DEPLOY MODELOS ML - HACIENDA GAMELERA"
echo "=========================================="

VERSION="v1.1.0"
S3_BUCKET="s3://bovine-ml-models-production"
MODELS_DIR="./models"

# Validar que existen los 7 modelos
REQUIRED_BREEDS=("brahman" "nelore" "angus" "cebuinas" "criollo" "pardo-suizo" "jersey")

for breed in "${REQUIRED_BREEDS[@]}"; do
    MODEL_FILE="$MODELS_DIR/$breed/$VERSION/$breed-$VERSION.tflite"
    
    if [ ! -f "$MODEL_FILE" ]; then
        echo "❌ Error: Modelo $MODEL_FILE no encontrado"
        echo "Se requieren los 7 modelos de Hacienda Gamelera"
        exit 1
    fi
    
    echo "✅ Encontrado: $MODEL_FILE"
done

echo "\n✅ Validación exitosa: 7 modelos TFLite encontrados"

# Subir modelos a S3
echo "\nSubiendo modelos a S3..."
for breed in "${REQUIRED_BREEDS[@]}"; do
    MODEL_FILE="$MODELS_DIR/$breed/$VERSION/$breed-$VERSION.tflite"
    METRICS_FILE="$MODELS_DIR/$breed/$VERSION/metrics.json"
    
    # Subir modelo
    aws s3 cp "$MODEL_FILE" "$S3_BUCKET/$breed-$VERSION.tflite" \
      --content-type "application/octet-stream" \
      --metadata "breed=$breed,version=$VERSION,hacienda=gamelera"
    
    # Subir métricas
    aws s3 cp "$METRICS_FILE" "$S3_BUCKET/$breed-$VERSION-metrics.json"
    
    echo "✅ Subido: $breed-$VERSION.tflite"
done

# Generar y subir manifest.json
echo "\nGenerando manifest.json..."
python scripts/generate_manifest.py --version "$VERSION" --output manifest.json
aws s3 cp manifest.json "$S3_BUCKET/manifest.json" \
  --cache-control "max-age=300"  # 5 minutos de caché

echo "\n=========================================="
echo "✅ DEPLOY MODELOS ML COMPLETADO"
echo "Versión: $VERSION"
echo "Modelos: 7/7 (todas las razas de Hacienda Gamelera)"
echo "S3 Bucket: $S3_BUCKET"
echo "=========================================="

# Notificar a app móvil que hay nuevos modelos
# (app verificará manifest.json cada 6 horas)
echo "\nNota: App móvil descargará nuevos modelos en próxima sincronización"
```

---

## Health Checks

### Backend Health Endpoint

```python
# app/api/routes/health.py

from fastapi import APIRouter, status
from pydantic import BaseModel
from datetime import datetime

from ...core.config import settings
from ...database.mongodb import get_database

router = APIRouter(tags=["Health"])

class HealthResponse(BaseModel):
    """Response de health check."""
    status: str
    version: str
    timestamp: datetime
    hacienda: str
    services: dict[str, str]

@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check del sistema",
)
async def health_check():
    """
    Verifica que todos los servicios estén funcionando.
    
    Checks:
    - API FastAPI respondiendo
    - MongoDB conectado
    - Modelos ML cargados (7 razas)
    - S3 accesible
    
    Returns:
        HealthResponse con estado de todos los servicios
    """
    services_status = {}
    
    # Check MongoDB
    try:
        db = await get_database()
        await db.command("ping")
        services_status["mongodb"] = "healthy"
    except Exception:
        services_status["mongodb"] = "unhealthy"
    
    # Check S3
    try:
        # Verificar que manifest.json existe
        s3_client = boto3.client('s3')
        s3_client.head_object(Bucket=settings.AWS_S3_BUCKET_NAME, Key='manifest.json')
        services_status["s3_models"] = "healthy"
    except Exception:
        services_status["s3_models"] = "unhealthy"
    
    # Check modelos ML (verificar que existen los 7)
    try:
        from ...ml.model_loader import MLModelFactory
        loaded_models = len(MLModelFactory._models)
        services_status["ml_models"] = f"healthy ({loaded_models}/7 loaded)"
    except Exception:
        services_status["ml_models"] = "unhealthy"
    
    overall_status = "healthy" if all(
        "healthy" in status for status in services_status.values()
    ) else "degraded"
    
    return HealthResponse(
        status=overall_status,
        version=settings.APP_VERSION,
        timestamp=datetime.now(),
        hacienda=settings.HACIENDA_NAME,
        services=services_status,
    )
```

---

## Disaster Recovery

### Plan de Recuperación ante Desastres

```markdown
## Disaster Recovery Plan - Hacienda Gamelera

### Escenarios

#### 1. Base de Datos Corrupta
**Detección**: Health check MongoDB falla, app no puede leer datos

**Recuperación**:
1. Detener backend: `docker-compose stop backend`
2. Descargar último backup: `aws s3 cp s3://bovine-backups/.../mongodb-latest.tar.gz .`
3. Restaurar MongoDB: `mongorestore --drop --gzip mongodb-backup/`
4. Verificar integridad: Contar animales por raza (debe ser ~500 total)
5. Reiniciar backend: `docker-compose up -d backend`
6. Smoke tests: Listar animales, estimar peso

**RTO**: 30 minutos  
**RPO**: <24 horas (backup diario)

#### 2. Modelos ML Perdidos/Corruptos
**Detección**: Estimaciones fallan con error "Model not found"

**Recuperación**:
1. Descargar modelos desde S3: `aws s3 sync s3://bovine-ml-models/production/ ./models/`
2. Verificar los 7 modelos TFLite existen
3. Verificar manifest.json
4. Reiniciar backend para recargar modelos

**RTO**: 10 minutos  
**RPO**: 0 (modelos versionados en S3)

#### 3. Servidor EC2 Caído Completamente
**Detección**: API no responde, monitoring alert

**Recuperación**:
1. Lanzar nueva instancia EC2 desde AMI backup
2. Montar volumen EBS con datos (si existe)
3. Instalar Docker + Docker Compose
4. Clonar repo: `git clone ... && git checkout tags/v1.0.0`
5. Copiar .env de AWS Secrets Manager
6. Restaurar MongoDB desde backup S3
7. Deploy: `docker-compose -f docker-compose.production.yml up -d`
8. Configurar NGINX con SSL
9. Actualizar DNS (Route 53) a nueva IP

**RTO**: 2 horas  
**RPO**: <24 horas

#### 4. App Móvil con Bug Crítico en Producción
**Detección**: Reportes de Bruno, crashlytics alerts

**Recuperación**:
1. Identificar versión estable anterior (ej: v1.0.0)
2. Re-release APK anterior en S3
3. Notificar a Bruno para desinstalar y reinstalar
4. Hotfix en branch: `git checkout -b hotfix/critical-camera-crash`
5. Fix, test, merge a main
6. Build nuevo APK con version v1.0.1
7. Deploy v1.0.1 como patch

**RTO**: 4 horas (para fix), 10 minutos (para rollback)  
**RPO**: N/A (app es stateless)
```

---

## Monitoreo y Alertas

### Alertas Críticas (PagerDuty / Slack)

```yaml
# prometheus/alerts.yml

groups:
  - name: bovine_critical_alerts
    interval: 30s
    rules:
      # Precisión ML por debajo del umbral
      - alert: MLPrecisionBelowThreshold
        expr: avg(weighing_estimation_confidence) < 0.95
        for: 5m
        labels:
          severity: critical
          hacienda: gamelera
        annotations:
          summary: "Precisión ML <95% en Hacienda Gamelera"
          description: "Confidence promedio {{ $value | humanizePercentage }} < 95% requerido. Verificar modelos TFLite."
      
      # Tiempo de procesamiento muy lento
      - alert: ProcessingTimeTooSlow
        expr: histogram_quantile(0.95, weighing_estimation_duration_seconds_bucket) > 3.0
        for: 5m
        labels:
          severity: warning
          hacienda: gamelera
        annotations:
          summary: "Procesamiento >3 segundos en Hacienda Gamelera"
          description: "p95 = {{ $value | humanizeDuration }}. Objetivo: <3 segundos."
      
      # Backend down
      - alert: BackendDown
        expr: up{job="backend"} == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Backend API no responde"
          description: "API de Hacienda Gamelera caída hace >2 minutos."
      
      # MongoDB disconnected
      - alert: MongoDBDisconnected
        expr: mongodb_up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "MongoDB desconectado"
          description: "Base de datos de Hacienda Gamelera inaccesible."
```

---

## Runbook de Operaciones

### Comandos Útiles

```bash
# Ver logs en tiempo real
docker-compose logs -f backend --tail=100

# Reiniciar servicio específico
docker-compose restart backend

# Verificar uso de recursos
docker stats

# Limpiar espacio en disco
docker system prune -a --volumes -f

# Backup manual urgente
./scripts/backup.sh

# Verificar health check
curl https://api.haciendagamelera.com/api/v1/health | jq .

# Ver métricas de MongoDB
docker exec bovine-mongodb mongo --eval "db.stats()"

# Contar animales por raza (debe ser ~500 total)
docker exec bovine-mongodb mongo bovine_weight_estimation --eval "
  db.animals.aggregate([
    { \$group: { _id: '\$breed_type', count: { \$sum: 1 } } }
  ])"

# Tail logs de NGINX
tail -f /var/log/nginx/bovine-api-access.log | grep -v health

# Ver último backup en S3
aws s3 ls s3://bovine-backups-production/hacienda-gamelera/daily/ \
  --recursive | tail -10
```

---

## Security Checklist

```markdown
## Security Checklist - Producción

### Infraestructura
- [x] Firewall configurado (solo 80, 443, 22)
- [x] SSH con key-based auth (no passwords)
- [x] SSL/TLS certificado válido (Let's Encrypt)
- [x] NGINX con headers de seguridad
- [x] Docker containers sin root user

### Aplicación
- [x] JWT con secret key fuerte (64+ chars)
- [x] Passwords hasheados con bcrypt
- [x] Rate limiting en APIs críticas
- [x] CORS configurado solo origins permitidos
- [x] SQL injection prevención (Beanie ODM)
- [x] Secrets en AWS Secrets Manager (no en .env)

### Datos
- [x] Encriptación en tránsito (HTTPS)
- [x] Encriptación en reposo (MongoDB encryption at rest)
- [x] Backups encriptados en S3
- [x] Logs no contienen información sensible
- [x] GDPR compliance (si aplicable)

### Auditoría
- [x] Logs de acceso a APIs sensibles
- [x] Logs de generación de reportes SENASAG
- [x] Logs de creación de GMAs
- [x] Monitoreo de intentos de login fallidos
```

---

## Referencias

- **Architecture**: `docs/standards/architecture-standards.md`
- **Docker**: https://docs.docker.com/
- **AWS**: https://docs.aws.amazon.com/
- **Prometheus**: https://prometheus.io/docs/

---

**Documento de Deployment Standards v1.0**  
**Fecha**: 28 octubre 2024  
**Proyecto**: Sistema de Estimación de Peso Bovino con IA  
**Cliente**: Hacienda Gamelera (Bruno Brito Macedo)  
**Infraestructura**: Docker + AWS + MongoDB Atlas + NGINX


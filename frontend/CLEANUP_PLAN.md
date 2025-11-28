# 🧹 Plan de Limpieza - Eliminar Referencias a Compañía/Propiedad

## 📋 Archivos a Eliminar

### Vistas (`src/views/`)
- [ ] `CompanyView.js` - ❌ Eliminar
- [ ] `PropertyView.js` - ❌ Eliminar
- [ ] `MapView.js` - ❌ Eliminar
- [ ] `RoleView.js` - ✅ **MANTENER** (gestión de roles)
- [ ] `UserView.js` - ✅ **MANTENER** (adaptar - eliminar referencias a Company)

### Templates (`src/templates/`)
- [ ] `CompanyTemplate.js` - ❌ Eliminar
- [ ] `PropertyTemplate.js` - ❌ Eliminar
- [ ] `MapTemplate.js` - ❌ Eliminar
- [ ] `RoleTemplate.js` - ✅ **MANTENER**
- [ ] `UserTemplate.js` - ✅ **MANTENER** (adaptar - eliminar referencias a Company)

### Servicios (`src/services/`)
- [ ] `company/` (toda la carpeta)
  - `createCompany.js`
  - `getAllCompanies.js`
- [ ] `property/` (toda la carpeta)
  - `createProperty.js`
  - `getCompanyProperty.js`
  - `getUserProperty.js`
- [ ] `role/` - ✅ **MANTENER**
  - `createRole.js`
  - `getAllRoles.js`
- [ ] `user/` - ✅ **MANTENER** (adaptar - eliminar referencias a Company)
  - `createUser.js`

### Containers (`src/containers/`)
- [ ] `company/` (toda la carpeta)
  - `CreateNewCompany.js`
  - `GetAllCompanies.js`
- [ ] `property/` (toda la carpeta)
  - `CreateNewProperty.js`
- [ ] `role/` - ✅ **MANTENER**
  - `CreateNewRole.js`
  - `GetAllRoles.js`
- [ ] `user/` - ✅ **MANTENER** (adaptar - eliminar referencias a Company)
  - `CreateNewUser.js`
  - `GetProperty.js` - ⚠️ Evaluar si se necesita (probablemente eliminar)

### Organisms (`src/components/organisms/`)
- [ ] `CreateCompany/`
- [ ] `CreateProperty/`
- [ ] `CreateRole/` - ✅ **MANTENER**
- [ ] `CreateUser/` - ✅ **MANTENER** (adaptar - eliminar referencias a Company)

### Utils/Transformers (`src/utils/transformers/`)
- [ ] `companyToComboBox.js`
- [ ] `propertyToRadioButton.js`
- [ ] `roleToComboBox.js` - ✅ **MANTENER**

## ✅ Decisiones Tomadas

### Gestión de Usuarios/Roles
- ✅ **MANTENER** `RoleView.js`, `UserView.js`, `CreateRole/`, `CreateUser/`
- ✅ El sistema tiene roles: Administrador, Usuario, Invitado
- ⚠️ **ADAPTAR** para eliminar referencias a Company/Property

### Archivos a Adaptar (NO eliminar)
- `UserView.js` - Eliminar `GetAllCompanies` y referencias a Company
- `UserTemplate.js` - Eliminar dependencia de `dataList` (companies)
- `CreateUser/` - Eliminar referencias a Company
- `containers/user/CreateNewUser.js` - Eliminar lógica de Company
- `containers/user/GetProperty.js` - Evaluar si se necesita (probablemente eliminar)

## 📝 Orden de Eliminación

1. **Primero**: Eliminar servicios y containers (no se usan)
2. **Segundo**: Eliminar vistas y templates obsoletos
3. **Tercero**: Eliminar organisms y transformers
4. **Cuarto**: Limpiar imports en archivos que los referencien
5. **Quinto**: Actualizar rutas (ya hecho en routes.js)

## ✅ Verificación

Después de eliminar, verificar:
- [ ] No hay imports rotos
- [ ] No hay referencias en `routes.js`
- [ ] No hay referencias en `constants.js` (sidebar)
- [ ] El proyecto compila sin errores


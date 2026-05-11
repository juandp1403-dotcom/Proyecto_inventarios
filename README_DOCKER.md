# Docker Compose - Sistema de Inventarios

## Arquitectura del Contenedor

Este proyecto incluye una configuración completa de Docker Compose con los siguientes servicios:

### Servicios

1. **web**: Aplicación Flask (puerto 5000)
2. **db**: Base de datos PostgreSQL (puerto 5432)
3. **adminer**: Interfaz de administración de BD (puerto 8080)

## Uso

### Producción
```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f web

# Detener servicios
docker-compose down
```

### Desarrollo
```bash
# Iniciar con SQLite y modo debug
docker-compose -f docker-compose.dev.yml up -d

# Reconstruir imagen
docker-compose build --no-cache web
```

### Comandos útiles
```bash
# Entrar al contenedor de la app
docker-compose exec web bash

# Ver estado de los contenedores
docker-compose ps

# Eliminar volúmenes (cuidado: borra datos)
docker-compose down -v
```

## Configuración

- **Base de datos**: PostgreSQL con persistencia de datos
- **Variables de entorno**: Configuradas en docker-compose.yml
- **Volúmenes**: Datos persistentes y archivos de la aplicación

## Acceso

- **Aplicación**: http://localhost:5000
- **Adminer (BD)**: http://localhost:8080
  - Servidor: db
  - Usuario: postgres
  - Contraseña: password
  - Base de datos: inventarios

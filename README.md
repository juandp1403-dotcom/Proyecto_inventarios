# Sistema de Gestión de Inventarios

Sistema web desarrollado con **Flask**, **SQLAlchemy** y **PostgreSQL / SQLite** para la gestión y trazabilidad de inventarios, ambientes, artículos, solicitudes y auditoría de accesos.

---

## 🚀 Integración Continua (GitHub Actions)

El proyecto cuenta con integración continua configurada en [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

### Disparadores del Workflow
- **Push**: a ramas `main`, `dev`, `Test-**`, y ramas de características `feature/**`.
- **Pull Request**: hacia las ramas `main` y `dev`.
- **Ejecución manual**: disponible desde la pestaña *Actions* de GitHub (*workflow_dispatch*).

### Matriz de Pruebas
Las pruebas se ejecutan automáticamente en entornos limpios de Ubuntu con:
- Python 3.11
- Python 3.12

---

## 🧪 Ejecución de Pruebas en Local

### 1. Activar el entorno virtual e instalar dependencias

```bash
# En Windows (PowerShell)
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Ejecutar todas las pruebas (recomendado)

Se incluye el script centralizado [`run_tests.py`](run_tests.py) que descubre y ejecuta de forma unificada las pruebas de las carpetas `test/` y `tests/`:

```bash
python run_tests.py
```

### 3. Ejecutar pruebas con el módulo nativo `unittest`

Si prefieres ejecutar los módulos por separado:

```bash
# Pruebas de modelos, movimientos, auditoría, reportes y roles (carpeta test/)
python -m unittest discover -s test -p "test_*.py" -v

# Pruebas de autenticación y utilidades (carpeta tests/)
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## 📦 Estructura de Pruebas

- [`test/base_test.py`](test/base_test.py): Configuración de la base de datos de pruebas en memoria (`sqlite:///:memory:`) y utilidades generadoras de fixtures (usuarios, roles, ambientes, artículos).
- [`test/test_usuario.py`](test/test_usuario.py): Pruebas de modelos y validaciones de usuario.
- [`test/test_rol.py`](test/test_rol.py): Pruebas del catálogo y asignación de roles.
- [`test/test_solicitud.py`](test/test_solicitud.py): Pruebas del flujo de estados y aprobación de solicitudes.
- [`test/test_movimiento.py`](test/test_movimiento.py): Pruebas de kardex y movimientos de entrada/salida.
- [`test/test_reporte.py`](test/test_reporte.py): Pruebas de generación y almacenamiento de reportes.
- [`test/test_login_auditoria.py`](test/test_login_auditoria.py): Pruebas del sistema de trazabilidad y bloqueo de intentos de inicio de sesión.
- [`tests/test_auth.py`](tests/test_auth.py): Pruebas de validación y hash de contraseñas.

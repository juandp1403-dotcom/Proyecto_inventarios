import os
import sys
import unittest

def run_all_tests():
    # Asegurar que el directorio raíz del proyecto esté en sys.path
    project_root = os.path.abspath(os.path.dirname(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Variables de entorno por defecto para pruebas si no están definidas
    os.environ.setdefault('SECRET_KEY', 'test-secret-key-12345')
    os.environ.setdefault('DATABASE_URL', 'sqlite:///:memory:')

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Descubrir pruebas en ambas carpetas 'test' y 'tests'
    total_dirs = 0
    for test_dir in ['test', 'tests']:
        dir_path = os.path.join(project_root, test_dir)
        if os.path.isdir(dir_path):
            discovered = loader.discover(start_dir=dir_path, pattern='test_*.py', top_level_dir=project_root)
            suite.addTests(discovered)
            total_dirs += 1

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)

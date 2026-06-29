import unittest
from werkzeug.security import generate_password_hash

from app.routes.usuario_routes import verify_password


class VerifyPasswordTestCase(unittest.TestCase):
    def test_plaintext_password_is_accepted(self):
        self.assertTrue(verify_password('123456', '123456'))

    def test_hashed_password_is_accepted(self):
        stored_hash = generate_password_hash('123456')
        self.assertTrue(verify_password(stored_hash, '123456'))

    def test_wrong_password_is_rejected(self):
        self.assertFalse(verify_password('123456', 'wrong'))


if __name__ == '__main__':
    unittest.main()

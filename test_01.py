import orm_setup
import unittest
from codicefiscale import codicefiscale
from app.ges_login.login_controller import LoginController
from app.ges_login.login_model import LoginModel
from store.models import Esame, Utente
from app.utils import Ambiente


class PyRISTest(unittest.TestCase):

    def test_codicefiscale_corretto(self):
        self.assertEqual(codicefiscale.encode('Bramucci', 'Matteo Lorenzo', 'M', '31/10/2000', 'Jesi'), 'BRMMTL00R31E388S')

    def test_codicefiscale_incompleto(self):
        with self.assertRaises(ValueError):
            self.assertEqual(codicefiscale.encode('Bramucci', 'Matteo Lorenzo', 'M', '31/10/2000', ''), 'BRMMTL00R31E388S')

    def test_login_ok(self):
        modello = LoginModel()
        controllore = LoginController(modello)
        self.assertEqual(controllore.login('admin', 'admin'), True)

    def test_login_not_ok(self):
        modello = LoginModel()
        controllore = LoginController(modello)
        self.assertEqual(controllore.login('admin1', 'admin'), False)

    def test_configurazioni_default(self):
        self.assertEqual(Ambiente.visualizzazione['stile'], "Fusion")
        self.assertEqual(Ambiente.visualizzazione['tema'], "scuro")


if __name__ == '__main__':
    unittest.main()
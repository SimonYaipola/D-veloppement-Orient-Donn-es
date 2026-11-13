import unittest
from metier.clientMetier import rechercherClient

class test_rechercherClient(unittest.TestCase):

    def test_id_null(self):
        with self.assertRaises(ValueError):
            rechercherClient(None)

    def test_id_introuvable(self):
        with self.assertRaises(ValueError):
            rechercherClient('00000000-0000-0000-0000-000000000000')
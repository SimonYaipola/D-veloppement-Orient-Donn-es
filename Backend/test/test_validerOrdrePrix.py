import unittest
from types import SimpleNamespace
from pydantic import ValidationError
from DTO.typechambreDTO import TypeChambreDTO

class TestTypeChambreDTO(unittest.TestCase):
    def creer_dto(self,prix_plafond, prix_plancher):
        #Fournit les attributs attendus par le constructeur du DTO
        type_chambre = SimpleNamespace(
            id_type_chambre=None,
            nom_type="Double",
            prix_plafond=prix_plafond,
            prix_plancher=prix_plancher,
            description_chambre="Chambre de test",
        )
        return TypeChambreDTO(type_chambre)

    def test_accepte_plafond_superieur_ou_egal_au_plancer(self):
        for plafond in (200.0,150.0):
            with self.subTest(prix_plafond=plafond):
                dto = self.creer_dto(plafond, 150.0)
                self.assertEqual(dto.prix_plafond, plafond)
                self.assertEqual(dto.prix_plancher, 150.0)

    def test_accepte_plafond_absent(self):
        dto = self.creer_dto(None, 150.0)

        self.assertIsNone(dto.prix_plafond)
        self.assertEqual(dto.prix_plancher, 150.0)

    def test_refuse_plafond_inferieur_au_plancher(self):
        with self.assertRaises(ValidationError) as contexte:
            self.creer_dto(100.0, 150.0)

        erreur = contexte.exception.errors()[0]
        self.assertEqual(erreur["loc"], ())
        self.assertEqual(erreur["type"], "value_error")
        self.assertIn(
            "Le prix plafond doit être supérieur ou égal au prix plancher.",
            erreur["msg"],
        )

if __name__ == "__main__":
    unittest.main()


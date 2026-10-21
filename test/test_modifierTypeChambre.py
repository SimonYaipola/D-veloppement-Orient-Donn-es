import unittest
from unittest.mock import Mock, patch
from uuid import uuid4

from DTO.typechambreDTO import TypeChambreDTO
from modele.table import Typechambre
from metier.chambreMetier import modifierTypeChambre


class TestModifierTypeChambre(unittest.TestCase):

    def setUp(self):
        self.identifiant = uuid4()

        self.modifications = TypeChambreDTO(
            Typechambre(
                id_type_chambre=str(self.identifiant).upper(),
                nom_type="Double",
                prix_plancher=200.0,
                prix_plafond=300.0,
                description_chambre="Nouvelle description",
            )
        )

        self.session = Mock()
    ## Test pour vérifier que la fonction modifierTypeChambre modifie correctement un type de chambre existant et retourne le DTO mis à jour.
    @patch("metier.chambreMetier.Session")
    def test_modification_reussie(self, mock_session):
        mock_session.return_value.__enter__.return_value = self.session

        type_existant = Typechambre(
            id_type_chambre=str(self.identifiant).upper(),
            nom_type="Simple",
            prix_plancher=100.0,
            prix_plafond=150.0,
            description_chambre="Ancienne description",
        )
        self.session.get.return_value = type_existant

        resultat = modifierTypeChambre(self.modifications)

        self.session.get.assert_called_once_with(
            Typechambre,
            str(self.identifiant).upper(),
        )
        self.session.commit.assert_called_once()

        self.assertEqual(type_existant.nom_type, "Double")
        self.assertEqual(type_existant.prix_plancher, 200.0)
        self.assertEqual(type_existant.prix_plafond, 300.0)
        self.assertEqual(
            type_existant.description_chambre,
            "Nouvelle description",
        )

        self.assertIsInstance(resultat, TypeChambreDTO)
        self.assertEqual(resultat.id_type_chambre, self.identifiant)
        self.assertEqual(resultat.nom_type, "Double")
        self.assertEqual(resultat.prix_plancher, 200.0)
        self.assertEqual(resultat.prix_plafond, 300.0)
        self.assertEqual(
            resultat.description_chambre,
            "Nouvelle description",
        )
    ### Test pour vérifier que la fonction modifierTypeChambre lève une exception ValueError lorsque l'identifiant du type de chambre est absent.
    @patch("metier.chambreMetier.Session")
    def test_identifiant_absent(self, mock_session):
        self.modifications.id_type_chambre = None

        with self.assertRaisesRegex(
            ValueError,
            "L'identifiant du type de chambre est obligatoire",
        ):
            modifierTypeChambre(self.modifications)

        mock_session.assert_not_called()
    ### Test pour vérifier que la fonction modifierTypeChambre lève une exception ValueError lorsque le type de chambre à modifier n'existe pas dans la base de données.    
    @patch("metier.chambreMetier.Session")
    def test_type_introuvable(self, mock_session):
        mock_session.return_value.__enter__.return_value = self.session
        self.session.get.return_value = None

        with self.assertRaisesRegex(
            ValueError,
            "Le type de chambre est introuvable",
        ):
            modifierTypeChambre(self.modifications)

        self.session.commit.assert_not_called()
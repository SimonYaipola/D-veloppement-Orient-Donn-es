import unittest
from unittest.mock import Mock, patch
from uuid import uuid4

from modele.table import Chambre
from modele.typeChambre import Typechambre
from metier.chambreMetier import supprimerTypeChambre


class TestSupprimerTypeChambre(unittest.TestCase):

    def setUp(self):
        self.identifiant = uuid4()
        self.session = Mock()
    ## Test pour vérifier que la fonction supprimerTypeChambre supprime correctement un type de chambre existant.
    @patch("metier.chambreMetier.Session")
    def test_suppression_reussie(self, mock_session):
        mock_session.return_value.__enter__.return_value = self.session

        type_existant = Typechambre(
            id_type_chambre=str(self.identifiant).upper(),
            nom_type="Double",
            prix_plancher=200.0,
            prix_plafond=300.0,
            description_chambre="Chambre de test",
            chambre=[],
        )
        self.session.get.return_value = type_existant

        supprimerTypeChambre(self.identifiant)

        self.session.get.assert_called_once_with(
            Typechambre,
            str(self.identifiant).upper(),
        )
        self.session.delete.assert_called_once_with(type_existant)
        self.session.commit.assert_called_once()
    ## Test pour vérifier que la fonction supprimerTypeChambre lève une exception ValueError lorsque l'identifiant du type de chambre est absent ou lorsque le type de chambre n'est pas trouvé dans la base de données.
    @patch("metier.chambreMetier.Session")
    def test_identifiant_absent(self, mock_session):
        with self.assertRaisesRegex(
            ValueError,
            "L'identifiant du type de chambre est obligatoire",
        ):
            supprimerTypeChambre(None)

        mock_session.assert_not_called()
    ## Test pour vérifier que la fonction supprimerTypeChambre lève une exception ValueError lorsque le type de chambre à supprimer n'existe pas dans la base de données.
    @patch("metier.chambreMetier.Session")
    def test_type_introuvable(self, mock_session):
        mock_session.return_value.__enter__.return_value = self.session
        self.session.get.return_value = None

        with self.assertRaisesRegex(
            ValueError,
            "Le type de chambre est introuvable",
        ):
            supprimerTypeChambre(self.identifiant)

        self.session.delete.assert_not_called()
        self.session.commit.assert_not_called()
    ## Test pour vérifier que la fonction supprimerTypeChambre lève une exception ValueError lorsque le type de chambre à supprimer est utilisé par une chambre existante.
    @patch("metier.chambreMetier.Session")
    def test_type_utilise_par_une_chambre(self, mock_session):
        mock_session.return_value.__enter__.return_value = self.session

        self.session.get.return_value = Typechambre(
            id_type_chambre=str(self.identifiant).upper(),
            nom_type="Double",
            prix_plancher=200.0,
            prix_plafond=300.0,
            description_chambre="Chambre de test",
            chambre=[Chambre(numero_chambre=101)],
        )

        with self.assertRaisesRegex(
            ValueError,
            "Ce type de chambre est utilisé par une chambre",
        ):
            supprimerTypeChambre(self.identifiant)

        self.session.delete.assert_not_called()
        self.session.commit.assert_not_called()
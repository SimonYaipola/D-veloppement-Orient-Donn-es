import unittest
from unittest.mock import Mock, patch
from uuid import uuid4
from DTO.typechambreDTO import TypeChambreDTO
from modele.typeChambre import TypeChambre
from metier.typeChambreMetier import rechercherTypeChambre

class TestRechercherTypeChambre(unittest.TestCase):

    def setUp(self):
        self.identifiant = uuid4()
        self.session = Mock()
    ## Test pour vérifier que la fonction rechercherTypeChambre retourne correctement le DTO correspondant à un type de chambre existant.
    @patch("metier.typeChambreMetier.Session")
    def test_recherche_reussie(self, mock_session):
        mock_session.return_value.__enter__.return_value = self.session
        self.session.get.return_value = TypeChambre(
            id_type_chambre=str(self.identifiant).upper(),
            nom_type="Double",
            prix_plancher=200.0,
            prix_plafond=300.0,
            description_chambre="Chambre avec deux lits",
        )

        resultat = rechercherTypeChambre(self.identifiant)

        self.session.get.assert_called_once_with(
            TypeChambre,
            str(self.identifiant).upper(),
        )
        self.assertIsInstance(resultat, TypeChambreDTO)
        self.assertEqual(resultat.id_type_chambre, self.identifiant)
        self.assertEqual(resultat.nom_type, "Double")
        self.assertEqual(resultat.prix_plancher, 200.0)
        self.assertEqual(resultat.prix_plafond, 300.0)
        self.assertEqual(
            resultat.description_chambre,
            "Chambre avec deux lits",
        )
        self.session.commit.assert_not_called()
     ## Test pour vérifier que la fonction rechercherTypeChambre lève une exception lorsque l'identifiant du type de chambre est absent ou lorsque le type de chambre n'est pas trouvé dans la base de données.
    @patch("metier.typeChambreMetier.Session")
    def test_identifiant_absent(self, mock_session):
        with self.assertRaisesRegex(
            ValueError,
            "L'identifiant du type de chambre est obligatoire",
        ):
            rechercherTypeChambre(None)

        mock_session.assert_not_called()
    ## Test pour vérifier que la fonction rechercherTypeChambre lève une exception ValueError lorsque le type de chambre à rechercher n'existe pas dans la base de données.
    @patch("metier.typeChambreMetier.Session")
    def test_type_introuvable(self, mock_session):
        mock_session.return_value.__enter__.return_value = self.session
        self.session.get.return_value = None

        with self.assertRaisesRegex(
            ValueError,
            "Le type de chambre est introuvable",
        ):
            rechercherTypeChambre(self.identifiant)

        self.session.commit.assert_not_called()

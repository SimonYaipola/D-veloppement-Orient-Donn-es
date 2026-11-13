import unittest
from unittest.mock import patch, Mock
from uuid import uuid4
from metier.chambreMetier import supprimerChambre
from modele.chambre import Chambre


class TestSupprimerChambre(unittest.TestCase):

    def setUp(self):
        self.identifiant= uuid4()  
        self.session = Mock()

    @patch('metier.chambreMetier.Session')
    def test_supprimer_chambre_reussie(self,mock_session):
        mock_session.return_value.__enter__.return_value = self.session

        chambre = Chambre(
            id_chambre=self.identifiant,
            numero_chambre=101,
            disponible_reservation=True,
            autre_informations="Simple",
            reservations=[],
            
        )
        self.session.get.return_value = chambre

        supprimerChambre(self.identifiant)
        self.session.get.assert_called_once_with(Chambre, str(self.identifiant).upper())
        self.session.delete.assert_called_once_with(chambre)
        self.session.commit.assert_called_once()
    @patch('metier.chambreMetier.Session')
    def test_identifiant_absent(self, mock_session):
        with self.assertRaisesRegex(
            ValueError,
            "L'ID de la chambre ne peut pas être null.",
        ):
            supprimerChambre(None)

        mock_session.assert_not_called()

    @patch('metier.chambreMetier.Session')
    def test_chambre_introuvable(self, mock_session):
        mock_session.return_value.__enter__.return_value = self.session
        self.session.get.return_value = None

        with self.assertRaisesRegex(
            ValueError,
            "La chambre est introuvable.",
        ):
            supprimerChambre(self.identifiant)

        mock_session.delete.assert_not_called()
        mock_session.commit.assert_not_called()

    @patch('metier.chambreMetier.Session')
    def test_chambre_utilisee_par_reservation(self, mock_session):
        mock_session.return_value.__enter__.return_value = self.session

        chambre = Mock(spec=Chambre)
        chambre.reservations = [Mock()]  # Simuler une réservation existante
        mock_session.get.return_value = chambre

        with self.assertRaisesRegex(
            ValueError,
            "La chambre ne peut pas être supprimée, car elle est associée à une ou plusieurs réservations.",
        ):
            supprimerChambre(self.identifiant)
        mock_session.delete.assert_not_called()
        mock_session.commit.assert_not_called()
    



        
        
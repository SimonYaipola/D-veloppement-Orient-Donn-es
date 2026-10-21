import unittest
from unittest.mock import Mock, patch
from uuid import uuid4
from modele.client import Client
from modele.reservation import Reservation
from metier.clientMetier import supprimerClient

class TestSupprimerClient(unittest.TestCase):

    def setUp(self):
        self.identifiant = uuid4()
        self.session = Mock()
    @patch("metier.clientMetier.Session")
    def test_suppression_reussie(self, mock_session):
        mock_session.return_value.__enter__.return_value = self.session

        client_existant = Client(
            id_client=str(self.identifiant).upper(),
            nom="L'agent",
            prenom="Jean",
            adresse="quelquepart",
            mot_de_passe="MotDePasse",
            mobile="1112223333",
            reservations=[],
        )
        self.session.get.return_value = client_existant

        supprimerClient(self.identifiant)

        self.session.get.assert_called_once_with(
            Client,
            str(self.identifiant).upper(),
        )
        self.session.delete.assert_called_once_with(client_existant)
        self.session.commit.assert_called_once()
    @patch("metier.clientMetier.Session")
    def test_identifiant_absent(self, mock_session):
        with self.assertRaisesRegex(
            ValueError,
            "L'identifiant du client est obligatoire",
        ):
            supprimerClient(None)

        mock_session.assert_not_called()
    @patch("metier.clientMetier.Session")
    def test_client_introuvable(self, mock_session):
        mock_session.return_value.__enter__.return_value = self.session
        self.session.get.return_value = None

        with self.assertRaisesRegex(
            ValueError,
            "Le client est introuvable",
        ):
            supprimerClient(self.identifiant)

        self.session.delete.assert_not_called()
        self.session.commit.assert_not_called()
    @patch("metier.clientMetier.Session")
    def test_client_avec_reservations(self, mock_session):
        mock_session.return_value.__enter__.return_value = self.session

        self.session.get.return_value = Client(
            id_client=str(self.identifiant).upper(),
            nom="Jean",
            prenom="L'agent",
            adresse="quelquepart",
            mot_de_passe="MotDePasse",
            mobile="1112223333",
            reservations=[Reservation(numero_reservation=1)],
        )

        with self.assertRaisesRegex(
            ValueError,
            "Ce client a des réservations",
        ):
            supprimerClient(self.identifiant)

        self.session.delete.assert_not_called()
        self.session.commit.assert_not_called()
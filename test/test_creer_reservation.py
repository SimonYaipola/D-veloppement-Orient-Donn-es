from datetime import date, datetime
import unittest
from unittest.mock import patch
from modele.table import Client, Chambre, Typechambre
from metier.reservationMetier import creerReservation
from DTO.reservationDTO import ReservationCreerDTO

from sqlalchemy import create_engine, delete
import urllib
from uuid import UUID

server = '158.69.208.232,1433'
database = 'Hotels'
username = 'sa'
password = 'Automne,2026'
params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
with engine.connect() as connection:
    print("Connection réussie") 

# fausses variables pour les mock tests
ID_CLIENT = "EC50134D-372B-4DFD-9627-02BE06BA6BD6"
ID_CHAMBRE = "1276E513-BB05-41D9-B22E-0073772A006A"

class test_creerReservation(unittest.TestCase):
    @patch("metier.reservationMetier.Session")
    def test_creerReservation(self, mockSession):
        session = mockSession.return_value.__enter__.return_value

        # créer le client et la chambre Mock pour ensuite les utiliser dans le mock test
        client = Client(id_client=ID_CLIENT, prenom="Test", nom="Test", adresse="Test", mot_de_passe="Test", mobile="5145550000")
        chambre = Chambre(id_chambre=ID_CHAMBRE, numero_chambre=1, disponible_reservation=True, autre_informations="Test", fk_type_chambre="00000000-0000-0000-0000-000000000000")
        # créer le type chambre mock pour l'associer à la chambre
        chambre.type_chambre = Typechambre(
            id_type_chambre="00000000-0000-0000-0000-000000000000",
            nom_type="Test",
            prix_plafond=300.0,
            prix_plancher=100.0,
            description_chambre="Test",
        )
        session.get.side_effect = [chambre, client]
        session.refresh.side_effect = lambda r: setattr(r, "numero_reservation", 2) # Trouvé par IA, problème d'attribution de la valeur à la variable numero_reservation
        # Création de la fausse reservation avec la classe ReservationCreerDTO
        DTO = ReservationCreerDTO(
            date_debut_reservation=date(2026, 9, 20),
            date_fin_reservation=date(2026, 9, 25),
            prix_jour=200.00,
            info_reservation="Mock test de création d'une réservation",
            id_client=UUID(ID_CLIENT),
            id_chambre=UUID(ID_CHAMBRE),
        )

        # création de la reservation mock
        resultat = creerReservation(DTO)

        session.add.assert_called_once()
        session.commit.assert_called_once()

        # confirmation des valeurs de la nouvelle reservation
        ajoutee = session.add.call_args.args[0]
        UUID(str(ajoutee.id_reservation))
        self.assertEqual(ajoutee.date_debut_reservation, date(2026, 9, 20))
        self.assertEqual(ajoutee.date_fin_reservation, date(2026, 9, 25))
        self.assertEqual(ajoutee.prix_jour, 200.00)
        self.assertEqual(ajoutee.client, client)
        self.assertEqual(ajoutee.chambre, chambre)
        self.assertEqual(resultat.numero_reservation, 2)
        UUID(str(ajoutee.id_reservation))
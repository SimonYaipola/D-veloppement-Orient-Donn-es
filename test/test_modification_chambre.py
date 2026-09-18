import unittest
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
import urllib
from modele.chambre import Chambre, Typechambre
from metier.chambreMetier import modifierChambre, ChambreDTO

    
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


class test_modification_Chambre(unittest.TestCase):
    def test_modifierChambre(self):
        chambreDTO = ChambreDTO(
            Chambre(
                numero_chambre=490,
                disponible_reservation=False,
                type_chambre=
                    Typechambre(
                        nom_type='king',
                        prix_plancher=229.0
                    )
            )
        )

        chambreDTOModifier = modifierChambre(chambreDTO)

        self.assertEqual(chambreDTOModifier.numero_chambre, 501)
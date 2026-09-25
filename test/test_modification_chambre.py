import unittest
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from sqlalchemy import text
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
        with Session(engine) as session:
            numChambre = 294
            stmt = select(Chambre).where(
                Chambre.numero_chambre == numChambre
            )

            chambreAModifier = session.execute(stmt).scalars().first()

            self.assertIsNotNone(chambreAModifier, "La chambre" + str(numChambre) + " n'existe pas")

            type_chambre = session.get(Typechambre, chambreAModifier.fk_type_chambre)

            chambreDTOModifier = ChambreDTO(
                Chambre(
                    id_chambre=chambreAModifier.id_chambre,
                    numero_chambre=numChambre,
                    disponible_reservation=False,
                    autre_informations="Chambre modifiée",
                    type_chambre=type_chambre
                    )
                )
            

            chambreDTOModifier = modifierChambre(chambreDTOModifier)

            self.assertEqual(chambreDTOModifier.numero_chambre, numChambre)
import unittest
from modele.chambre import Chambre, Typechambre
from metier.chambreMetier import creerChambre, ChambreDTO
from sqlalchemy.orm import Session
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


class test_creerChambre(unittest.TestCase):
    def test_creerChambre(self):
        chambreDTO = ChambreDTO(
            Chambre(
                numero_chambre=501,
                disponible_reservation=True,
                autre_informations='lavabo inclut',
                id_chambre='1776E513-BB05-41D9-B22E-0073772A006A',
                type_chambre=
                    Typechambre(
                        nom_type='triple',
                        prix_plancher=210,
                        prix_plafond=320,
                        description_chambre='Chambre avec un gros lit'
                    )
            )
        )

        chambreDTOCree = creerChambre(chambreDTO)

        self.assertEqual(chambreDTOCree.numero_chambre, 501)
        self.assertEqual(chambreDTOCree.disponible_reservation, True)
        self.assertEqual(chambreDTOCree.autre_informations, 'lavabo inclut')
        self.assertEqual(chambreDTOCree.idChambre, UUID('1776E513-BB05-41D9-B22E-0073772A006A'))
        self.assertEqual(chambreDTOCree.type_chambre.nom_type, 'triple')
        self.assertEqual(chambreDTOCree.type_chambre.prix_plancher, 210)
        self.assertEqual(chambreDTOCree.type_chambre.prix_plafond, 320)
        self.assertEqual(chambreDTOCree.type_chambre.description_chambre, 'Chambre avec un gros lit')
        

        with Session(engine) as session:
            stmt = delete(Chambre).where(Chambre.id_chambre == '1776E513-BB05-41D9-B22E-0073772A006A')
            session.execute(stmt)
            session.commit()



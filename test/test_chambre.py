import urllib
import unittest
import modele 
from modele.chambre import Chambre
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select

import logging
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel (logging.INFO)

#Dans des vrais tests unitaires en entreprises, on n'utilise pas la vraie BD lors de tests unitaires. 
#On utilise plutôt un BD in-memory' qui est initialisé au début du test et complètement détruite lorsque 
#le/les tests sont complétés. Pour les besoins du cours (i.e. le est temps limité) on va utiliser une seule BD 
#soit celle qui est déjà créé dans le process SQLEXPRESS. Dépendemment de votre version de sql server express 
#la chaîne de connection peut être différente.


#La chaîne de connection ci-bas servait lorsque j'utilisais une version antérieure de SQL Server Express. #engine - create_engine("mssql+pyodbc://localhost\\sqlexpress01/Hotel?driver-SQL Server', use_setinputsizes=False) #Cette chaione de connection est utilisée pour SQL Server Express 17.


#engine = create_engine(f"mssql+pyodbc://158.69.208.232\\SQLEXPRESS/Hotels?driver=ODBC+Drivers+17+for+SQL+Server" )

#engine = create_engine("mssql+pyodbc://158.69.208.232\\SQLEXPRESS/Hotel?driver=ODBC+Driver+17+for+SQL+Server", use_setinputsizes=False)

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

class test_chambre(unittest.TestCase):
    def test_getChambreParNumero(self):
        with Session(engine) as session:
            stmt = select(Chambre).where(Chambre.numero_chambre == 243)
            chambre = session.execute(stmt).scalar_one()
            self.assertEqual(chambre.numero_chambre, 243)
            self.assertIsNone (chambre.autre_informations)
            self.assertTrue(chambre.disponible_reservation)
            self.assertEqual(chambre.id_chambre, 'E5872679-D5AB-4A4D-8090-C0AFCC6D47C0')
            self.assertEqual(chambre.type_chambre.nom_type, 'VIP')
            self.assertEqual(chambre.type_chambre.prix_plancher, 400.00)
            self.assertEqual(chambre.type_chambre.prix_plafond, 1220.00)
            self.assertEqual(chambre.type_chambre.description_chambre, 'Pour le monde qui on trops dargent')
            self.assertEqual(chambre.type_chambre.id_type_chambre, '12633C57-4790-4516-BFC5-BD0E5A3C920C')

                                 
#TODO: Tester tous les champs et toutes les relations des 3 autres classes.
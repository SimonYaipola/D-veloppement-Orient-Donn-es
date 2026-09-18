import urllib
import unittest
import modele 
from modele.chambre import Client
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select

import logging
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel (logging.INFO)

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

class test_client(unittest.TestCase):
    def test_Unclient(self):
        with Session(engine) as session:
            stmt = select(Client).where(Client.id_client == 'EC50134D-372B-4DFD-9627-02BE06BA6BD6')
            client = session.execute(stmt).scalar_one()
            self.assertEqual(client.prenom, 'Pier-Davide')
            self.assertEqual(client.nom, 'Morel')
            self.assertEqual(client.adresse, '80 Bd de Gaspé, QC')
            self.assertEqual(client.mobile, '4183681534')
            self.assertEqual(client.mot_de_passe, 'PDestSolide!')
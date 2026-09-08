import urllib
import unittest
import modele 
from modele.chambre import Typechambre
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select

import logging
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel (logging.INFO)


#Params pour définir les paramètres de connection à la base de données.
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

class TesTypeChambre(unittest.TestCase):
    def test_TypeChambre(self):
        with Session(engine) as session:
            #Sélectionner un type de chambre spécifique à partir de la base de données en utilisant SQLAlchemy.
            stmt = select(Typechambre).where(Typechambre.nom_type ==  'triple')

            
            #Exécuter la requête et récupérer le résultat sous forme d'objet Typechambre.
            type_chambre = session.execute(stmt).scalar_one()

            #Vérifier que les attributs de l'objet Typechambre correspondent aux valeurs attendues.
            self.assertEqual(type_chambre.nom_type, 'triple')

            self.assertEqual(type_chambre.prix_plancher, 200.00)

            self.assertEqual(type_chambre.prix_plafond, 420)

            self.assertEqual(type_chambre.id_type_chambre, '52FC37DF-5454-42AB-BF0F-259C996F3FD5')

            self.assertEqual(type_chambre.description_chambre, 'Chambre avec lit de la taille de guillaume')

       
      




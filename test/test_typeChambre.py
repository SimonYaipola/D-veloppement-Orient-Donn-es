import unittest
import logging
from modele.typeChambre import TypeChambre
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import Session
from engine.connexion import engine

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel (logging.INFO)

with Session(engine) as session:

    class TesTypeChambre(unittest.TestCase):
        def test_TypeChambre(self):
            with Session(engine) as session:
                #Sélectionner un type de chambre spécifique à partir de la base de données en utilisant SQLAlchemy.
                stmt = select(TypeChambre).where(TypeChambre.nom_type ==  'triple')

                
                #Exécuter la requête et récupérer le résultat sous forme d'objet Typechambre.
                type_chambre = session.execute(stmt).scalar_one()

                #Vérifier que les attributs de l'objet Typechambre correspondent aux valeurs attendues.
                self.assertEqual(type_chambre.nom_type, 'triple')

                self.assertEqual(type_chambre.prix_plancher, 200.00)

                self.assertEqual(type_chambre.prix_plafond, 420)

                self.assertEqual(type_chambre.id_type_chambre, '52FC37DF-5454-42AB-BF0F-259C996F3FD5')

                self.assertEqual(type_chambre.description_chambre, 'Chambre avec lit de la taille de guillaume')

        
        




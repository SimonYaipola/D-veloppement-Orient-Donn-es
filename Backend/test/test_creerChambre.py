import unittest
from modele.chambre import Chambre
from modele.typeChambre import TypeChambre
from metier.chambreMetier import creerChambre, ChambreDTO
from sqlalchemy.orm import Session
from sqlalchemy import delete
from uuid import UUID
from sqlalchemy.orm import Session
from engine.connexion import engine

with Session(engine) as session:

    class test_creerChambre(unittest.TestCase):
        def test_creerChambre(self):
            chambreDTO = ChambreDTO(
                Chambre(
                    numero_chambre=501,
                    disponible_reservation=True,
                    autre_informations='lavabo inclut',
                    id_chambre='1776E513-BB05-41D9-B22E-0073772A006A',
                    type_chambre=
                        TypeChambre(
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



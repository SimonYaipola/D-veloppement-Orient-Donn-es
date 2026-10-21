import unittest
from sqlalchemy.orm import Session
from sqlalchemy import select
from modele.chambre import Chambre
from modele.typeChambre import TypeChambre
from metier.chambreMetier import modifierChambre, ChambreDTO
from sqlalchemy.orm import Session
from engine.connexion import engine

with Session(engine) as session:

    class test_modification_Chambre(unittest.TestCase):
        def test_modifierChambre(self):
            with Session(engine) as session:
                numChambre = 294
                stmt = select(Chambre).where(
                    Chambre.numero_chambre == numChambre
                )

                chambreAModifier = session.execute(stmt).scalars().first()

                self.assertIsNotNone(chambreAModifier, "La chambre" + str(numChambre) + " n'existe pas")

                type_chambre = session.get(TypeChambre, chambreAModifier.fk_type_chambre)

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

import unittest
from modele.chambre import Chambre, Typechambre
from metier.chambreMetier import creerChambre, ChambreDTO


class test_creerChambre(unittest.TestCase):
    def test_creerChambre(self):
        chambreDTO = ChambreDTO(
            Chambre(
                numero_chambre=501,
                disponible_reservation=True,
                type_chambre=
                    Typechambre(
                        nom_type='king',
                        prix_plancher=229.0
                    )
            )
        )

        chambreDTOCree = creerChambre(chambreDTO)

        self.assertEqual(chambreDTOCree.numero_chambre, 501)

        # TODO : Ajouter des assertions pour tous les champs afin de s'assurer que le DTO a été
        # construit adéquatement et est complet.

        # TODO : Supprimer la chambre nouvellement créée :
        # importer create_engine et delete de SQLAlchemy. Créer une session et exécuter
        # un statement qui vient deleter la chambre nouvellement créée par le test précédent.
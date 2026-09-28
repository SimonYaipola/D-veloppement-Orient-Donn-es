import unittest
from unittest.mock import patch
from uuid import UUID

from modele.chambre import Chambre, Typechambre
from DTO.chambreDTO import TypechambreDTO
from metier.chambreMetier import creerTypeChambre


class test_creerTypeChambre(unittest.TestCase):
    ## Test pour vérifier que la fonction creerTypeChambre lève une exception ValueError lorsque le nom du type de chambre est vide.
    @patch("metier.chambreMetier.Session")
    def test_creerTypeChambre(self, mockSession):
        typeChambreDTO = TypechambreDTO(
            Typechambre(
                nom_type="test_creation_type",
                prix_plancher=150.0
            )
        )
        ## Appel de la fonction creerTypeChambre avec le DTO de type de chambre.
        typeChambreDTOCree = creerTypeChambre(typeChambreDTO)
        
        self.assertEqual(typeChambreDTOCree.nom_type, "test_creation_type")
        self.assertEqual(typeChambreDTOCree.prix_plancher, 150.0)

        session = mockSession.return_value.__enter__.return_value
        session.add.assert_called_once()
        session.commit.assert_called_once()
        ## Vérification que l'objet Typechambre ajouté à la session a les attributs corrects et que l'ID est un UUID valide.
        typeAjoute = session.add.call_args.args[0]
        self.assertEqual(typeAjoute.nom_type, "test_creation_type")
        self.assertEqual(typeAjoute.prix_plancher, 150.0)
        UUID(str(typeAjoute.id_type_chambre))
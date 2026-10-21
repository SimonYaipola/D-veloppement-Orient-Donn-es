import unittest
from unittest.mock import patch
from uuid import UUID
from modele.typeChambre import TypeChambre
from DTO.typechambreDTO import TypeChambreDTO
from metier.typeChambreMetier import creerTypeChambre

class test_creerTypeChambre(unittest.TestCase):
    # Vérifie la création d'un type de chambre et le DTO retourné.
    @patch("metier.typeChambreMetier.Session")
    def test_creerTypeChambre(self, mockSession):
        typeChambreDTO = TypeChambreDTO(
            TypeChambre(
                nom_type="test_creation_type",
                prix_plafond=250.0,
                prix_plancher=150.0,
                description_chambre="Chambre de test"
            )
        )
        ## Appel de la fonction creerTypeChambre avec le DTO de type de chambre.
        typeChambreDTOCree = creerTypeChambre(typeChambreDTO)
        
        self.assertEqual(typeChambreDTOCree.nom_type, "test_creation_type")
        self.assertEqual(typeChambreDTOCree.prix_plafond, 250.0)
        self.assertEqual(typeChambreDTOCree.prix_plancher, 150.0)
        self.assertEqual(typeChambreDTOCree.description_chambre, "Chambre de test")
        self.assertIsInstance(typeChambreDTOCree.id_type_chambre, UUID)


        session = mockSession.return_value.__enter__.return_value
        session.add.assert_called_once()
        session.commit.assert_called_once()
        ## Vérification que l'objet Typechambre ajouté à la session a les attributs corrects et que l'ID est un UUID valide.
        typeAjoute = session.add.call_args.args[0]
        self.assertEqual(typeAjoute.nom_type, "test_creation_type")
        self.assertEqual(typeAjoute.prix_plafond, 250.0)
        self.assertEqual(typeAjoute.prix_plancher, 150.0)
        self.assertEqual(typeAjoute.description_chambre,"Chambre de test",)
        self.assertEqual(typeChambreDTOCree.id_type_chambre,UUID(typeAjoute.id_type_chambre),
)
        UUID(str(typeAjoute.id_type_chambre))

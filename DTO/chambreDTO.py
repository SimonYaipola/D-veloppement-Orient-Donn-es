from typing import Optional
from pydantic import BaseModel
import sqlalchemy
from modele.table import Typechambre, Chambre
from uuid import UUID
from datetime import datetime

# Data Transfert Object : pydantic BaseModel pour intégration facile avec FastAPI.
# Facilite aussi grandement la sérialization et la validation des données contenues dans les DTOs.

class TypechambreDTO(BaseModel):
    try: 
        id_type_chambre: Optional[UUID] = None
        nom_type: str
        prix_plafond: Optional[float] = None
        prix_plancher: float
        description_chambre: Optional[str] = None

        def __init__(self, typeChambre: Typechambre = None):
            
            super().__init__(
                id_type_chambre=typeChambre.id_type_chambre,
                nom_type=typeChambre.nom_type,
                prix_plafond=typeChambre.prix_plafond,
                prix_plancher=typeChambre.prix_plancher,
                description_chambre=typeChambre.description_chambre
            )
        if (len(nom_type) > 50 ) :
            raise NameError(f"Erreur de Longueur de nom_type")
        if (prix_plafond >= prix_plancher) :
            raise ValueError(f"Erreur de valeur des prix de la chambre")
        if (len(description_chambre) > 200 ) :
            raise NameError(f"Erreur de Longueur de description_chambre")

        
    except ValueError as ve :
        print(f"Erreur de valeur: {ve}")
    except NameError as ne :
        print(f"Erreur de nom/string: {ne}")
    except sqlalchemy.exc.DatabaseError as dbe :
        print(f"Erreur d'opérations dans la DB: {dbe}")
    except sqlalchemy.exc.StatementError as se :
        print(f"Erreur de statement: {se}")
    except Exception as e :
        print(f"Exception lors de ChambreDTO: {e}")


class ChambreDTO(BaseModel):
    try: 
        idChambre: Optional[UUID] = None
        numero_chambre: int = ()
        disponible_reservation: bool
        autre_informations: Optional[str] = None
        type_chambre: TypechambreDTO

        def __init__(self, chambre: Chambre = None):
            super().__init__(
                idChambre=chambre.id_chambre,
                numero_chambre=chambre.numero_chambre,
                disponible_reservation=chambre.disponible_reservation,
                autre_informations=chambre.autre_informations,
                type_chambre=TypechambreDTO(chambre.type_chambre)
            )

        if (numero_chambre > 0) :
            raise ValueError(f"Erreur de valeur dans numero_chambre")
        
        if (len(autre_informations) > 500 ) :
            raise NameError(f"Erreur de Longueur de autre_information")
        
        if (len(type_chambre) > len("52FC37DF-5454-42AB-BF0F-259C996F3FD5")) :
            raise NameError(f"Erreur dans la clé type_chambre")
        
    except ValueError as ve :
        print(f"Erreur de valeur: {ve}")
    except NameError as ne :
        print(f"Erreur de nom/string: {ne}")
    except sqlalchemy.exc.DatabaseError as dbe :
        print(f"Erreur d'opérations dans la DB: {dbe}")
    except sqlalchemy.exc.StatementError as se :
        print(f"Erreur de statement: {se}")
    except Exception as e :
        print(f"Exception lors de ChambreDTO: {e}")
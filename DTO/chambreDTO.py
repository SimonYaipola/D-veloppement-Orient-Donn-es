from typing import Optional
from pydantic import BaseModel, Field, field_validator, model_validator
from modele.table import Typechambre, Chambre
from uuid import UUID
from datetime import datetime


# Data Transfert Object : pydantic BaseModel pour intégration facile avec FastAPI.
# Facilite aussi grandement la sérialization et la validation des données contenues dans les DTOs.

class TypeChambreDTO(BaseModel):
    id_type_chambre: Optional[UUID] = None
    nom_type: str = Field(min_length=1, max_length=50, strict=True)
    prix_plafond: Optional[float] = Field( default=None, ge=0, allow_inf_nan=False)
    prix_plancher: float = Field(ge=0, allow_inf_nan=False)
    description_chambre: Optional[str] = None

    def __init__(self, typeChambre: Typechambre = None):
        super().__init__(
            id_type_chambre=typeChambre.id_type_chambre,
            nom_type=typeChambre.nom_type,
            prix_plafond=typeChambre.prix_plafond,
            prix_plancher=typeChambre.prix_plancher,
            description_chambre=typeChambre.description_chambre
        )
    #Retire les espace avant la vérification de la longueur du nom_type 
    @field_validator("nom_type", mode="before")
    @classmethod
    def nettoyer_nom_type(cls, valeur):
        if isinstance(valeur, str):
            return valeur.strip()
        return valeur
    #Erreur si le prix_plafond est inférieur au prix_plancher
    @model_validator(mode="after")
    def valider_ordre_prix(self):
        if(
            self.prix_plafond is not None
            and self.prix_plafond < self.prix_plancher
        ):
            raise ValueError("Le prix plafond doit être supérieur ou égal au prix plancher.")
        return self
    


class ChambreDTO(BaseModel):
    idChambre: Optional[UUID] = None
    numero_chambre: int = Field(gt=0, strict=True)
    disponible_reservation: bool = Field(strict=True)
    autre_informations: Optional[str] = None
    type_chambre: TypeChambreDTO

    def __init__(self, chambre: Chambre = None):
        super().__init__(
            idChambre=chambre.id_chambre,
            numero_chambre=chambre.numero_chambre,
            disponible_reservation=chambre.disponible_reservation,
            autre_informations=chambre.autre_informations,
            type_chambre=TypeChambreDTO(chambre.type_chambre)
        )
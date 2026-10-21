from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, field_validator, model_validator
from modele.typeChambre import TypeChambre

# Data Transfert Object : pydantic BaseModel pour intégration facile avec FastAPI.
# Facilite aussi grandement la sérialization et la validation des données contenues dans les DTOs.

class TypeChambreDTO(BaseModel):
    id_type_chambre: Optional[UUID] = None
    nom_type: str = Field(min_length=1, max_length=50, strict=True)
    prix_plafond: Optional[float] = Field( default=None, ge=0, allow_inf_nan=False)
    prix_plancher: float = Field(ge=0, allow_inf_nan=False)
    description_chambre: Optional[str] = None

    def __init__(self, typeChambre: TypeChambre = None):
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
    
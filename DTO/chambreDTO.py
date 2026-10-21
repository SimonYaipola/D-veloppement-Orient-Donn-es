from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from modele.table import Chambre
from DTO.typechambreDTO import TypeChambreDTO



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
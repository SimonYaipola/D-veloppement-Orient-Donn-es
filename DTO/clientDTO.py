from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from modele.table import Client

class clientDTO(BaseModel):
    nom_client: str = Field(min_length=1, max_length=50, strict=True)
    prenom_client: str = Field(min_length=1, max_length=50, strict=True)
    adresse_client: str = Field(min_length=1, max_length=100, strict=True)
    mot_de_passe_client: str = Field(min_length=1, max_length=60, strict=True)
    mobile_client: str = Field(min_length=1, max_length=15, strict=True)
    id_client: Optional[UUID] = None

    def __init__(self, client: Client = None):
        super().__init__(
            nom_client=client.nom,
            prenom_client=client.prenom,
            adresse_client=client.adresse,
            mot_de_passe_client=client.mot_de_passe,
            mobile_client=client.mobile,
            id_client=client.id_client
        )

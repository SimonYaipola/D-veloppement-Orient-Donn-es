from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, field_validator, model_validator
from modele.table import Reservation
from DTO.clientDTO import ClientDTO
from DTO.chambreDTO import ChambreDTO
from datetime import date

class ReservationCreerDTO(BaseModel):
    date_debut_reservation: date
    date_fin_reservation: date
    prix_jour: float
    info_reservation: str
    id_reservation: Optional[UUID] = None
    id_client: UUID
    id_chambre: UUID

    @model_validator(mode="after")
    def valider_ordre_date(self):
        if self.date_fin_reservation < self.date_debut_reservation:
            raise ValueError("La date de fin doit être postérieure ou égale à la date de début.")
        return self

class ReservationDTO(BaseModel):
    date_debut_reservation: date
    date_fin_reservation: date
    prix_jour: float = Field(ge=0, allow_inf_nan=False)
    info_reservation: str
    id_reservation: UUID

    client: clientDTO
    chambre: ChambreDTO

    numero_reservation: int

    def __init__(self, reservation: Reservation = None):
        super().__init__(
            date_fin_reservation=reservation.date_fin_reservation,
            date_debut_reservation=reservation.date_debut_reservation,
            prix_jour=reservation.prix_jour,
            info_reservation=reservation.info_reservation,
            id_reservation=reservation.id_reservation,
            client=clientDTO(reservation.client),
            chambre=ChambreDTO(reservation.chambre),
            numero_reservation=reservation.numero_reservation
        )

    #Valider que le prix par jour est supérieur à 0 
    @model_validator(mode="after")
    def valider_prix_jour(self):
        if(
            self.prix_jour is not None
            and self.prix_jour < 0
        ):
            raise ValueError("Le prix par jour doit être supérieur à 0.")
        return self
        
    #Valider que la date de fin est après la date du début
    @model_validator(mode="after")
    def valider_ordre_date(self):
        if(
            self.date_fin_reservation < self.date_debut_reservation
        ):
            raise ValueError("La date de fin doit être postérieure ou égale à la date du début.")
        
        return self
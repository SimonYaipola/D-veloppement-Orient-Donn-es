from datetime import date
from uuid import UUID

from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from sqlalchemy import String
import DTO.reservationDTO
from metier.reservationMetier import creerReservation, rechercherReservation, modifierReservation, supprimerReservation
from DTO.chambreDTO import TypeChambreDTO
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/creerReservation")
def read_item(date_debut: date, date_fin: date, prix_jour: float, info_reservation: str, id_client: str, id_chambre: str, numero_reservation: int):
    try:
        reservation = DTO.reservationDTO.ReservationCreerDTO(
                    date_debut_reservation=date_debut,
                    date_fin_reservation=date_fin,
                    prix_jour=prix_jour,
                    info_reservation=info_reservation,
                    id_client=UUID(id_client),
                    id_chambre=UUID(id_chambre),
                    numero_reservation=numero_reservation
                )
        return creerReservation(reservation)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))

@app.get("/rechercherReservation")
def read_item(no_reservation: int, no_chambre: int | None = None):
    try:
        return rechercherReservation(no_reservation, no_chambre)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))

@app.post("/modifierReservation")
def read_item(numero_reservation: int, date_debut: date | None = None, date_fin: date | None = None, prix_jour: float | None = None, info_reservation: str | None = None, id_chambre: str | None = None):
    DTOAModifier = rechercherReservation(numero_reservation)
    
    if (date_debut != None):
        DTOAModifier.date_debut_reservation = date_debut

    if (date_fin != None):
        DTOAModifier.date_fin_reservation = date_fin

    if (prix_jour != None):
        DTOAModifier.prix_jour = prix_jour

    if (info_reservation != None):
        DTOAModifier.info_reservation = info_reservation

    if (id_chambre != None):
        DTOAModifier.id_chambre = id_chambre
    try:
    
        return modifierReservation(DTOAModifier, str(id_chambre) if id_chambre else None)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))

@app.delete("/supprimerReservation")
def read_item(no_reservation: int):
    try:
        return supprimerReservation(no_reservation)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))
uvicorn.run (app, host="127.0.0.1", port=8000)
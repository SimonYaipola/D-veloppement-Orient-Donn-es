from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from metier.chambreMetier import creerChambre, getChambreParNumero, ChambreDTO
from metier.typeChambreMetier import creerTypeChambre, TypeChambreDTO
from DTO.chambreDTO import TypeChambreDTO
from metier.reservationMetier import rechercherReservation
from metier.clientMetier import creerClient, modifierClient, rechercherClient, supprimerClient
from DTO.clientDTO import ClientDTO
#from DTO.CriteresRechercheDTO
from fastapi.middleware.cors import CORSMiddleware
from uuid import UUID
import uuid
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/chambre/(no_chambe)")
def read_item(no_chambre: int):
    try:
        return getChambreParNumero(no_chambre)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))

@app.post("/creerTypeChambre")
def read_item(type: TypeChambreDTO):
    try:
        return creerTypeChambre(type)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))

#@app.post("/rechercherReservation")
#def read_item(critere: CriteresRechercheDTO):
#    try:
#        return rechercherReservation(critere)
#    except ValueError as e:
#        return HTTPException(status_code=404, detail=str(e))

@app.post("/creerClient")
def read_item(client: ClientDTO):
    try:
        return creerClient(client)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))

@app.post("/modifierClient")
def read_item(client: ClientDTO):
    try:
        return modifierClient(client)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))

@app.get("/rechercherClient")
def read_item(id_client: UUID):
    try:
        return rechercherClient(id_client)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))

@app.get("/supprimerClient")
def read_item(id_client: UUID):
    try:
        return supprimerClient(id_client)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))


uvicorn.run (app, host="127.0.0.1", port=8000)
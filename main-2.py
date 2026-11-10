from typing import Optional
from uuid import UUID

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import NoResultFound

from DTO.chambreDTO import ChambreDTO
from DTO.typechambreDTO import TypeChambreDTO
from metier.chambreMetier import (
    creerChambre,
    getChambreParNumero,
    modifierChambre,
    supprimerChambre,
)
from metier.typeChambreMetier import (
    creerTypeChambre,
    rechercherTypeChambre,
    modifierTypeChambre,
    supprimerTypeChambre,
)
from metier.reservationMetier import ReservationDTO
from fastapi import FastAPI, HTTPException

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Chambre ----------

@app.get("/chambre/{no_chambre}")
def rechercher_chambre(no_chambre: int):
    try:
        chambre = getChambreParNumero(no_chambre)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    if chambre is None:
        raise HTTPException(status_code=404, detail="Chambre introuvable.")
    return chambre

@app.post("/creerChambre", status_code=201)
def creer_chambre(numero_chambre: int, disponible_reservation: bool,
                  id_type_chambre: UUID,
                  autre_informations: Optional[str] = None):
    try:
        type_chambre = rechercherTypeChambre(id_type_chambre)
        chambre = ChambreDTO(
            numero_chambre=numero_chambre,
            disponible_reservation=disponible_reservation,
            autre_informations=autre_informations,
            type_chambre=type_chambre
        )
        return creerChambre(chambre)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@app.put("/modifierChambre")
def modifier_chambre(id_chambre: UUID, numero_chambre: int, disponible_reservation: bool,
                     id_type_chambre: UUID,
                     autre_informations: Optional[str] = None):
    try:
        type_chambre = rechercherTypeChambre(id_type_chambre)
        chambre = ChambreDTO(
            idChambre=id_chambre,
            numero_chambre=numero_chambre,
            disponible_reservation=disponible_reservation,
            autre_informations=autre_informations,
            type_chambre=type_chambre
        )
        return modifierChambre(chambre)
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail="Chambre introuvable.") from e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@app.delete("/supprimerChambre/{id_chambre}")
def supprimer_chambre(id_chambre: UUID):
    try:
        supprimerChambre(id_chambre)
        return {"message": "Chambre supprimée."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

# ---------- Type de chambre ----------

@app.post("/creerTypeChambre", status_code=201)
def creer_type_chambre(nom_type: str, prix_plancher: float,
                       prix_plafond: Optional[float] = None,
                       description_chambre: Optional[str] = None):
    try:
        type_chambre = TypeChambreDTO(
            nom_type=nom_type,
            prix_plancher=prix_plancher,
            prix_plafond=prix_plafond,
            description_chambre=description_chambre
        )
        return creerTypeChambre(type_chambre)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.get("/rechercherTypeChambre/{id_type_chambre}")
def rechercher_type_chambre(id_type_chambre: UUID):
    try:
        return rechercherTypeChambre(id_type_chambre)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

@app.put("/modifierTypeChambre")
def modifier_type_chambre(id_type_chambre: UUID, nom_type: str, prix_plancher: float,
                          prix_plafond: Optional[float] = None,
                          description_chambre: Optional[str] = None):
    try:
        type_chambre = TypeChambreDTO(
            id_type_chambre=id_type_chambre,
            nom_type=nom_type,
            prix_plancher=prix_plancher,
            prix_plafond=prix_plafond,
            description_chambre=description_chambre
        )
        return modifierTypeChambre(type_chambre)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@app.delete("/supprimerTypeChambre/{id_type_chambre}")
def supprimer_type_chambre(id_type_chambre: UUID):
    try:
        supprimerTypeChambre(id_type_chambre)
        return {"message": "Type de chambre supprimé."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

# ---------- Réservation  ----------

@app.get("/rechercherReservation")
def rechercher_reservation(critere: int):
    try:
        return ReservationDTO(critere)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


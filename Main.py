from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import uvicorn
import fastapi
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
from fastapi import status
from fastapi import Form, status
from pydantic import ValidationError
from datetime import date
from typing import Optional
from uuid import UUID

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import String
from sqlalchemy.exc import NoResultFound

import DTO.reservationDTO
from DTO.chambreDTO import ChambreDTO
from DTO.typechambreDTO import TypeChambreDTO
from metier.chambreMetier import (
    creerChambre,
    getChambreParNumero,
    modifierChambre,
    supprimerChambre,
)
from metier.reservationMetier import (
    ReservationDTO,
    creerReservation,
    modifierReservation,
    rechercherReservation,
    supprimerReservation,
)
from metier.typeChambreMetier import (
    creerTypeChambre,
    modifierTypeChambre,
    rechercherTypeChambre,
    supprimerTypeChambre,
)


fake_users_db = {
    "johndoe":{
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret"
    },
    "simon":{
        "username": "simon",
        "full_name": "Simon-Pierre Larouche",
        "email": "simonpierre@bienecrit.com",
        "hashed_password": "fakehashedsimonpierre"
    },
}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return{"access_token": user.username, "token_type": "bearer"}

def fake_hash_password(password: str):
    return "fakehashed" + password

def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

class User (BaseModel):
    username: str
    email: str | None = None
    full_name: str |None = None

class UserInDB(User):
    hashed_password: str

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# ---------- Chambre ----------

@app.get("/chambre/{no_chambre}")
def rechercher_chambre(current_user: Annotated[User, Depends(get_current_user)], no_chambre: int):
    try:
        chambre = getChambreParNumero(no_chambre)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    if chambre is None:
        raise HTTPException(status_code=404, detail="Chambre introuvable.")
    return chambre

@app.post("/creerChambre", status_code=201)
def creer_chambre(current_user: Annotated[User, Depends(get_current_user)],
                  numero_chambre: int, disponible_reservation: bool,
                  id_type_chambre: UUID,
                  autre_informations: Optional[str] = None
                  ):
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
def modifier_chambre(current_user: Annotated[User, Depends(get_current_user)],
                     id_chambre: UUID, numero_chambre: int, disponible_reservation: bool,
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
def supprimer_chambre(current_user: Annotated[User, Depends(get_current_user)], id_chambre: UUID):
    try:
        supprimerChambre(id_chambre)
        return {"message": "Chambre supprimée."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

# ---------- Type de chambre ----------

@app.post("/creerTypeChambre", status_code=201)
def creer_type_chambre(current_user: Annotated[User, Depends(get_current_user)],
                       nom_type: str, prix_plancher: float,
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
def rechercher_type_chambre(current_user: Annotated[User, Depends(get_current_user)], id_type_chambre: UUID):
    try:
        return rechercherTypeChambre(id_type_chambre)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

@app.put("/modifierTypeChambre")
def modifier_type_chambre(current_user: Annotated[User, Depends(get_current_user)],
                          id_type_chambre: UUID, nom_type: str, prix_plancher: float,
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
def supprimer_type_chambre(current_user: Annotated[User, Depends(get_current_user)], id_type_chambre: UUID):
    try:
        supprimerTypeChambre(id_type_chambre)
        return {"message": "Type de chambre supprimé."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

# ---------- Réservation  ----------

@app.post("/creerReservation")
def read_item(current_user: Annotated[User, Depends(get_current_user)], date_debut: date, date_fin: date, prix_jour: float, info_reservation: str, id_client: str, id_chambre: str, numero_reservation: int):
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
def read_item(current_user: Annotated[User, Depends(get_current_user)], no_reservation: int, no_chambre: int | None = None):
    try:
        return rechercherReservation(no_reservation, no_chambre)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))

@app.post("/modifierReservation")
def read_item(current_user: Annotated[User, Depends(get_current_user)], numero_reservation: int, date_debut: date | None = None, date_fin: date | None = None, prix_jour: float | None = None, info_reservation: str | None = None, id_chambre: str | None = None):
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
def read_item(current_user: Annotated[User, Depends(get_current_user)], no_reservation: int):
    try:
        return supprimerReservation(no_reservation)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))

    # ---------- Client ----------

# Empêche les données invalide du dto
def leClientDTO(**champs) -> ClientDTO:
    try:
        return ClientDTO(**champs)
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail=[f"{err['loc'][0]} : {err['msg']}" for err in e.errors()],
        )

@app.post("/creerClient", status_code=201)
def creer_client(
    current_user: Annotated[User, Depends(get_current_user)],
    nom_client: Annotated[str, Form()],
    prenom_client: Annotated[str, Form()],
    adresse_client: Annotated[str, Form()],
    mot_de_passe_client: Annotated[str, Form()],
    mobile_client: Annotated[str, Form()],
    ):
    try:
        client = leClientDTO(
            nom_client=nom_client,
            prenom_client=prenom_client,
            adresse_client=adresse_client,
            mot_de_passe_client=mot_de_passe_client,
            mobile_client=mobile_client,
            )
        return creerClient(client)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))

@app.put("/modifierClient/{id_client}")
def modifier_client(
    current_user: Annotated[User, Depends(get_current_user)],
    id_client: UUID,
    nom_client: Annotated[str, Form()],
    prenom_client: Annotated[str, Form()],
    adresse_client: Annotated[str, Form()],
    mot_de_passe_client: Annotated[str, Form()],
    mobile_client: Annotated[str, Form()],
    ):
    try:
        client = leClientDTO(
        id_client=id_client,
        nom_client=nom_client,
        prenom_client=prenom_client,
        adresse_client=adresse_client,
        mot_de_passe_client=mot_de_passe_client,
        mobile_client=mobile_client,
    )
        return modifierClient(client)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))

@app.get("/rechercherClient/{id_client}")
def rechercher_client(
    id_client: UUID,
    current_user: Annotated[User, Depends(get_current_user)]
    ):
    try:
        return rechercherClient(id_client)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))

@app.delete("/supprimerClient{id_client}")
def supprimer_client(
    id_client: UUID,
    current_user: Annotated[User, Depends(get_current_user)]):
    try:
        return supprimerClient(id_client)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))


uvicorn.run (app, host="127.0.0.1", port=8000)
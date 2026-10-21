from uuid import uuid4

from sqlalchemy.orm import Session
from DTO.clientDTO import ClientDTO
from engine.connexion import engine
from sqlalchemy import create_engine, select, update
from modele.client import Client
from uuid import UUID
import uuid


def creerClient(client: ClientDTO):

    with Session(engine) as session:
        stmt = select(Client).where(
            Client.mobile == client.mobile_client
        )
        if session.execute(stmt).scalars().first() is not None:
            raise ValueError("Un client avec ce numéro de mobile existe déjà.")
        
        if client.id_client is None:
            client.id_client = uuid.uuid4()

        nouveauClient = Client(
            nom_client=client.nom,
            prenom_client=client.prenom,
            adresse_client=client.adresse,
            mot_de_passe_client=client.mot_de_passe,
            mobile_client=client.mobile,
            id_client=client.id_client,
        )

        session.add(nouveauClient)
        session.commit()

        return ClientDTO(nouveauClient)


def modifierClient():
    return

def rechercherClient():
    return

def supprimerClient():
    return
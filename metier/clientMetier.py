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


def modifierClient(client: ClientDTO):
    if client.id_client is None:
        raise ValueError("L'identifiant du client est obligatoire.")

    with Session(engine) as session:
        clientAModifier = session.get(
            Client,
            str(client.id_client).upper(),
        )

        if clientAModifier is None:
            raise ValueError("Le client est introuvable.")

        stmt = select(Client).where(
            Client.mobile == client.mobile_client,
            Client.id_client != clientAModifier.id_client,
        )
        if session.execute(stmt).scalars().first() is not None:
            raise ValueError("Un autre client utilise déjà ce numéro de mobile.")

        clientAModifier.nom = client.nom_client
        clientAModifier.prenom = client.prenom_client
        clientAModifier.adresse = client.adresse_client
        clientAModifier.mot_de_passe = client.mot_de_passe_client
        clientAModifier.mobile = client.mobile_client

        session.commit()
        session.refresh(clientAModifier)

        return ClientDTO(clientAModifier)

def rechercherClient(id_client: UUID):
    if id_client is None:
        raise ValueError("L'identifiant du client est obligatoire.")

    with Session(engine) as session:
        clientTrouve = session.get(
            Client,
            str(id_client).upper(),
        )

        if clientTrouve is None:
            raise ValueError("Le client est introuvable.")

        return ClientDTO(clientTrouve)

def supprimerClient(id_client: UUID):
    if id_client is None:
        raise ValueError("L'identifiant du client est obligatoire.")

    with Session(engine) as session:
        clientASupprimer = session.get(
            Client,
            str(id_client).upper(),
        )
        if clientASupprimer is None:
            raise ValueError("Le client est introuvable.")
        if clientASupprimer.reservations:
            raise ValueError("Ce client a des réservations.")

        session.delete(clientASupprimer)
        session.commit()
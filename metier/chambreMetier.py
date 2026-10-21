
from uuid import uuid4

from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select, update
from DTO.chambreDTO import ChambreDTO, TypechambreDTO
from DTO.clientDTO import clientDTO
from DTO.reservationDTO import Reservation
from modele.table import Chambre, Typechambre
from modele.client import Client
from DTO.chambreDTO import ChambreDTO
from DTO.typechambreDTO import TypeChambreDTO
from modele.table import Chambre
from modele.typeChambre import Typechambre
from uuid import UUID
import urllib
import uuid



# engine = create_engine(
#     "mssql+pyodbc://localhost\\sqlexpress01/Hotel?driver=SQL Server",
#     use_setinputsizes=False
# )

server = '158.69.208.232,1433'
database = 'Hotels'
username = 'sa'
password = 'Automne,2026'
params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
)


engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}",
    use_setinputsizes=False
)


def creerChambre(chambre: ChambreDTO):
    if chambre.numero_chambre is None or chambre.disponible_reservation is None or chambre.autre_informations is None or chambre.type_chambre is None or chambre.type_chambre.nom_type is None:
        raise ValueError ("Tous les champs doivent être remplis sauf id_chambre qui est facultatif.")
    if type (chambre.numero_chambre) is not int or chambre.numero_chambre <= 0:
        raise ValueError ("Le numéro de chambre dois être un entier positif.")
    if type (chambre.disponible_reservation) is not bool:
        raise TypeError ("La disponibilité de la réservation doit être un booléen.")
    if type (chambre.autre_informations) is not str:
        raise TypeError ("Les autres informations doivent être du texte.")

    with Session(engine) as session:
        stmt = select(Typechambre).where(
            Typechambre.nom_type == chambre.type_chambre.nom_type
        )
        typeChambre = session.execute(stmt).scalars().first()
        
        if chambre.idChambre is None:
            chambre.idChambre = uuid.uuid4()

        nouvelleChambre = Chambre(
            numero_chambre=chambre.numero_chambre,
            disponible_reservation=chambre.disponible_reservation,
            autre_informations=chambre.autre_informations,
            id_chambre=str(chambre.idChambre).upper(),
            fk_type_chambre=str(typeChambre.id_type_chambre).upper(),
        )

        session.add(nouvelleChambre)
        session.commit()

        return chambre


def creerTypeChambre(typeChambre: TypechambreDTO):
    nom = typeChambre.nom_type.strip() if typeChambre.nom_type else ""

    if not nom:
        raise ValueError("Le nom du type de chambre ne peut pas être vide.")
    if len(nom) > 50:
        raise ValueError("Le nom du type de chambre ne peut pas dépasser 50 caractères.")
    if typeChambre.prix_plancher is None or typeChambre.prix_plancher < 0:
        raise ValueError("Le prix plancher doit être un nombre positif.")
    
    # TODO : Ajouter gestion des erreurs. On va voir un exemple au prochain cours.
    with Session(engine) as session:
        nouveauTypeChambre = Typechambre(
            id_type_chambre=str(uuid4()).upper(),
            nom_type=nom,
            prix_plancher=typeChambre.prix_plancher,
            prix_plafond=typeChambre.prix_plafond,
            description_chambre=typeChambre.description_chambre,
        )

        session.add(nouveauTypeChambre)
        session.commit()
        session.refresh(nouveauTypeChambre)

        return TypeChambreDTO(nouveauTypeChambre)

def modifierTypeChambre(typeChambre: TypeChambreDTO):
    if typeChambre.id_type_chambre is None:
        raise ValueError("L'identifiant du type de chambre est obligatoire.")

    with Session(engine) as session:
        typeAModifier = session.get(
            Typechambre,
            str(typeChambre.id_type_chambre).upper(),
        )

        if typeAModifier is None:
            raise ValueError("Le type de chambre est introuvable.")

        typeAModifier.nom_type = typeChambre.nom_type
        typeAModifier.prix_plancher = typeChambre.prix_plancher
        typeAModifier.prix_plafond = typeChambre.prix_plafond
        typeAModifier.description_chambre = (
            typeChambre.description_chambre
        )

        session.commit()
        session.refresh(typeAModifier)

        return TypeChambreDTO(typeAModifier)


def rechercherTypeChambre(id_type_chambre: UUID):
    if id_type_chambre is None:
        raise ValueError(
            "L'identifiant du type de chambre est obligatoire."
        )

    with Session(engine) as session:
        type_trouve = session.get(
            Typechambre,
            str(id_type_chambre).upper(),
        )

        if type_trouve is None:
            raise ValueError("Le type de chambre est introuvable.")

        return TypeChambreDTO(type_trouve)
def supprimerTypeChambre(id_type_chambre: UUID):
    if id_type_chambre is None:
        raise ValueError(
            "L'identifiant du type de chambre est obligatoire."
        )

    with Session(engine) as session:
        type_a_supprimer = session.get(
            Typechambre,
            str(id_type_chambre).upper(),
        )

        if type_a_supprimer is None:
            raise ValueError("Le type de chambre est introuvable.")
        ## Vérifier si le type de chambre est utilisé par une chambre avant de le supprimer.
        if type_a_supprimer.chambre:
            raise ValueError(
                "Ce type de chambre est utilisé par une chambre."
            )

        session.delete(type_a_supprimer)
        session.commit()
def getChambreParNumero(no_chambre: int):
    # TODO : Ajouter des validations au besoin. Ex : no_chambre ne doit pas être null.
    
    if no_chambre is None:
        raise ValueError("Le numéro de chambre ne peut pas être null.")

    if isinstance(no_chambre, bool) or not isinstance(no_chambre, int):
        raise TypeError("Le numéro de chambre doit être un entier.")

    if no_chambre <= 0:
        raise ValueError("Le numéro de chambre doit être un entier positif.")

     # TODO : Ajouter gestion des erreurs. On va voir un exemple au prochain cours.

    with Session(engine) as session:
        stmt = select(Chambre).where(
            Chambre.numero_chambre == no_chambre
        )
        result = session.execute(stmt)

        for chambre in result.scalars():
            return ChambreDTO(chambre)


    
    



def modifierChambre(chambre: ChambreDTO):
    # TODO : Valider que la chambre existe bien dans la BD et autres validations.
    # TODO : Ajouter gestion des erreurs. On va voir un exemple au prochain cours.
    with Session(engine) as session:
        stmt = select(Chambre).where(
            Chambre.id_chambre == chambre.idChambre
        )
        chambreAModifier = session.execute(stmt).scalars().one()

        chambreAModifier.disponible_reservation = chambre.disponible_reservation
        chambreAModifier.autre_informations = chambre.autre_informations
        chambreAModifier.numero_chambre = chambre.numero_chambre
        chambreAModifier.fk_type_chambre = chambre.type_chambre.id_type_chambre

        session.execute(
            update(Chambre).where(Chambre.id_chambre == chambre.idChambre).values(
                disponible_reservation=chambre.disponible_reservation,
                autre_informations=chambre.autre_informations,
                numero_chambre=chambre.numero_chambre,
                fk_type_chambre=chambre.type_chambre.id_type_chambre,
            )
        )
        session.commit()
        return chambre

def creerClient(client: clientDTO):

    with Session(engine) as session:
        stmt = select(Client).where(
            Client.mobile == Client.mobile
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

        return clientDTO(nouveauClient)


def modifierClient():
    return

def rechercherClient():
    return

def supprimerClient():
    return
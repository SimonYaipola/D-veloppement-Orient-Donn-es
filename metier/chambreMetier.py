
from uuid import uuid4

from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select, update
from DTO.chambreDTO import ChambreDTO, TypeChambreDTO
from modele.table import Chambre, Typechambre
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
    # TODO : Générer un uuid et l'assigner à la chambre, si vous n'utilisez pas un auto-increment.   #if null. raise value(ValueError)
    # TODO : Ajouter des validations au besoin. Ex : Lorsque l'on crée une chambre, s'il n'y a pas de numéro de chambre
    # ou si le numéro de chambre existe déjà, on Raise un ValueError.
    # TODO : Ajouter gestion des erreurs. On va voir un exemple au prochain cours.
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


def creerTypeChambre(typeChambre: TypeChambreDTO):
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
            id_type_chambre=str(uuid4()),
            nom_type=nom,
            prix_plancher=typeChambre.prix_plancher
        )

        session.add(nouveauTypeChambre)
        session.commit()

        return typeChambre


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
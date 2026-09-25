from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from DTO.chambreDTO import ChambreDTO, TypechambreDTO
from modele.chambre import Chambre, Typechambre
import urllib


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
    # TODO : Générer un uuid et l'assigner à la chambre, si vous n'utilisez pas un auto-increment.
    # TODO : Ajouter des validations au besoin. Ex : Lorsque l'on crée une chambre, s'il n'y a pas de numéro de chambre
    # ou si le numéro de chambre existe déjà, on Raise un ValueError.
    # TODO : Ajouter gestion des erreurs. On va voir un exemple au prochain cours.
    with Session(engine) as session:
        stmt = select(Typechambre).where(
            Typechambre.nom_type == chambre.type_chambre.nom_type
        )
        result = session.execute(stmt)

        for typeChambre in result.scalars():
            nouvelleChambre = Chambre(
                numero_chambre=chambre.numero_chambre,
                disponible_reservation=chambre.disponible_reservation,
                autre_informations=chambre.autre_informations,
                type_chambre=typeChambre
            )

        session.add(nouvelleChambre)
        session.commit()

        return chambre


def creerTypeChambre(typeChambre: TypechambreDTO):
    # TODO : Générer un uuid et l'assigner à la chambre, si vous n'utilisez pas un auto-increment.
    # TODO : Ajouter des validations au besoin.
    # TODO : Ajouter gestion des erreurs. On va voir un exemple au prochain cours.
    with Session(engine) as session:
        nouveauTypeChambre = Typechambre(
            nom_type=typeChambre.nom_type,
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

        # TODO: Setter les autres champs

        session.commit()
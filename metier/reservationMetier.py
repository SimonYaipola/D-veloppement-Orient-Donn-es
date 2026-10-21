from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select, update
from DTO.reservationDTO import ReservationDTO, ReservationCreerDTO
from DTO.chambreDTO import ChambreDTO
from DTO.clientDTO import clientDTO
from modele.table import Chambre, Reservation, Client
import urllib
import uuid

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

def creerReservation(reservation: ReservationDTO):
    with Session(engine) as session:
        chambre = session.get(Chambre, str(reservation.id_chambre).upper())
        client = session.get(Client, str(reservation.id_client).upper())
        if chambre is None or client is None:
            raise ValueError("Chambre ou client introuvable.")

        nouvelleReservation = Reservation(
            id_reservation=str(uuid.uuid4()).upper(),
            date_debut_reservation=reservation.date_debut_reservation,
            date_fin_reservation=reservation.date_fin_reservation,
            prix_jour=reservation.prix_jour,
            info_reservation=reservation.info_reservation,
            client=client,
            chambre=chambre,
        )

        session.add(nouvelleReservation)
        session.commit()
        session.refresh(nouvelleReservation)
        return ReservationDTO(nouvelleReservation)


def getReservationParNumero(no_reservation: int):
    if no_reservation is None:
        raise ValueError("Le numéro de reservation ne peut pas être null.")

    if isinstance(no_reservation, bool) or not isinstance(no_reservation, int):
        raise TypeError("Le numéro de reservation doit être un entier.")

    if no_reservation <= 0:
        raise ValueError("Le numéro de reservation doit être un entier positif.")

    with Session(engine) as session:
        stmt = select(Reservation).where(
            Reservation.numero_reservation == no_reservation
        )
        result = session.execute(stmt)

        for reservation in result.scalars():
            return ChambreDTO(reservation)


def modifierReservation(reservation: ReservationDTO):
    with Session(engine) as session:
        stmt = select(Reservation).where(
            Reservation.numero_chambre == reservation.numero_chambre
        )
        reservationAModifier = session.execute(stmt).scalars().one()

        reservationAModifier.date_debut_reservation = reservation.date_debut_reservation
        reservationAModifier.date_fin_reservation = reservation.date_fin_reservation
        reservationAModifier.prix_jour = reservation.prix_jour
        reservationAModifier.info_reservation = reservation.info_reservation
        reservationAModifier.fk_id_chambre = reservation.chambre.idChambre

        session.execute(
            update(Reservation).where(Reservation.numero_reservation == reservation.numero_reservation).values(
                date_debut_reservation = reservation.date_debut_reservation,
                date_fin_reservation = reservation.date_fin_reservation,
                prix_jour = reservation.prix_jour,
                info_reservation = reservation.info_reservation,
                fk_id_chambre = reservation.chambre.idChambre
            )
        )
        session.commit()
        return reservation

def supprimerReservation(reservation: Reservation):
    with Session(engine) as session:
        stmt = select(Reservation).where(
            Reservation.numero_chambre == reservation.numero_chambre
        )
        reservationASupprimer = session.execute(stmt).scalars().one()

        session.delete(reservationASupprimer)
        session.commit()
        return reservation
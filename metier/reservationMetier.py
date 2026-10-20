from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select, update
from DTO.reservationDTO import ReservationDTO
from DTO.chambreDTO import ChambreDTO
from DTO.clientDTO import ClientDTO # À LIER AVEC CLIENTDTO !!!!!
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
        stmt = select(Chambre).where(
            Chambre.id_chambre == reservation.id_chambre
        )
        chambre = session.execute(stmt).scalars().first()

        stmt = select(Client).where(
            Client.id_client == reservation.id_client
        )
        client = session.execute(stmt).scalars().first()

        if reservation.id_Reservation is None:
            reservation.id_Reservation = uuid.uuid4()

        nouvelleReservation = Reservation(
            date_fin_reservation=reservation.date_fin_reservation,
            date_debut_reservation=reservation.date_debut_reservation,
            prix_jour=reservation.prix_jour,
            info_reservation=reservation.info_reservation,
            id_reservation=reservation.id_reservation,
            client=client,
            chambre=chambre,
        )

        session.add(nouvelleReservation)
        session.commit()

        return reservation


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
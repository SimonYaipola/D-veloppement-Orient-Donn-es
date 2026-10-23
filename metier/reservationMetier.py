from typing import Optional
import uuid

from sqlalchemy import select, update
from sqlalchemy.orm import Session
from DTO.reservationDTO import ReservationDTO, RechercherReservationDTO
from engine.connexion import engine
from modele.chambre import Chambre
from modele.client import Client
from modele.reservation import Reservation

with Session(engine) as session:

    def creerReservation(reservation: ReservationDTO):
        if reservation is None:
            raise ValueError("Le numéro de chambre ne peut pas être null.")
        
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


    def rechercherReservation(no_reservation: Optional[int], no_chambre: Optional[int]):

        if no_reservation is None or no_chambre is None:
            raise ValueError("Le numéro donné ne peut pas être null.")

        if isinstance(no_reservation, bool) or not isinstance(no_reservation, int):
            raise TypeError("Le numéro donné doit être un entier.")

        if isinstance(no_chambre, bool) or not isinstance(no_chambre, int):
            raise TypeError("Le numéro donné doit être un entier.")

        if no_reservation <= 0 or no_chambre <= 0:
            raise ValueError("Le numéro donné doit être un entier positif.")

        with Session(engine) as session:
            if no_reservation:
                stmt = select(Reservation).where(
                    Reservation.numero_reservation == no_reservation
                )
            else:
                if no_chambre:
                    stmt = select(Reservation.fk_id_chambre, Chambre.id_chambre, Chambre.numero_chambre).join(Chambre, Chambre.id_chambre == Reservation.fk_id_chambre).where(
                        Chambre.numero_chambre == no_chambre
                    )

            
            reservation = session.execute(stmt).scalars().first()
            return ReservationDTO(reservation) if reservation else None


    def modifierReservation(reservation: ReservationDTO):
        with Session(engine) as session:
            stmt = select(Reservation).where(
                Reservation.numero_reservation == reservation.numero_reservation
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
            session.refresh(reservationAModifier)
            return ReservationDTO(reservationAModifier)

    def supprimerReservation(no_reservation: int):
        with Session(engine) as session:
            reservationASupprimer = session.execute(
                select(Reservation).where(Reservation.numero_reservation == no_reservation)).scalars().one()

            session.delete(reservationASupprimer)
            session.commit()
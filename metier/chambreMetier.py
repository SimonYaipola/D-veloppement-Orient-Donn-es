import uuid

from sqlalchemy import select, update
from sqlalchemy.orm import Session
from DTO.chambreDTO import ChambreDTO
from engine.connexion import engine
from modele.chambre import Chambre
from modele.typeChambre import TypeChambre

with Session(engine) as session:


    def creerChambre(chambre: ChambreDTO):
        # TODO : Générer un uuid et l'assigner à la chambre, si vous n'utilisez pas un auto-increment.   #if null. raise value(ValueError)
        # TODO : Ajouter des validations au besoin. Ex : Lorsque l'on crée une chambre, s'il n'y a pas de numéro de chambre
        # ou si le numéro de chambre existe déjà, on Raise un ValueError.
        # TODO : Ajouter gestion des erreurs. On va voir un exemple au prochain cours.
        with Session(engine) as session:
            stmt = select(TypeChambre).where(
                TypeChambre.nom_type == chambre.type_chambre.nom_type
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

    def supprimerChambre(id_chambre: uuid.UUID):
        if id_chambre is None:
            raise ValueError("L'ID de la chambre ne peut pas être null.")

        with Session(engine) as session:
            chambre = session.get(Chambre, str(id_chambre).upper(),
            )

            if chambre is None:
                raise ValueError("La chambre est introuvable.")

            if chambre.reservations:
                raise ValueError("La chambre ne peut pas être supprimée, car elle est associée à une ou plusieurs réservations.")
            session.delete(chambre)
            session.commit()
            
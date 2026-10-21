from uuid import UUID, uuid4

from sqlalchemy.orm import Session
from DTO.typechambreDTO import TypeChambreDTO
from engine.connexion import engine
from modele.typeChambre import TypeChambre

with Session(engine) as session:

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
            nouveauTypeChambre = TypeChambre(
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
                TypeChambre,
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
                TypeChambre,
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
                TypeChambre,
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
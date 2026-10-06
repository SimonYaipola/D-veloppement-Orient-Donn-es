# --- Code du Prof ---

from pyclbr import Class
from typing import List
from sqlalchemy import ForeignKey
import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column

class Base(DeclarativeBase):
    pass

class Chambre(Base):
    __tablename__ = "chambre"

    numero_chambre: Mapped[int]
    disponible_reservation: Mapped[bool]
    autre_informations: Mapped[str]
    id_chambre: Mapped[str] = mapped_column(primary_key=True)

    # Définition de la clé étrangère qui permettra de mapper a classe type_chambre directement dans la classe chambre.
    fk_type_chambre: Mapped[str] = mapped_column(ForeignKey("type_chambre.id_type_chambre"))

    # Relation de 1 à 1 qui sera automatiquement mappé sur SQLAlchemy grâce à la clé étrangàre.
    type_chambre: Mapped['Typechambre'] = relationship()
    # Relation de 1 à N qui sera automatiquement mappé sur SQLAlchemy grâce à la 'relationship()' de la classe Reservation
    reservations: Mapped[List["Reservation"]] = relationship(back_populates="chambre") #Simon 
class Typechambre(Base):
    __tablename__ = "type_chambre"
    nom_type: Mapped[str]
    prix_plafond: Mapped[float]
    prix_plancher: Mapped[float]
    description_chambre: Mapped[str]
    id_type_chambre: Mapped[str] = mapped_column(primary_key=True)
    # Relation de 1 à N qui sera automatiquement mappé sur SQLAlchemy grâce à la 'relationship()' de la classe Chambre
    chambre: Mapped[List["Chambre"]] = relationship(back_populates="type_chambre")
# --- Fin code du prof ---

class Reservation(Base):
    try :
        __tablename__ = "reservation"
        date_fin_reservation: Mapped[str] = mapped_column(nullable=False)
        date_debut_reservation: Mapped[str] = mapped_column(nullable=False)
        prix_jour: Mapped[float] = mapped_column(nullable=False)
        info_reservation: Mapped[str] = mapped_column(nullable=False)
        id_reservation: Mapped[str] = mapped_column(primary_key = True)
        # clées étrangères
        fk_id_client: Mapped[str] = mapped_column(ForeignKey("client.id_client"))
        fk_id_chambre: Mapped[str] = mapped_column(ForeignKey("chambre.id_chambre"))
        # Relations 1 à 1
        client: Mapped['Client'] = relationship()
        chambre: Mapped['Chambre'] = relationship()

        if (len(client) > len("EC50134D-372B-4DFD-9627-02BE06BA6BD6")) :
            raise NameError(f"Erreur dans la clé étrangère client")
        
        if (len(chambre) > len("EC50134D-372B-4DFD-9627-02BE06BA6BD6")) :
            raise NameError(f"Erreur dans la clé étrangère chambre")

        if isinstance(prix_jour, int) :
            raise ValueError(f"prix jour n'est pas le bon type (INT)")

        if (len(date_fin_reservation) > len("2026-09-15 00:00:00.000")) :
            ValueError(f"Erreur de date de fin de la reservation")

        if (len(date_debut_reservation) > len("2026-09-15 00:00:00.000")) :
            ValueError(f"Erreur de date de debut de la reservation")

        
    except ValueError as ve :
        print(f"Erreur de valeur: {ve}")
    except NameError as ne :
        print(f"Erreur de nom/string: {ne}")
    except sqlalchemy.exc.DatabaseError as dbe :
        print(f"Erreur d'opérations dans la DB: {dbe}")
    except sqlalchemy.exc.StatementError as se :
        print(f"Erreur de statement: {se}")
    except Exception as e :
        print(f"Autre exception: {e}")


# ---  Code Simon ---
class Client(Base):
    __tablename__ = "client"
    #Champs de la table client
    nom: Mapped[str]
    prenom: Mapped[str]
    adresse: Mapped[str]
    id_client: Mapped[str] = mapped_column(primary_key = True)
    mot_de_passe: Mapped[str]
    mobile: Mapped[str]
    # Relations 1 à N
    reservations: Mapped[List["Reservation"]] = relationship(back_populates="client")
    #--- Fin code Simon ---
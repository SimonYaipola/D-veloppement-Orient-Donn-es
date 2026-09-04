# --- Code du Prof ---

from pyclbr import Class
from typing import List
from sqlalchemy import ForeignKey
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
# --- Code de GUG ---
class Reservation(Base):
    __tablename__ = "reservation"
    date_fin_reservation: Mapped[str] 
    date_debut_reservation: Mapped[str] 
    prix_jour: Mapped[float]
    info_reservation: Mapped[str]
    id_reservation: Mapped[str] = mapped_column(primary_key = True)
    # clées étrangères
    fk_id_client: Mapped[str] = mapped_column(ForeignKey("client.id_client"))
    fk_id_chambre: Mapped[str] = mapped_column(ForeignKey("chambre.id_chambre"))
    # Relations 1 à 1
    client: Mapped['Client'] = relationship()
    chambre: Mapped['Chambre'] = relationship()
    # --- Fin code de GUG ---

# ---  Code Simon ---
class Client(Base):
    __tablename__ = "client"
    #Champs de la table client
    nom_: Mapped[str]
    prenom: Mapped[str]
    adresse: Mapped[str]
    id_client: Mapped[str] = mapped_column(primary_key = True)
    mot_de_passe: Mapped[str]
    mobile: Mapped[str]
    # Relations 1 à N
    reservations: Mapped[List["Reservation"]] = relationship(back_populates="client")
    #--- Fin code Simon ---
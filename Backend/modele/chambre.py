from typing import List, TYPE_CHECKING
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from modele.base import Base

if TYPE_CHECKING:
    from modele.typeChambre import TypeChambre
    from modele.reservation import Reservation


class Chambre(Base):
    __tablename__ = "chambre"

    numero_chambre: Mapped[int]
    disponible_reservation: Mapped[bool]
    autre_informations: Mapped[str]
    id_chambre: Mapped[str] = mapped_column(primary_key=True)

    # Définition de la clé étrangère qui permettra de mapper a classe type_chambre directement dans la classe chambre.
    fk_type_chambre: Mapped[str] = mapped_column(ForeignKey("type_chambre.id_type_chambre"))

    # Relation de 1 à 1 qui sera automatiquement mappé sur SQLAlchemy grâce à la clé étrangàre.
    type_chambre: Mapped['TypeChambre'] = relationship()
    # Relation de 1 à N qui sera automatiquement mappé sur SQLAlchemy grâce à la 'relationship()' de la classe Reservation
    reservations: Mapped[List["Reservation"]] = relationship(back_populates="chambre") 
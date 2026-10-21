from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, relationship, mapped_column
from modele.base import Base

if TYPE_CHECKING:
    from modele.reservation import Reservation

class Client(Base):
    __tablename__ = "client"
    #Champs de la table client
    nom: Mapped[str]
    prenom: Mapped[str]
    adresse: Mapped[str]
    id_client: Mapped[str] = mapped_column(primary_key = True)
    mot_de_passe: Mapped[str]
    mobile: Mapped[str]
    # Relations 1 Ã N
    reservations: Mapped[List["Reservation"]] = relationship(back_populates="client")
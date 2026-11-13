from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey, FetchedValue
from modele.base import Base


if TYPE_CHECKING:
    from modele.chambre import Chambre
    from modele.client import Client

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

    numero_reservation: Mapped[int] =  mapped_column(server_default=FetchedValue())
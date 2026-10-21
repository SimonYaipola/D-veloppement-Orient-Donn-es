from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, relationship, mapped_column
from modele.base import Base

if TYPE_CHECKING:
    from modele.chambre import Chambre




class TypeChambre(Base):
    __tablename__ = "type_chambre"

    nom_type: Mapped[str]
    prix_plafond: Mapped[float]
    prix_plancher: Mapped[float]
    description_chambre: Mapped[str]
    id_type_chambre: Mapped[str] = mapped_column(primary_key=True)

    chambre: Mapped[List["Chambre"]] = relationship(
        back_populates="type_chambre"
    )
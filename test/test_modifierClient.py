import unittest
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from modele.client import Client
from metier.clientMetier import modifierClient, ClientDTO
from engine.connexion import engine

with Session(engine) as session:

    class test_modification_Client(unittest.TestCase):
        def test_modifierClient(self):
            with Session(engine) as session:
                mobileClient = '4183681534'
                stmt = select(Client).where(
                    Client.mobile == mobileClient
                )

                clientAModifier = session.execute(stmt).scalars().first()
                self.assertIsNotNone(clientAModifier, "Le client avec le mobile " + mobileClient + " n'existe pas")
                idClient = clientAModifier.id_client
                adresseOriginale = clientAModifier.adresse
                motDePasseOriginal = clientAModifier.mot_de_passe

                clientDTOModifier = ClientDTO(
                    Client(
                        id_client=idClient,
                        nom=clientAModifier.nom,
                        prenom=clientAModifier.prenom,
                        adresse="Adresse modifiée",
                        mot_de_passe="MotDePasseModifie1!",
                        mobile=mobileClient
                        )
                    )

                try:
                    clientDTOModifier = modifierClient(clientDTOModifier)

                    self.assertEqual(clientDTOModifier.mobile_client, mobileClient)
                    self.assertEqual(clientDTOModifier.adresse_client, "Adresse modifiée")
                    self.assertEqual(clientDTOModifier.mot_de_passe_client, "MotDePasseModifie1!")

                finally:
                    session.execute(
                        update(Client).where(Client.id_client == idClient).values(
                            adresse=adresseOriginale,
                            mot_de_passe=motDePasseOriginal,
                        )
                    )
                    session.commit()
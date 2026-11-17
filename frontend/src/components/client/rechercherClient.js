import { useState } from "react";
import ListeClient from "./listeClientFonction";

const RechercheClient = () => {
    const [clients, setClients] = useState(undefined);

    const rechercheClients = () => {
        setClients(mockClients);
    };

    const effacerClients = () => {
        setClients([]);
    };

    return (
        <>
            <h1>Rechercher des clients</h1>
            <button onClick={rechercheClients}>Rechercher</button>
            <button onClick={effacerClients}>Effacer</button>
            {clients !== undefined && (
                <ListeClient clients={clients} />
            )}
        </>
    );
};

export default RechercheClient;

const mockClients = [
    {
        id_client: "7C1E9A54-2B3D-4F8E-A6C0-5D9B2E1F3A47",
        nom_client: "Saisrien",
        prenom_client: "Jean",
        adresse_client: "1234 rue Des Tulipes, Gaspé",
        mobile_client: "418-123-4567",
        mot_de_passe_client: "motdepasse123",
    },
    {
        id_client: "E4B2D817-6A9C-4E3F-8B1D-0F7C5A2E9D36",
        nom_client: "Therrien",
        prenom_client: "Paul",
        adresse_client: "6789 rue Des Érables, Matane",
        mobile_client: "418-456-1234",
        mot_de_passe_client: "motdepasse456",
    },
];

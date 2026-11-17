import { useState } from "react";
import ListeClient from "./listeClientFonction";

const SupprimerClient = () => {
    const [clients, setClients] = useState(mockClients);
    const [idClient, setIdClient] = useState("");
    const [message, setMessage] = useState("");

    const supprimerClient = () => {
        setClients(
            clients.filter((client) => client.id_client !== idClient)
        );
        setMessage(`Client ${idClient} supprimé.`);
        setIdClient("");
    };

    return (
        <>
            <h1>Supprimer un client</h1>
            <input type="text" placeholder="ID du client (UUID)" value={idClient} onChange={(e) => setIdClient(e.target.value)} />
            <button onClick={supprimerClient}>Supprimer</button>
            {message && <p>{message}</p>}

            <ListeClient clients={clients} />
        </>
    );
};

export default SupprimerClient;

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

import { useState } from "react";
import ListeClient from "./listeClientFonction";

const ModifierClient = () => {
    const [clients, setClients] = useState(mockClients);
    const [idClient, setIdClient] = useState("");
    const [formulaire, setFormulaire] = useState(undefined);
    const [message, setMessage] = useState("");

    const choisirClient = () => {
        const trouve = clients.find(
            (client) => client.id_client === idClient
        );
        setFormulaire({ ...trouve });
    };

    const changerChamp = (valeur) => {
        setFormulaire({ ...formulaire, [valeur.target.name]: valeur.target.value });
    };

    const modifierClient = () => {
        setClients(
            clients.map((client) =>
                client.id_client === formulaire.id_client ? formulaire : client
            )
        );
        setFormulaire(undefined);
        setIdClient("");
        setMessage("Client modifié.");
    };

    return (
        <>
            <h1>Modifier un client</h1>
            <input type="text" placeholder="ID du client (UUID)" value={idClient} onChange={(valeur) => setIdClient(valeur.target.value)} />
            <button onClick={choisirClient}>Choisir</button>
            {message && <p>{message}</p>}

            {formulaire !== undefined && (
                <div>
                    <br />
                    <label>
                        Prénom :{" "}
                        <input type="text" name="prenom_client" value={formulaire.prenom_client} onChange={changerChamp} />
                    </label>
                    <br />
                    <label>
                        Nom :{" "}
                        <input type="text" name="nom_client" value={formulaire.nom_client} onChange={changerChamp} />
                    </label>
                    <br />
                    <label>
                        Adresse :{" "}
                        <input type="text" name="adresse_client" value={formulaire.adresse_client} onChange={changerChamp} />
                    </label>
                    <br />
                    <label>
                        Mobile :{" "}
                        <input type="text" name="mobile_client" value={formulaire.mobile_client} onChange={changerChamp} />
                    </label>
                    <br />
                    <label>
                        Mot de passe :{" "}
                        <input type="text" name="mot_de_passe_client" value={formulaire.mot_de_passe_client} onChange={changerChamp} />
                    </label>
                    <br />
                    <button onClick={modifierClient}>
                        Modifier le client
                    </button>
                </div>
            )}

            <ListeClient clients={clients} />
        </>
    );
};

export default ModifierClient;

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

import { useState } from "react";
import ListeClient from "./listeClientFonction";

const formulaireVide = {
    id_client: "",
    nom_client: "",
    prenom_client: "",
    adresse_client: "",
    mobile_client: "",
    mot_de_passe_client: "",
};

const CreerClient = () => {
    const [clients, setClients] = useState(mockClients);
    const [formulaire, setFormulaire] = useState(formulaireVide);

    const changerChamp = (valeur) => {
        setFormulaire({ ...formulaire, [valeur.target.name]: valeur.target.value });
    };

    const creerClient = () => {
        const nouveauClient = { ...formulaire };
        setClients([...clients, nouveauClient]);
        setFormulaire(formulaireVide);
    };

    return (
        <>
            <h1>Créer un client</h1>

            <label>
                ID du client (UUID) :{" "}
                <input type="text" name="id_client" value={formulaire.id_client} onChange={changerChamp} placeholder="7C1E9A54-2B3D-4F8E-A6C0-5D9B2E1F3A47" />
            </label>
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
                <input type="text" name="mobile_client" value={formulaire.mobile_client} onChange={changerChamp} placeholder="418-123-4567" />
            </label>
            <br />
            <label>
                Mot de passe :{" "}
                <input type="text" name="mot_de_passe_client" value={formulaire.mot_de_passe_client} onChange={changerChamp} />
            </label>
            <br />
            <button onClick={creerClient}>Créer le client</button>

            <ListeClient clients={clients} />
        </>
    );
};

export default CreerClient;

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

export async function creerClient(client) {
    const nouveau = { ...client, id_client: Date.now() };
    mockClients = [...mockClients, nouveau];
    return nouveau;
}

export async function rechercherClient(idClient) {
    return mockClients;
}

export async function modifierClient(idClient, champs) {
    mockClients = mockClients.map((c) =>
        c.id_client === idClient ? { ...c, ...champs } : c
    );
    return mockClients.find((c) => c.id_client === idClient);
}

export async function supprimerClient(idClient) {
    mockClients = mockClients.filter((c) => c.id_client !== idClient);
    return { message: "Client supprimé." };
}

let mockClients = [
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

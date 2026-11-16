import logoChambre from "../logo/logoChambre.jpg";

export async function creerReservation(reservation) {
    const nouvelle = { ...reservation, id: Date.now() };
    mockReservations = [...mockReservations, nouvelle];
    return nouvelle;
}

export async function rechercherReservation(numeroReservation, numeroChambre) {
    return mockReservations;
}

export async function modifierReservation(id, champs) {
    mockReservations = mockReservations.map((r) =>
        r.id === id ? { ...r, ...champs } : r
    );
    return mockReservations.find((r) => r.id === id);
}

export async function supprimerReservation(id) {
    mockReservations = mockReservations.filter((r) => r.id !== id);
    return { message: "Réservation supprimée." };
}

/* json mock en attendant que l'on bind le front-end avec le back-end */
const mockReservations = [
    {
        id: 1,
        du: "15 décembre 2024",
        au: "24 décembre 2024",
        prix: "129.99",
        client: {
            prenom: "Jean",
            nom: "Saisrien",
            adresse: "1234 rue Des Tulipes, Gaspé",
            mobile: "418-123-4567",
        },
        chambre: {
            numero: 12,
            logo: logoChambre,
        },
    },
    {
        id: 2,
        du: "25 décembre 2024",
        au: "31 décembre 2024",
        prix: "159.99",
        client: {
            prenom: "Paul",
            nom: "Therrien",
            adresse: "6789 rue Des Érables, Matane",
            mobile: "418-456-1234",
        },
        chambre: {
            numero: 20,
            logo: logoChambre,
        },
    },
];
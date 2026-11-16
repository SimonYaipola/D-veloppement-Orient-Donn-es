import { useState } from "react";
import ListeReservation from "./listeReservationFonction";
import logoChambre from "../logo/logoChambre.jpg";

const RechercheReservation = () => {
    const [reservations, setReservations] = useState(undefined);

    const rechercheReservations = () => {
        setReservations(mockReservations);
    };

    const effacerReservations = () => {
        setReservations([]);
    };

    return (
        <>
            <h1>Rechercher des réservations</h1>
            <button onClick={rechercheReservations}>Rechercher</button>
            <button onClick={effacerReservations}>Effacer</button>
            {reservations !== undefined && (
                <ListeReservation reservations={reservations} />
            )}
        </>
    );
};

export default RechercheReservation;

const mockReservations = [
    {
        id_reservation: "3f2b8c1e-5a47-4d9e-9c1a-1b2f6e7d8a90",
        numero_reservation: 1,
        date_debut_reservation: "2026-12-15",
        date_fin_reservation: "2026-12-24",
        prix_jour: 129.99,
        info_reservation: "Arrivée en fin d'après-midi",
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
        id_reservation: "9a7d4e22-81bc-4f0a-b3d5-6c2e1f904a17",
        numero_reservation: 2,
        date_debut_reservation: "2026-12-25",
        date_fin_reservation: "2026-12-31",
        prix_jour: 159.99,
        info_reservation: "Lit supplémentaire demandé",
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
import { useState } from "react";
import ListeReservation from "./listeReservationFonction";
import logoChambre from "../logo/logoChambre.jpg";

const SupprimerReservation = () => {
    const [reservations, setReservations] = useState(mockReservations);
    const [numero, setNumero] = useState("");
    const [message, setMessage] = useState("");

    const supprimerReservation = () => {
        const existe = reservations.some(
            (reservation) => reservation.numero_reservation === Number(numero)
        );
        setReservations(
            reservations.filter((reservation) => reservation.numero_reservation !== Number(numero))
        );
        setMessage(`Réservation numéro ${numero} supprimée.`);
        setNumero("");
    };

    return (
        <>
            <h1>Supprimer une réservation</h1>
            <input type="number" placeholder="Numéro de la réservation" value={numero} onChange={(e) => setNumero(e.target.value)} />
            <button onClick={supprimerReservation}>Supprimer</button>
            {message && <p>{message}</p>}

            <ListeReservation reservations={reservations} />
        </>
    );
};

export default SupprimerReservation;

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
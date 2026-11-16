import { useState } from "react";
import ListeReservation from "./listeReservationFonction";
import logoChambre from "../logo/logoChambre.jpg";

const ModifierReservation = () => {
    const [reservations, setReservations] = useState(mockReservations);
    const [numero, setNumero] = useState("");
    const [formulaire, setFormulaire] = useState(undefined);
    const [message, setMessage] = useState("");


    const choisirReservation = () => {
        const trouvee = reservations.find(
            (reservation) => reservation.numero_reservation === Number(numero)
        );
        setFormulaire({ ...trouvee });
    };

    const changerChamp = (valeur) => {
        setFormulaire({ ...formulaire, [valeur.target.name]: valeur.target.value });
    };

    const modifierReservation = () => {
        const modifiee = {
            ...formulaire,
            numero_reservation: Number(formulaire.numero_reservation),
            prix_jour: Number(formulaire.prix_jour),
        };
        setReservations(
            reservations.map((reservation) =>
                reservation.id_reservation === modifiee.id_reservation ? modifiee : reservation
            )
        );
        setFormulaire(undefined);
        setNumero("");
        setMessage("Réservation modifiée.");
    };

    return (
        <>
            <h1>Modifier une réservation</h1>
            <input type="number" placeholder="Numéro de la réservation" value={numero} onChange={(valeur) => setNumero(valeur.target.value)} />
            <button onClick={choisirReservation}>Choisir</button>
            {message && <p>{message}</p>}

            {formulaire !== undefined && (
                <div>
                    <br />
                    <label>
                        Numéro de la réservation :{" "}
                        <input type="number" name="numero_reservation" value={formulaire.numero_reservation} onChange={changerChamp} />
                    </label>
                    <br />
                    <label>
                        Date de début :{" "}
                        <input type="date" name="date_debut_reservation" value={formulaire.date_debut_reservation} onChange={changerChamp} />
                    </label>
                    <br />
                    <label>
                        Date de fin :{" "}
                        <input type="date" name="date_fin_reservation" value={formulaire.date_fin_reservation} onChange={changerChamp} />
                    </label>
                    <br />
                    <label>
                        Prix par jour :{" "}
                        <input type="number" step="0.01" name="prix_jour" value={formulaire.prix_jour} onChange={changerChamp} />
                    </label>
                    <br />
                    <label>
                        Informations :{" "}
                        <input type="text" name="info_reservation" value={formulaire.info_reservation} onChange={changerChamp} />
                    </label>
                    <br />
                    <button onClick={modifierReservation}>
                        Modifier la réservation
                    </button>
                </div>
            )}

            <ListeReservation reservations={reservations} />
        </>
    );
};

export default ModifierReservation;

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
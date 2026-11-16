import { useState } from "react";

function Reservation({ reservation }) {
    const [isClientVisible, setIsClientVisible] = useState(false);
    const [isChambreVisible, setIsChambreVisible] = useState(false);

    return (
        <>
            <h4>
                Réservation numéro : {reservation.numero_reservation} :{" "} <br />
                {reservation.date_debut_reservation} au {reservation.date_fin_reservation}</h4>
            <p>{reservation.prix_jour} $ par jour</p>
            <p>{reservation.info_reservation}</p>
            <div>
                <button
                    className="button-info"
                    onClick={() => setIsClientVisible(!isClientVisible)}
                >
                    {reservation.client.prenom} {reservation.client.nom}
                </button>
                <p hidden={!isClientVisible}>
                    {reservation.client.adresse}
                    <br />
                    {reservation.client.mobile}
                </p>

                <br />

                <button
                    className="button-info"
                    onClick={() => setIsChambreVisible(!isChambreVisible)}
                >
                    Chambre {reservation.chambre.numero}
                </button>
                <p hidden={!isChambreVisible}>
                    <img
                        src={reservation.chambre.logo}
                        alt={`Chambre ${reservation.chambre.numero}`}
                    />
                </p>
            </div>
        </>
    );
}

export default Reservation;
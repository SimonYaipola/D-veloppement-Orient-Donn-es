import Reservation from "./reservationFonction";

const ListeReservation = ({ reservations = [] }) => {
    const listeReservation = reservations.map((reservation) => (
        <Reservation
            key={reservation.id_reservation}
            reservation={reservation}
        />
    ));

    return <>{listeReservation}</>;
};

export default ListeReservation;
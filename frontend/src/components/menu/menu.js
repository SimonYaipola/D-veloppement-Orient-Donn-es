import { Outlet, Link } from "react-router-dom";

const Menu = () => {
    return (
        <>
            <Link to="/client">Clients</Link>
            <br />
            <Link to="/admin">Administration</Link>
            <br />
            <Link to="/">Réservations</Link>
            <br />
            <Link to="/creer">Créer</Link>
            <br />
            <Link to="/modifier">Modifier</Link>
            <br />
            <Link to="/supprimer">Supprimer</Link>
            <Outlet />
        </>
    );
};

export default Menu;
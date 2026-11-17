import { Outlet, Link } from "react-router-dom";

const Menu = () => {
    return (
        <>
            <Link to="/admin">Administration</Link>
            <br />
            <Link to="/">Réservations</Link>
            <br />
            <Link to="/creer">Créer</Link>
            <br />
            <Link to="/modifier">Modifier</Link>
            <br />
            <Link to="/supprimer">Supprimer</Link>
            <br />
            <Link to="/client">Clients</Link>
            <br />
            <Link to="/client/creer">Créer un client</Link>
            <br />
            <Link to="/client/modifier">Modifier un client</Link>
            <br />
            <Link to="/client/supprimer">Supprimer un client</Link>
            <br />
            <Outlet />
        </>
    );
};

export default Menu;
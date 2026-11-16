import RechercheReservation from "./components/reservation/rechercherReservation";
import CreerReservation from "./components/reservation/creerReservation.js";
import SupprimerReservation from "./components/reservation/supprimerReservation.js";
import ModifierReservation from "./components/reservation/modifierReservation.js";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Menu from "./components/menu/menu.js";
import logoChambre from "./components/logo/logoChambre.jpg";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Menu />}>
                    <Route index element={<RechercheReservation />} />
                    <Route path="creer" element={<CreerReservation />} />
                    <Route path="supprimer" element={<SupprimerReservation />} />
                    <Route path="modifier" element={<ModifierReservation />} />
                </Route>
            </Routes>
        </BrowserRouter>
    );
}

export default App;
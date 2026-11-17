import RechercheReservation from "./components/reservation/rechercherReservation";
import CreerReservation from "./components/reservation/creerReservation.js";
import SupprimerReservation from "./components/reservation/supprimerReservation.js";
import ModifierReservation from "./components/reservation/modifierReservation.js";
// client
import RechercheClient from "./components/client/rechercherClient.js";
import CreerClient from "./components/client/creerClient.js";
import ModifierClient from "./components/client/modifierClient.js";
import SupprimerClient from "./components/client/supprimerClient.js";
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
                    <Route path="client" element={<RechercheClient />} />
                    <Route path="client/creer" element={<CreerClient />} />
                    <Route path="client/modifier" element={<ModifierClient />} />
                    <Route path="client/supprimer" element={<SupprimerClient />} />
                </Route>
            </Routes>
        </BrowserRouter>
    );
}

export default App;
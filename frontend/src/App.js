import Reservation from './components/reservation/reservationClasse'; 
import logoChambre from "./components/logo/logoChambre.jpg";

function App() {
  return (
    <>
      <Reservation reservation={reservation1} /> 
      <Reservation reservation={reservation2} />
    </>
  );
}

  
/* json mock en attendant que l'on bind le front-end avec le back-end */ 
const reservation1 = {
  du: "15 décembre 2024",
  au: "24 décembre 2024",
  prix: "129.99",
  client: {
    prenom: "Jean",
    nom: "Saisrien",
    adresse: "1234 rue Des Tulipes, Gaspé",
    mobile: "418-123-4567"
  },
  chambre: {
    numero: "12",
    logo: logoChambre
  }
}

const reservation2 = {
  du: "25 décembre 2024",
  au: "31 décembre 2024",
  prix: "159.99",
  client: {
  
    prenom: "Paul",
    nom: "Therrien",
    adresse: "6789 rue Des Érables, Matane",
    mobile: "418-456-1234"
  },
  chambre: {
    numero: 20,
    logo: logoChambre
  }
}

export default App;
import { useState } from "react";

function Client({ client }) {
    const [isInformationVisible, setIsInformationVisible] = useState(false);

    return (
        <>
            <h4>
                Client : {client.prenom_client} {client.nom_client}</h4>
            <p>ID : {client.id_client}</p>
            <div>
                <button
                    className="button-info"
                    onClick={() => setIsInformationVisible(!isInformationVisible)}
                >
                    Coordonnées
                </button>
                <p hidden={!isInformationVisible}>
                    {client.adresse_client}
                    <br />
                    {client.mobile_client}
                </p>
            </div>
        </>
    );
}

export default Client;

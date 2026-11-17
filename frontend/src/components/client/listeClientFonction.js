import Client from "./clientFonctions";

const ListeClient = ({ clients = [] }) => {
    const listeClient = clients.map((client) => (
        <Client
            key={client.id_client}
            client={client}
        />
    ));

    return <>{listeClient}</>;
};

export default ListeClient;

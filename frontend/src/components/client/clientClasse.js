import { Component, createRef } from "react";

class Client extends Component {
    constructor(props) {
        super(props);
        this.refInformation = createRef();
        this.toggleInformationVisibility = this.toggleInformationVisibility.bind(this);
    }

    render() {
        return <>
            <h4>Client : {this.props.client.prenom_client} {this.props.client.nom_client}</h4>
            <p>ID : {this.props.client.id_client}</p>
            <div>
                <button className="button-info"
                        onClick={() => this.toggleInformationVisibility(this.refInformation)}>
                    Coordonnées
                </button>
                <p ref={this.refInformation} hidden={true}>
                    {this.props.client.adresse_client}
                    <br></br>
                    {this.props.client.mobile_client}
                </p>
            </div>
        </>
    }

    toggleInformationVisibility(ref) {
        ref.current.hidden = !ref.current.hidden;
    }
}
export default Client;

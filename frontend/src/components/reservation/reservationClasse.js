import { Component, createRef } from "react";

class Reservation extends Component {
    constructor(props) {
        super(props);
        this.refClient = createRef();
        this.refChambre = createRef();
        this.toggleInformationVisibility = this.toggleInformationVisibility.bind(this);
    }

    render() {
        return <>
            <h4>{this.props.reservation.du} au {this.props.reservation.au}</h4>
            <p>{this.props.reservation.prix} par jour</p>
            <div>
                <button class="button-info"
                        onclick={() => this.toggleInformationVisibility(this.refClient)}> 
                    {this.props.reservation.client.prenom} {this.props.reservation.client.nom}
                </button>
                <p ref={this.refClient} hidden={true}>
                    {this.props.reservation.client.adresse}
                    <br></br>
                    {this.props.reservation.client.mobile}
                </p>
                <br></br>
                <button class="button-info"
                        onclick={() => this.toggleInformationVisibility(this.refChambre)}>
                    Chambre {this.props.reservation.chambre.numero}
                </button>
                <p ref={this.refChambre} hidden={true}>
                    <img src={this.props.reservation.chambre.logo} />
                </p>
            </div>
        </>
    }

    toggleInformationVisibility(ref) {
        ref.current.hidden ? ref.current.hidden = false : ref.current.hidden= true;
    }
}
export default Reservation;
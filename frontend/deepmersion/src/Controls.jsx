import React, { Component } from "react";

import { ButtonGroup, Button } from "react-bootstrap";

import FontAwesomeIcon from "@fortawesome/react-fontawesome";
import faBomb from "@fortawesome/fontawesome-free-solid/faBomb";

export class Controls extends Component {
  render() {
    return (
      <div className="container controls">
        <ButtonGroup>
          <Button bsStyle="warning" onClick={this.props.onRandomise}>
            <FontAwesomeIcon icon={faBomb} /> Randomize
          </Button>
          <Button
            bsStyle="info"
            active={this.props.muted}
            onClick={this.props.onToggle.bind(null, "muted")}
          >
            Mute
          </Button>
        </ButtonGroup>
        &emsp;
        <ButtonGroup>
          <Button
            bsStyle="primary"
            active={!this.props.useObjects}
            onClick={this.props.onToggle.bind(null, "useObjects")}
          >
            Objects
          </Button>
          <Button
            bsStyle="success"
            active={!this.props.usePlaces}
            onClick={this.props.onToggle.bind(null, "usePlaces")}
          >
            Places
          </Button>
        </ButtonGroup>
        &emsp;
        <Button
          bsStyle="danger"
          active={!this.props.useChatter}
          onClick={this.props.onToggle.bind(null, "useChatter")}
        >
          Chatter
        </Button>
        &emsp;
        {this.props.loading && <Spinner name="circle" />}
      </div>
    );
  }
}

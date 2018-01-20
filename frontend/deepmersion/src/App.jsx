import React, { Component } from "react";

import {
  PageHeader,
  Grid,
  Row,
  Col,
  ButtonGroup,
  Button
} from "react-bootstrap";

import Dropzone from "react-dropzone";

import FontAwesomeIcon from "@fortawesome/react-fontawesome";
import faFileImage from "@fortawesome/fontawesome-free-regular/faFileImage";
import faBomb from "@fortawesome/fontawesome-free-solid/faBomb";

import { AudioGrid } from "./AudioChoices";
import "./App.css";
import logo from "./logo.svg";

class App extends Component {
  constructor(props) {
    super(props);

    this.sounds = [
      "main-birds",
      "main-crickets",
      "main-fire",
      "main-people",
      "main-rain",
      "main-sbowl",
      "main-thunder",
      "main-waves",
      "main-whitenoise",
      "main-wind"
    ];

    this.state = {
      isEnabled: true,
      muted: true,

      masterVolume: 0.5,
      volumes: this.sounds.map(_ => 0)
    };
  }

  randomizeSounds = () => {
    let newVolumes = this.sounds.map(_ => {
      let r = Math.random();
      if (r < 0.5) {
        return 0;
      }

      return r;
    });

    this.setState({ volumes: newVolumes });
  };

  toggleMute = () => {
    this.setState(previous => {
      return { muted: !previous.muted };
    });
  };

  onDrop = (accepted, rejected) => {
    let reader = new FileReader();

    reader.onload = img => {
      console.log("image loaded");
      this.refs.preview.src = img.target.result;
    };
    reader.readAsDataURL(accepted[0]);
  };

  render() {
    return (
      <div className="App">
        <div className="container">
          <PageHeader>
            <img src={logo} className="logo" alt="logo" /> DeepMersion{" "}
            <small>own your surroundings</small>
          </PageHeader>

          <p className="lead">
            {/* someone please write something better than this. */}
            DeepMersion takes photos you provide, and picks ambient background
            music to suit it. Try with an example photo below, or upload your
            own.
          </p>
        </div>

        <div className="container controls">
          <ButtonGroup>
            <Button bsStyle="warning" onClick={this.randomizeSounds}>
              <FontAwesomeIcon icon={faBomb} /> Randomize
            </Button>
            <Button
              bsStyle="info"
              active={this.state.muted}
              onClick={this.toggleMute}
            >
              Mute
            </Button>
          </ButtonGroup>
        </div>

        <div className="container">
          <Grid>
            <Row>
              <Col md={4}>
                <Dropzone
                  accept="image/jpeg, image/png"
                  multiple={false}
                  onDrop={this.onDrop}
                >
                  <div className="dropzone">
                    <FontAwesomeIcon icon={faFileImage} size="6x" />

                    <p>Drop an image here.</p>
                    <small>Accepts JPEG, PNG</small>
                  </div>
                </Dropzone>
              </Col>
              <Col md={8}>
                <img ref="preview" className="previewImage" alt="" />
              </Col>
            </Row>
          </Grid>
        </div>

        <AudioGrid
          ref="grid"
          muted={this.state.muted}
          masterVolume={this.state.masterVolume}
          volumes={this.state.volumes}
          sounds={this.sounds}
        />
      </div>
    );
  }
}

export default App;

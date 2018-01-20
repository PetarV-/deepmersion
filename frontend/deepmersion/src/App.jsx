import React, { Component } from "react";

import {
  PageHeader,
  Grid,
  Row,
  Col,
  ButtonGroup,
  Button,
  Label
} from "react-bootstrap";

import Dropzone from "react-dropzone";
import request from "superagent";

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
      volumes: this.sounds.map(_ => 0),
      tags: []
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

    this.setState({ volumes: newVolumes, muted: false });
  };

  toggleMute = () => {
    this.setState(previous => {
      return { muted: !previous.muted };
    });
  };

  classify = image => {
    const req = request.post("/classify");
    req.attach("image", image);
    req.then(res => {
      let tags = res.body.tags;
      let volumes = res.body.volumes;
      this.setState({
        volumes: volumes,
        tags: tags,
        muted: false
      });
    });
  };

  onDrop = (accepted, rejected) => {
    this.classify(accepted[0]);

    // update the preview
    let reader = new FileReader();

    reader.onload = img => {
      console.log("image loaded");
      this.refs.preview.src = img.target.result;
    };
    reader.readAsDataURL(accepted[0]);
  };

  render() {
    let tags = this.state.tags.map(x => {
      return (
        <span>
          <Label bsStyle="primary">{x}</Label>
          &emsp;
        </span>
      );
    });

    return (
      <div className="App">
        <div className="shiny">
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
        </div>

        <div className="container dragdrop">
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
              <Col md={4}>
                <img ref="preview" className="previewImage" alt="" />
              </Col>
              <Col md={4}>
                <p style={{ lineHeight: 1.75 }}>{tags}</p>
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

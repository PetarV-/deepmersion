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
      objectTags: [],
      placeTags: [],

      useObjects: true,
      usePlaces: true,
      useChatter: true
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

  toggleChatter = () => {
    this.setState(previous => {
      return { useChatter: !previous.useChatter };
    });
  };

  classify = image => {
    request
      .post("/classify")
      .field("useObjects", this.state.useObjects)
      .field("useChatter", this.state.useChatter)
      .field("usePlaces", this.state.usePlaces)
      .attach("image", image)
      .then(res => {
        let objectTags = res.body.objectTags;
        let placeTags = res.body.placeTags;

        let volumes = res.body.volumes;
        console.log(volumes);

        this.setState({
          volumes: volumes,
          muted: false,

          objectTags: objectTags || [],
          placeTags: placeTags || []
        });
      });
  };

  onDrop = (accepted, rejected) => {
    // ask the server for an audio configuration
    this.classify(accepted[0]);

    // update the preview
    let reader = new FileReader();

    reader.onload = img => {
      console.log("image loaded");
      this.refs.preview.src = img.target.result;
    };
    reader.readAsDataURL(accepted[0]);
  };

  toggleObjects = () => {
    this.setState(previous => {
      return {
        useObjects: !previous.useObjects
      };
    });
  };

  togglePlaces = () => {
    this.setState(previous => {
      return {
        usePlaces: !previous.usePlaces
      };
    });
  };

  render() {
    let objectTags = this.state.objectTags.map(x => {
      return (
        <span>
          <Label bsStyle="primary">{x}</Label>
          &emsp;
        </span>
      );
    });

    let placeTags = this.state.placeTags.map(x => {
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
              <img src={logo} className="logo" alt="logo" /> Deepmersion{" "}
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
            &emsp;
            <ButtonGroup>
              <Button
                bsStyle="primary"
                active={this.state.useObjects}
                onClick={this.toggleObjects}
              >
                Objects
              </Button>
              <Button
                bsStyle="success"
                active={this.state.usePlaces}
                onClick={this.togglePlaces}
              >
                Places
              </Button>
            </ButtonGroup>
            &emsp;
            <Button
              bsStyle="danger"
              active={this.state.useChatter}
              onClick={this.toggleChatter}
            >
              Chatter
            </Button>
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
                <p style={{ lineHeight: 1.75 }}>{objectTags}</p>
                <p style={{ lineHeight: 1.75 }}>{placeTags}</p>
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

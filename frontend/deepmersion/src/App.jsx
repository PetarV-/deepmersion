import React, { Component } from "react";

import { PageHeader, Grid, Row, Col, Label } from "react-bootstrap";

import Dropzone from "react-dropzone";
import request from "superagent";

import FontAwesomeIcon from "@fortawesome/react-fontawesome";
import faFileImage from "@fortawesome/fontawesome-free-regular/faFileImage";

import { AudioGrid } from "./AudioChoices";
import { TagList } from "./TagList";
import { Controls } from "./Controls";
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
      useChatter: true,
      usePlaces: true
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

  toggle = key => {
    this.setState(previous => {
      let result = {};
      result[key] = !previous[key];
      return result;
    });
  };

  render() {
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

          <Controls
            onRandomise={this.randomizeSounds}
            onToggle={this.toggle}
            useObjects={this.state.useObjects}
            useChatter={this.state.useChatter}
            usePlaces={this.state.usePlaces}
            muted={this.state.muted}
          />
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
                <TagList tags={this.state.objectTags} bsStyle="primary" />
                <TagList tags={this.state.placeTags} bsStyle="success" />
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

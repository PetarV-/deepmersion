import React, { Component } from "react";

import { PageHeader } from "react-bootstrap";

import { AudioGrid } from "./AudioChoices";
import { Controls } from "./Controls";
import { DropZone } from "./DropZone";

import "./App.css";
import logo from "./logo.svg";

export default class App extends Component {
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

      useObjects: true,
      useChatter: true,
      usePlaces: true
    };
  }

  randomizeSounds = () => {
    this.setState({ volumes: this.sounds.map(Math.random), muted: false });
  };

  toggle = key => {
    this.setState(previous => {
      let result = {};
      result[key] = !previous[key];
      return result;
    });
  };

  updateVolumes = volumes => {
    this.setState({
      volumes: volumes,
      muted: false
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

        <DropZone
          useObjects={this.state.useObjects}
          useChatter={this.state.useChatter}
          usePlaces={this.state.usePlaces}
          onClassify={this.updateVolumes}
        />

        <AudioGrid
          muted={this.state.muted}
          masterVolume={this.state.masterVolume}
          volumes={this.state.volumes}
          sounds={this.sounds}
        />
      </div>
    );
  }
}

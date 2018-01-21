import React, { Component } from "react";

import { PageHeader } from "react-bootstrap";
import Spinner from "react-spinkit";

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
      useChatter: false,
      usePlaces: true,

      chatterLevel: 1.0
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
    this.refs.controls.props.loading = false;
    console.log("Updating");
    console.log(volumes);
    this.setState({
      volumes: volumes,
      muted: false
    });
  };

  showLoading = () => {
    this.refs.controls.props.loading = true;
  };

  render() {
    return (
      <div className="App">
        <div className="shiny">
          <div className="container">
            <PageHeader>
              <img src={logo} className="logo" alt="logo" /> deepmersion{" "}
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
            ref="controls"
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
          chatterLevel={this.state.chatterLevel}
          onClassify={this.updateVolumes}
          onBeforeClassify={this.showLoading}
        />

        <AudioGrid
          muted={this.state.muted}
          masterVolume={this.state.masterVolume}
          volumes={this.state.volumes}
          sounds={this.sounds}
        />

        <footer>
          <div className="container">
            <hr />

            {/* <small>
              Developed by{" "}
              <a href="https://github.com/andreeadeac22">Andreea Deac</a>,{" "}
              <a href="https://github.com/catalina17">Catalina Cangeea</a>,{" "}
              <a href="https://github.com/matthewelse">Matthew Else</a> and{" "}
              <a href="https://github.com/petarv-">Petar Velickovic</a> at{" "}
              <a href="http://hackcambridge.com/">Hack Cambridge</a>, 2018.
            </small> */}
          </div>
        </footer>
      </div>
    );
  }
}

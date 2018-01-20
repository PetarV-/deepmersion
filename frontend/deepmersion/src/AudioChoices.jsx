// import ReactDOM from 'react-dom';
import React, { Component } from "react";

class AudioPlayer extends Component {
  componentWillUpdate(props, state) {
    this.refs.audio.volume = this.props.volume;
  }

  render() {
    let src_mp4 = this.props.src + ".mp4";
    let src_ogg = this.props.src + ".ogg";

    return (
      <audio
        ref="audio"
        loop
        autoPlay={true}
        volume={this.props.volume}
        muted={this.props.muted}
      >
        <source src={src_mp4} type="audio/mpeg" />
        <source src={src_ogg} type="audio/ogg" />
      </audio>
    );
  }
}

export class AudioGrid extends Component {
  constructor(props) {
    super(props);

    // we need to keep track of one volume for each audio file
    this.audioRoot = "/sounds";
    this.sounds = props.sounds;
  }

  render() {
    this.audios = this.sounds.map((name, i) => {
      return (
        <AudioPlayer
          key={name}
          src={this.audioRoot + "/" + name}
          volume={this.props.volumes[i] * this.props.masterVolume}
          muted={this.props.volumes[i] === 0 || this.props.muted}
        />
      );
    });

    return <div ref="container">{this.audios}</div>;
  }
}

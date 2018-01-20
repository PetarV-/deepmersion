// import ReactDOM from 'react-dom';
import React, { Component } from 'react';

class AudioPlayer extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (<video src={this.props.src} loop autoPlay={true} volume={this.props.volume} muted={this.props.muted}></video>)
  }
}

export class AudioGrid extends Component {
  constructor(props) {
    super(props);

    // we need to keep track of one volume for each audio file
    this.audioRoot = '/sounds';
    this.sounds = [
      'main-birds.mp4',
      'main-fire.mp4',
      'main-rain.mp4',
      'main-thunder.mp4',
      'main-whitenoise.mp4',
      'main-crickets.mp4',
      'main-people.mp4',
      'main-sbowl.mp4',
      'main-waves.mp4',
      'main-wind.mp4',
    ];

    this.state = {
      volume: this.sounds.map((_) => {
        let r = Math.random();
        if (r < 0.5) {
          return 0;
        }

        return r;
      }),
      volumeScale: this.props.volume
    }
  }

  render() {
    this.audios = this.sounds.map((name, i) => {
      return (<AudioPlayer key={name} src={this.audioRoot + "/" + name} volume={this.state.volume[i] * this.state.volumeScale} muted={this.state.volume[i] === 0 || this.props.muted}/>)
    })

    return (<div ref='container'>
      {this.audios}
    </div>)
  }
}


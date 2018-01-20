import React, { Component } from 'react';
import { Navbar } from 'react-bootstrap';
import { MuteToggleButton, VolumeSlider } from 'react-player-controls';
import { AudioGrid } from './AudioChoices';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props)
    this.state = {
      isEnabled: true,
      muted: false,

  	  volume: 0
    }
  }

  toggleMute = () => {
    this.setState((previous) => {
      return {muted: !previous.muted}
    })
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
            <Navbar inverse staticTop>
                <Navbar.Header>
                    <Navbar.Brand>
                        <a href="#home">deepmersion</a>
                    </Navbar.Brand>
                </Navbar.Header>
            </Navbar>
        </header>

        <div className="App-controls">
            <MuteToggleButton
              isEnabled={this.state.isEnabled}
              isMuted={this.state.muted}
              onMuteChange={this.toggleMute}
            />
        </div>

    		<VolumeSlider
    		  isEnabled={this.state.isEnabled}
    		  volume={this.state.volume}
    		  onVolumeChange={volume => this.setState({ volume: volume })} 
    		/>

        <AudioGrid ref="grid" muted={this.state.muted} volume={this.state.volume}/>
      </div>
    );
  }
}

export default App;

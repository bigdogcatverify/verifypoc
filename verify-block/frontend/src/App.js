import React, { Component } from 'react';
import './App.css';
import Status from './components/status'
import Send from './components/send'
import Chain from './components/chain'
import axios from 'axios';

class App extends Component {
  constructor(props){
    super(props);
  }
  render(){
  return (
    <div className="App">
    <Status/>
    <Send/>
    <Chain/>
    </div>
    );
  }
}

export default App;
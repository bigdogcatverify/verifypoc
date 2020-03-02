import React, { Component } from 'react';
import './App.css';
import Status from './components/status'
import Send from './components/send'
import Transactions from './components/transactions'
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
    <Transactions/>
    </div>
    );
  }
}

export default App;
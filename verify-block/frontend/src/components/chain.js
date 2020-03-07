import React, { Component } from 'react';
import { Container, Table } from 'react-bootstrap';
import axios from 'axios';

const endpoint = '/get_chain'
class Chain extends Component {
  constructor(props){
    super(props);
    this.state = {
      chain: [],
    }
  }
  componentDidMount() {
    axios.get(endpoint)
      .then(res => {
        const chain = res.data.chain;
        this.setState({ chain });
      })
  }
  render(){
    return (
      <Container>
      <h3><b> Chain </b></h3>
      <p>(Sync to get the latest chain time in the blockchain)</p>
      <Table responsive>
  <thead>
  <tr>
      <th>Index</th>
      <th>Time</th>
    </tr>
  </thead>
  <tbody>
  { this.state.chain.slice(0).reverse().map( c =>
    <tr key={c}>
      <td><b style={{color: '#007bff'}}>{c.index}</b></td>
      <td><b style={{color: '#007bff'}}>{c.timestamp}</b></td>
    </tr>
  )}
    </tbody>
    </Table>
      </Container>
    );
  }
}

export default Chain;
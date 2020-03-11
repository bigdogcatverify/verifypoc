import React, { Component } from 'react';
import { Form, Container, Col, Row, Button } from 'react-bootstrap';
import axios from 'axios';

const postEndpoint = '/mine_block';
const getEndpoint = '/get_chain';

class Send extends Component {
  constructor(props){
    super(props);
    this.state = {
      requester: '',
      time: '',
      verifier: '',
      isverified: '',
      address: '',
    };
    this.handleRequester = this.handleRequester.bind(this);
    this.handleVerifier = this.handleVerifier.bind(this);
    this.handleAddress = this.handleAddress.bind(this);
    this.handleIsVerified = this.handleIsVerified.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleRequester(event){
    this.setState({ requester: event.target.value});
  }
  handleVerifier(event){
    this.setState({ verifier: event.target.value});
  }
  handleAddress(event){
    this.setState({ address: event.target.value});
  }
  handleIsVerified(event){
    this.setState({ isverified: event.target.value});
  }
  componentDidMount() {
    axios.get(getEndpoint)
      .then(res => {
      })
    }

  handleSubmit(event) {
    event.preventDefault();

      axios.post(postEndpoint, { "verifier": this.state.verifier,
      "requester": this.state.requester,
      "time": this.state.time,
      "address": this.state.address,
      "isverified": this.state.isverified })
       .then(res => {
         console.log(res);
         console.log(res.data);
       })
  }

  render(){
    return (
        <Container>
  <br/>
  <h3><b>Verify</b></h3>
  <h4><b style={{color: '#007bff'}}>Verify Transactions</b> </h4>
        <Form onSubmit={this.handleSubmit}>
        <Form.Group as={Row}>
         <Form.Label column sm="2">
           Requester
         </Form.Label>
         <Col sm="8">
           <Form.Control onChange={this.handleRequester} value={this.state.requester} placeholder="Enter Requester" />
         </Col>
       </Form.Group>
       <Form.Group as={Row}>
         <Form.Label column sm="2">
           Verifier
         </Form.Label>
         <Col sm="8">
           <Form.Control onChange={this.handleVerifier} value={this.state.verifier} placeholder="Enter Verifier" />
         </Col>
       </Form.Group>
       <Form.Group as={Row}>
         <Form.Label column sm="2">
           Address
         </Form.Label>
         <Col sm="8">
           <Form.Control onChange={this.handleAddress} value={this.state.address} placeholder="Enter Address" />
         </Col>
       </Form.Group>
       <Form.Group as={Row}>
         <Form.Label column sm="2">
           Verified?
         </Form.Label>
         <Col sm="8">
           <Form.Control type="checkbox" onChange={this.handleIsVerified} value={this.state.isverified} placeholder="Is this verified" />
         </Col>
       </Form.Group>
      <Form.Group as={Row}>
      <Col sm="5">
      <Button variant="primary" type="submit">
    Send
  </Button>
  </Col>
  </Form.Group>
     </Form>
     <br/><br/>
      </Container>
    );
  }
}

export default Send;
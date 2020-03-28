import React, { Component } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'font-awesome/css/font-awesome.min.css';
import { Container, Row, Col } from 'react-bootstrap';
import axios from 'axios';


const endpoint = '/block/api/get_chain';
class Status extends Component {
  constructor(props){
    super(props);
    this.state = {
      length: [],
    }
  }

  componentDidMount() {
    axios.get(endpoint)
      .then(res => {
        const length = res.data.length;
        this.setState({ length });
      })
  }
  render(){
    return (
    <Container>
    <br/>
    <Row>
    <Col sm="6">
  <h5> <div><i className="fa fa-cubes"/></div> No. of Blocks Mined </h5> <hr/>
 <h5 style={{color: '#007bff'}}>#<b>{this.state.length} </b></h5>
    </Col>
    </Row>
    <br/><br/><br/>
    </Container>
    );
  }
}

export default Status;
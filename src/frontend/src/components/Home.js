import React, { Component } from "react";
import TableContainer from "./TableContainer";
import { getColumnResult } from "./Column";
import { Container } from "reactstrap";
import './Home.css';

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      loaded: false,
      placeholder: "Loading",
    };
  }

  componentDidMount() {
    fetch("api/result")
      .then((response) => {
        if (response.status > 400) {
          return this.setState(() => {
            return { placeholder: "Something went wrong!" };
          });
        }
        return response.json();
      })
      .then((data) => {
        this.setState(() => {
          return {
            data,
            loaded: true,
          };
        });
      });
  }

  render() {
    const columns = getColumnResult();
    const { data, loaded, error } = this.state;
    return (
      <Container style={{ marginTop: 20 }}>
        <TableContainer columns={columns} data={data} />
      </Container>
    );
  }
}

export default Home;

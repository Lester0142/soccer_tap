import React, { Component, useMemo, useState, useEffect } from "react";

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
    const { data, loaded, error } = this.state;
    return (
      <div>
        Hello from Results
        <ul>
          {this.state.data.map((each) => {
            return (
              <li key={each.id}>
                {each.name} - {each.goal} - {each.win}
              </li>
            );
          })}
        </ul>
      </div>
    );
  }
}

export default Home;

import React, { Component } from "react";
import Form from "./Form";
import getCookie from "./csrftoken";

class Match extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      loaded: false,
      placeholder: "Loading",
    };
  }

  componentDidMount() {
    fetch("api/match")
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

  handleFormSubmit = (textValue) => {
    fetch("insert/match", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({ content: textValue }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((value) => {
        if (value.status == 200){
          alert("Data submitted successfully!");
        } else {
          alert("Not updated properly. Please try again...")
        }
      })
      .catch((error) => {
        alert(`An error occurred: ${error.message}`);
      });
  };

  render() {
    const { data, loaded, error } = this.state;
    return (
      <div>
        Hello from matches
        <ul>
          {this.state.data.map((each) => {
            return (
              <li key={each.id}>
                {each.team_one} - {each.team_two} - {each.goal_one} - {each.goal_two}
              </li>
            );
          })}
        </ul>
        <label htmlFor="textInput"><b>Insert Matches:</b></label>
        <Form onSubmit={this.handleFormSubmit} />
      </div>
    );
  }
}

export default Match;

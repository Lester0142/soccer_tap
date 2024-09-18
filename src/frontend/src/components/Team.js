import React, { Component } from "react";
import Form from "./Form";
import getCookie from "./csrftoken";
import TableContainer from "./TableContainer";
import { getColumnTeam } from "./Column";
import './Team_Match.css';

class Team extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      loaded: false,
      placeholder: "Loading",
      columns: [],
      error: null
    };
  }

  // Data fetching method
  fetchData = () => {
    fetch("api/team")
      .then((response) => {
        if (response.status > 400) {
          throw new Error("Something went wrong!");
        }
        return response.json();
      })
      .then((data) => {
        this.setState({
          data,
          loaded: true,
          placeholder: null,
          error: null
        });
      })
      .catch((error) => {
        this.setState({
          placeholder: "Something went wrong!",
          error: error.message
        });
      });
  };

  componentDidMount() {
    this.setState({ columns: getColumnTeam() });
    this.fetchData(); // Initial data fetch
  }

  handleFormSubmit = (textValue) => {
    fetch("insert/team", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
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
        if (value.status === 200) {
          alert("Data submitted successfully!");
          this.fetchData(); // Refresh data after successful submission
        } else {
          alert("Not updated properly. Please try again...");
        }
      })
      .catch((error) => {
        alert(`An error occurred: ${error.message}`);
      });
  };

  saveChanges = (ogValue, editValue) => {
    let post_mess = ogValue["name"].concat(" ", editValue["name"], " ", editValue["date"], " ", editValue["group"])
    console.log(post_mess);
    fetch("update/team", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({content: post_mess}),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((value) => {
        if (value.status === 200) {
          alert("Data submitted successfully!");
          this.fetchData(); // Refresh data after successful submission
        } else {
          alert("Not updated properly. Please try again...");
        }
      })
      .catch((error) => {
        alert(`An error occurred: ${error.message}`);
      });
  };

  deleteEntry = (editValue) => {
    let post_mess = editValue["name"].concat(" ", editValue["name"], " ", editValue["date"], " ", editValue["group"])
    console.log(post_mess);
    fetch("delete/team", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({content: post_mess}),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((value) => {
        if (value.status === 200) {
          alert("Data submitted successfully!");
          this.fetchData(); // Refresh data after successful submission
        } else {
          alert("Not updated properly. Please try again...");
        }
      })
      .catch((error) => {
        alert(`An error occurred: ${error.message}`);
      });
  };

  render() {
    const { data, loaded, placeholder, error, columns } = this.state;

    return (
      <div className="container_custom">
        <div className="table-container_custom">
          {/* Check for loading state and errors */}
          {!loaded && !error && <div>{placeholder}</div>}
          {error && <div style={{ color: 'red' }}>{error}</div>}
          {loaded && <TableContainer columns={columns} data={data} saveChanges={this.saveChanges} deleteEntry={this.deleteEntry}/>}
        </div>
        <div className="form-container_custom">
          <label htmlFor="textInput_custom">
            <b>Insert Teams:</b>
          </label>
          <Form onSubmit={this.handleFormSubmit} />
        </div>
      </div>
    );
  }
}

export default Team;

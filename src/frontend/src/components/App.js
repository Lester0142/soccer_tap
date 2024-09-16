import React, { Component } from "react";
import { render } from "react-dom";
import AppNavbar from "./Navbar";
import Home from "./Home";
import Team from "./Team";
import Match from "./Match";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedComponent: 'home'
    };
  }

  handleSelect = (component) => {
    this.setState({ selectedComponent: component });
  };

  renderComponent() {
    const { selectedComponent } = this.state;
    switch (selectedComponent) {
      case 'home':
        return <Home />;
      case 'team':
        return <Team />;
      case 'match':
        return <Match />;
      default:
        return <Home />;
    }
  }

  render() {
    return (
      <>
        <AppNavbar onSelect={this.handleSelect} />
        <div className="container mt-4">
          {this.renderComponent()}
        </div>
      </>
    );
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);

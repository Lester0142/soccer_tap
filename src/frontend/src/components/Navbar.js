import React from 'react';
import { Navbar, Nav, Container } from 'react-bootstrap';

const AppNavbar = ({ onSelect }) => {
  return (
    <Navbar bg="primary" data-bs-theme="dark">
      <Container>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="mr-auto">
            <Nav.Link href="" onClick={() => onSelect('home')}>Results</Nav.Link>
            <Nav.Link href="" onClick={() => onSelect('team')}>Teams</Nav.Link>
            <Nav.Link href="" onClick={() => onSelect('match')}>Matches</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default AppNavbar;

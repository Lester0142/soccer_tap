import React, { useState } from 'react';
import { Navbar, Nav, Container, Button, Modal } from 'react-bootstrap';
import { FaTrash, FaFile } from 'react-icons/fa'; // Import trash icon
import getCookie from "./csrftoken";

const AppNavbar = ({ onSelect }) => {
  const [showDeleteModal, setShowDeleteModal] = useState(false); // State to handle modal visibility
  const [itemToDelete, setItemToDelete] = useState(null); // State to store the item to delete
  const [selectedTab, setSelectedTab] = useState('home'); // State to track selected tab

  // Function to handle the delete icon click
  const handleDeleteClick = (item) => {
    setItemToDelete(item); // Set the item to delete
    setShowDeleteModal(true); // Show the confirmation modal
  };

  // Function to confirm deletion and make the API call
  const confirmDelete = () => {
    if (itemToDelete) {
      setItemToDelete(null)
      fetch('delete/all', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          "X-CSRFToken": CSRF_TOKEN,
        },
        body: JSON.stringify({ content: "delete" }), // Send the item to be deleted
        credentials: "same-origin"
      })
        .then((response) => response.json())
        .then((value) => {
          if (value.status === 200) {
            alert("Delete Completed!");
            window.location.reload();
          } else {
            alert("Delete Issues. Please try again...");
          }
          setShowDeleteModal(false); // Close the modal after successful deletion
        })
        .catch((error) => {
          console.error('Error deleting:', error);
          alert("Delete Issues. Please try again...");
        });
    }
  };

  // Function to handle the download log icon click
  const handleLogClick = () => {
    getLog();
  };

  // Function to get and download the log file
  const getLog = () => {
    fetch('/download/log', { // Ensure this URL matches your Django endpoint
      method: 'GET',
      headers: {
        // 'Content-Type': 'application/json', // Remove or modify if not necessary for file download
        "X-CSRFToken": CSRF_TOKEN, // Optional, for CSRF protection if enabled
      },
      credentials: "same-origin"
    })
      .then(response => {
        if (response.ok) {
          // Extract the filename from the Content-Disposition header
          const contentDisposition = response.headers.get('Content-Disposition');
          let filename = 'logfile.txt'; // Default filename if header is not present

          if (contentDisposition) {
            const matches = /filename="([^"]*)"/.exec(contentDisposition);
            if (matches != null && matches[1]) {
              filename = matches[1];
            }
          }

          return response.blob().then(blob => ({ blob, filename }));
        } else {
          throw new Error('File not found or an error occurred.');
        }
      })
      .then(({ blob, filename }) => {
        // Create a link element to download the file
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename; // Use the filename extracted from the response
        document.body.appendChild(a);
        a.click(); // Trigger the download
        window.URL.revokeObjectURL(url); // Clean up the URL object
        a.remove(); // Remove the link element
      })
      .catch(error => {
        console.error(error.message);
        alert("Error downloading the file. Please try again.");
      });
  };

  return (
    <>
      <Navbar bg="primary" variant="dark">
        <Container>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="navbar-left">
              <Nav.Link
                href=""
                onClick={() => { onSelect('home'); setSelectedTab('home'); }}
                style={{ textDecoration: selectedTab === 'home' ? 'underline' : 'none', fontSize: '25px' }} // Adjust font size
              >
                Results
              </Nav.Link>
              <Nav.Link
                href=""
                onClick={() => { onSelect('team'); setSelectedTab('team'); }}
                style={{ textDecoration: selectedTab === 'team' ? 'underline' : 'none', fontSize: '25px' }} // Adjust font size
              >
                Teams
              </Nav.Link>
              <Nav.Link
                href=""
                onClick={() => { onSelect('match'); setSelectedTab('match'); }}
                style={{ textDecoration: selectedTab === 'match' ? 'underline' : 'none', fontSize: '25px' }} // Adjust font size
              >
                Matches
              </Nav.Link>
            </Nav>
            {/* Add Delete Icon, aligned to the right using 'navbar-right' */}
            <Nav className="navbar-right">
              <Nav.Link href="" onClick={() => handleDeleteClick(1)}>
                <FaTrash style={{ color: 'white' }} />
              </Nav.Link>
              <Nav.Link href="" onClick={() => handleLogClick()}>
                <FaFile style={{ color: 'white' }} />
              </Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>

      {/* Delete Confirmation Modal */}
      <Modal show={showDeleteModal} onHide={() => setShowDeleteModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Confirm Delete</Modal.Title>
        </Modal.Header>
        <Modal.Body>Are you sure you want to delete all entries?</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => { setShowDeleteModal(false); setItemToDelete(null); }}>
            Cancel
          </Button>
          <Button variant="danger" onClick={confirmDelete}>
            Delete
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
};

export default AppNavbar;

import React, { useState } from 'react';
import './Form.css'; // Import the CSS file for styling

const Form = ({ onSubmit }) => {
  const [inputValue, setInputValue] = useState('');
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputValue.trim() === '') {
      setError('Input cannot be empty');
    } else {
      setError('');
      console.log('Form submitted with:', inputValue);
      onSubmit(inputValue);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit} className="form">
        <div className="form-group">
          <textarea
            type="text"
            id="textInput"
            name="textInput"
            value={inputValue}
            onChange={handleChange}
            className="form-control_custom"
          />
          {error && <p className="error">{error}</p>}
        </div>
        <button type="submit" className="submit-button">Submit</button>
      </form>
    </div>
  );
};

export default Form;

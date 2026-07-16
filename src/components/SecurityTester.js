import React, { useState } from 'react';
import './SecurityTester.css';

const SecurityTester = () => {
  const [url, setUrl] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    // perform validation on url and perform animation
      
        const url = e.target.elements.url.value;
      
        const response = await fetch("http://localhost:3000/test-url", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ url }),
        });
      
        const data = await response.json();
        console.log(data.result);
  };

  const handleChange = (e) => {
    setUrl(e.target.value);
  };

  return (
    <div className="security-tester">
      <h2>Enter the URL of the website you want to test for security issues</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="https://example.com"
          value={url}
          onChange={handleChange}
        />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default SecurityTester;

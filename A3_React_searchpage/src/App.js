import React, { useState } from 'react';
import './App.css';

function App() {
  const [searchInput, setSearchInput] = useState('');
  const [searchResult, setSearchResult] = useState('');

  const data = [
    {
      question: 'What is React?',
      answer: 'React is a JavaScript library for building user interfaces.'
    },
    {
      question: 'How do you define a React component?',
      answer: 'A React component is a reusable building block for UI elements.'
    },
    
  ];
  const handleSearch = () => {
    // search logic
    // Convert the search input to lowercase for case-insensitive search
    const lowercaseSearchInput = searchInput.toLowerCase();

    // Find a matching question in the data
    const matchingEntry = data.find(entry => entry.question.toLowerCase().includes(lowercaseSearchInput)
    );

    // Set the search result to the answer if a matching question is found, or a message if not found
    setSearchResult(matchingEntry ? matchingEntry.answer : 'Answer not found.');
  };

  return (
    <div className="App">
      <h1>Search App</h1>
      <input
        type="text"
        placeholder="Enter your search query"
        value={searchInput}
        onChange={(e) => setSearchInput(e.target.value)}
      />
      <button onClick={handleSearch}>Search</button>
      <div className="output">
        
        <p>{searchResult}</p>
      </div>
    </div>
  );
}

export default App;

// src/components/generate.js
import React, { useState, useEffect } from 'react';

const Generate = () => {
  const [numParlays, setNumParlays] = useState(3); // Default to 3 parlays
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const API_URL = 'http://127.0.0.1:8000/generate-moneyline-suggestions/';

  const fetchSuggestions = async () => {
    setLoading(true);
    setError('');

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ num_parlays: numParlays }), // Send num_parlays in the request
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }

      const data = await response.json();
      if (data.success) {
        setSuggestions(data.predictions); // Updated to match the new response structure
      } else {
        throw new Error(data.error || 'Failed to fetch suggestions');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSuggestions();
  }, [numParlays]); // Fetch suggestions whenever numParlays changes

  return (
    <div>
      <h2>Moneyline Parlay Suggestions</h2>

      {/* Input for the number of parlays */}
      <div>
        <label>
          Number of Parlays:
          <input
            type="number"
            value={numParlays}
            onChange={(e) => setNumParlays(Number(e.target.value))}
            min="0"
            max="10"
          />
        </label>
        <button onClick={fetchSuggestions}>Fetch Suggestions</button>
      </div>

      {/* Loading and error messages */}
      {loading && <p>Loading suggestions...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {/* Display suggestions */}
      <ul>
        {suggestions.map((suggestion, index) => (
          <li key={index} style={{ marginBottom: '1em' }}>
            <strong>Teams:</strong> {suggestion.teams} <br />
            <strong>Home Team Odds:</strong> {suggestion.moneyline_odds.home_team} | 
            <strong> Away Team Odds:</strong> {suggestion.moneyline_odds.away_team} <br />
         </li>
        ))}
      </ul>
    </div>
  );
};

export default Generate;

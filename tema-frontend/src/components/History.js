import React, { useEffect, useState } from 'react';
import { getHistory } from '../services/api';

const History = () => {
  const [history, setHistory] = useState([]);  // Initialize history as an empty array
  const [loading, setLoading] = useState(true); // Loading state for async behavior
  const [error, setError] = useState(null);  // Error state to capture any issues

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await getHistory();
        
        console.log('API Response:', response); // Log the full response for debugging

        // Check if response and response.data are valid, and transaction_history exists
        if (response && response.data && Array.isArray(response.data.transaction_history)) {
          setHistory(response.data.transaction_history); // Set state with the valid array
        } else {
          setError('Invalid response data: transaction_history is not an array or is missing');
        }
      } catch (error) {
        setError('Error fetching history: ' + error.message);
      } finally {
        setLoading(false); // Set loading to false after request is done
      }
    };

    fetchHistory();
  }, []);

  if (loading) {
    return <div>Loading...</div>;  // Show loading message while fetching data
  }

  if (error) {
    return <div>{error}</div>;  // Show error message if something went wrong
  }

  return (
    <div className="container mt-4">
      <h2>Transaction History</h2>
      <table className="table">
        <thead>
          <tr>
            <th>Transaction Hash</th>
            <th>Function</th>
            <th>Response</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {history.length > 0 ? (
            history.map((entry, index) => (
              <tr key={index}>
                <td>{entry.transaction_hash}</td>
                <td>{entry.function_called}</td>
                <td>{entry.transaction_response}</td>
                <td>{entry.timestamp}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="4">No transaction history available.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default History;

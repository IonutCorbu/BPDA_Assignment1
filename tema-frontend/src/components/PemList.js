import React, { useState, useEffect } from 'react';
import { listPem } from '../services/api';  // Assuming listPem makes the GET request

const PemList = () => {
  const [pems, setPems] = useState([]);

  useEffect(() => {
    const fetchPemList = async () => {
      try {
        const response = await listPem();
        // Make sure to access the 'uploaded_pem_files' array from the response
        if (response.data && Array.isArray(response.data.uploaded_pem_files)) {
          setPems(response.data.uploaded_pem_files); // Set the array to state
        } else {
          console.error('Unexpected response structure:', response.data);
        }
      } catch (error) {
        console.error('Error fetching PEM list:', error);
      }
    };

    fetchPemList();
  }, []);  // Empty dependency array to run only once when the component mounts

  return (
    <div className="container mt-4">
      <h2>List of Uploaded PEM Files</h2>
      {pems.length > 0 ? (
        <ul>
          {pems.map((pem, index) => (
            <li key={index}>{pem}</li>
          ))}
        </ul>
      ) : (
        <p>No PEM files uploaded yet.</p>
      )}
    </div>
  );
};

export default PemList;

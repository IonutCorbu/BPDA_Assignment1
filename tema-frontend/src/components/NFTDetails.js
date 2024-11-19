import React, { useState, useEffect } from 'react';
import { listPem, getNftDetails } from '../services/api';

const NftDetails = () => {
  const [pemFileName, setPemFileName] = useState('');
  const [nftDetails, setNftDetails] = useState(null);
  const [pemFiles, setPemFiles] = useState([]);
  const [responseMessage, setResponseMessage] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchPemFiles = async () => {
      try {
        const response = await listPem();
        const files = response?.data?.uploaded_pem_files || []; // Ensure response contains uploaded_pem_files
        setPemFiles(files);
      } catch (error) {
        console.error('Error fetching PEM files:', error);
      }
    };

    fetchPemFiles();
  }, []);

  const handlePemChange = async (e) => {
    const selectedPem = e.target.value;
    setPemFileName(selectedPem);

    if (selectedPem) {
      try {
        const response = await getNftDetails(selectedPem);
        setNftDetails(response?.data?.result || {}); // Ensure result exists and set it
      } catch (error) {
        console.error('Error fetching NFT details:', error);
        setNftDetails(null);
      }
    } else {
      setNftDetails(null);
    }
  };

  const handleTransNftProperties = async () => {
    if (!pemFileName) {
      alert('Please select a PEM file first!');
      return;
    }

    setLoading(true);

    try {
      const response = await getNftDetails(pemFileName);
      setResponseMessage(response?.message || 'Transaction successful!');
      alert(response?.message || 'Transaction successful!');
    } catch (error) {
      console.error('Error processing transaction:', error);
      const errorMessage = error.response?.data?.error || 'Error occurred while processing the transaction.';
      setResponseMessage(errorMessage);
      alert(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-4">
      <h2>NFT Details</h2>
      <div className="form-group">
        <label>Select PEM File</label>
        <select
          className="form-control"
          value={pemFileName}
          onChange={handlePemChange}
        >
          <option value="">Select PEM</option>
          {pemFiles && pemFiles.length > 0 ? (
            pemFiles.map((pem, index) => (
              <option key={index} value={pem}>
                {pem}
              </option>
            ))
          ) : (
            <option>No PEM files available</option>
          )}
        </select>
      </div>

      {nftDetails && Object.keys(nftDetails).length > 0 && (
        <div className="mt-4">
          <h4>NFT Details:</h4>
          <pre>{JSON.stringify(nftDetails, null, 2)}</pre>
        </div>
      )}

      <div className="mt-4">
        <button
          className="btn btn-primary"
          onClick={handleTransNftProperties}
          disabled={loading}
        >
          {loading ? 'Processing...' : 'Submit NFT Transaction'}
        </button>
      </div>

      {responseMessage && (
        <div className="mt-4">
          <h4>Response:</h4>
          <pre>{responseMessage}</pre>
        </div>
      )}
    </div>
  );
};

export default NftDetails;

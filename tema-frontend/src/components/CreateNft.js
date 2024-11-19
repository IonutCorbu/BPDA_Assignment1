import React, { useState, useEffect } from 'react';
import { createNft, listPem } from '../services/api';

const CreateNft = () => {
  const [pemFileName, setPemFileName] = useState('');
  const [nftIdentifier, setNftIdentifier] = useState('');
  const [nftName, setNftName] = useState('');
  const [nftDetails, setNftDetails] = useState('');
  const [uri, setUri] = useState('');
  const [pemList, setPemList] = useState([]);
  const [loading, setLoading] = useState(false);
  const [responseData, setResponseData] = useState(null); // Store the full response data


  useEffect(() => {
    const fetchPemList = async () => {
      try {
        const response = await listPem();
        const files = Array.isArray(response.data.uploaded_pem_files) ? response.data.uploaded_pem_files : [];
        setPemList(files);
      } catch (error) {
        console.error('Error fetching PEM list:', error);
      }
    };

    fetchPemList();
  }, []);

  const handleCreateNft = async (e) => {
    e.preventDefault();
    setLoading(true);

    const nftData = {
      nftIdentifier,
      nftName,
      nftDetails,
      uri,
    };

    try {
      const response = await createNft(pemFileName, nftData);
      
      // Directly store the full response data without checking specific fields
      if (response.status === 200 && response.data) {
        setResponseData(response.data); // Save the full response data
        alert('NFT created successfully!');
      } else {
        alert('Failed to create NFT!');
      }
    } catch (error) {
      console.error('Error creating NFT:', error);
      alert('Error creating NFT!');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-4">
      <h2>Create NFT</h2>
      <form onSubmit={handleCreateNft}>
        <div className="form-group">
          <label>Select PEM File</label>
          <select
            className="form-control"
            value={pemFileName}
            onChange={(e) => setPemFileName(e.target.value)}
          >
            <option value="">Select PEM</option>
            {pemList.length > 0 ? (
              pemList.map((pem, index) => (
                <option key={index} value={pem}>
                  {pem}
                </option>
              ))
            ) : (
              <option>No PEM files available</option>
            )}
          </select>
        </div>

        <div className="form-group mt-3">
          <label>NFT Identifier</label>
          <input
            type="text"
            className="form-control"
            value={nftIdentifier}
            onChange={(e) => setNftIdentifier(e.target.value)}
            required
          />
        </div>

        <div className="form-group mt-3">
          <label>NFT Name</label>
          <input
            type="text"
            className="form-control"
            value={nftName}
            onChange={(e) => setNftName(e.target.value)}
            required
          />
        </div>

        <div className="form-group mt-3">
          <label>NFT Details</label>
          <input
            type="text"
            className="form-control"
            value={nftDetails}
            onChange={(e) => setNftDetails(e.target.value)}
            required
          />
        </div>

        <div className="form-group mt-3">
          <label>URI</label>
          <input
            type="text"
            className="form-control"
            value={uri}
            onChange={(e) => setUri(e.target.value)}
            required
          />
        </div>

        <button type="submit" className="btn btn-primary mt-4" disabled={loading}>
          {loading ? 'Creating...' : 'Create NFT'}
        </button>
      </form>

      {responseData && (
        <div className="mt-4">
          <h4>Response Data:</h4>
          <pre>{JSON.stringify(responseData, null, 2)}</pre> {/* Display full response */}
        </div>
      )}
    </div>
  );
};

export default CreateNft;

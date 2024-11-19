import React, { useState, useEffect } from 'react';
import { exchangeNft, listPem } from '../services/api';
import { useNavigate } from 'react-router-dom';

const ExchangeNft = () => {
  const [pemFileName, setPemFileName] = useState('');
  const [nftIdentifier, setNftIdentifier] = useState('');
  const [nftDetails, setNftDetails] = useState('');
  const [ownNftNonce, setOwnNftNonce] = useState('');
  const [pemList, setPemList] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [alertMessage, setAlertMessage] = useState('');
  const [alertType, setAlertType] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchPemList = async () => {
      try {
        const data = await listPem();
        console.log(data);
        if (data.data.uploaded_pem_files && Array.isArray(data.data.uploaded_pem_files)) {
          setPemList(data.data.uploaded_pem_files);
        } else {
          setError('Invalid response format for PEM files');
        }
      } catch (error) {
        setError('Error fetching PEM list: ' + error.message);
      }
    };

    fetchPemList();
  }, []);

  const handleExchangeNft = async (e) => {
    e.preventDefault();
    setLoading(true);

    const nftData = {
      nftIdentifier,
      nftDetails,
      ownNftNonce,
    };

    try {
      await exchangeNft(pemFileName, nftData);
      setAlertType('success');
      setAlertMessage('NFT exchanged successfully!');
      setLoading(false);
    } catch (error) {
      setAlertType('error');
      setAlertMessage('Error exchanging NFT: ' + error.message);
      setLoading(false);
    }
  };

  const handleAlertClose = () => {
    if (alertType === 'success') {
      navigate('/nft-list');
    }
    setAlertMessage('');
    setAlertType('');
  };

  return (
    <div className="container mt-4">
      <h2>Exchange NFT</h2>

      {alertMessage && (
        <div className={`alert alert-${alertType === 'success' ? 'success' : 'danger'}`} role="alert">
          {alertMessage}
          <button className="btn btn-link" onClick={handleAlertClose}>OK</button>
        </div>
      )}

      <form onSubmit={handleExchangeNft}>
        <div className="form-group">
          <label>Select PEM File</label>
          <select
            className="form-control"
            value={pemFileName}
            onChange={(e) => setPemFileName(e.target.value)}
            required
          >
            <option value="">Select PEM</option>
            {pemList.length > 0 ? (
              pemList.map((pem, index) => (
                <option key={index} value={pem}>{pem}</option>
              ))
            ) : (
              <option value="">No PEMs available</option>
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
          <label>Own NFT Nonce</label>
          <input
            type="text"
            className="form-control"
            value={ownNftNonce}
            onChange={(e) => setOwnNftNonce(e.target.value)}
            required
          />
        </div>

        <button type="submit" className="btn btn-primary mt-4" disabled={loading}>
          {loading ? 'Processing...' : 'Exchange NFT'}
        </button>
      </form>
    </div>
  );
};

export default ExchangeNft;

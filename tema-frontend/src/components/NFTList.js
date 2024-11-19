import React, { useState, useEffect } from 'react';

function NftList() {
  const [nfts, setNfts] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch the data from the local NFT supply API
  useEffect(() => {
    const endpoint = 'http://localhost:5000/nft-supply';  // The correct API endpoint

    const fetchData = async () => {
      try {
        const response = await fetch(endpoint);
        const data = await response.text();  // Assuming the response is plain text
        parseNftData(data);  // Parse the raw string to extract NFTs
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  // Parse the raw string response and extract NFT name and attributes
  const parseNftData = (data) => {
    // Regex pattern to capture `name` and `attributes` in the raw data
    const pattern = /name=b'([^']+)', attributes=b'([^']+)'/g;
    const parsedNfts = [];
    let match;

    // Loop through each match of the regex and extract name and attributes
    while ((match = pattern.exec(data)) !== null) {
      const name = match[1].trim();
      const attributesRaw = match[2].trim();

      // Convert the raw attributes from hex-like format (\x00\x00\x01) to a clean string (000001)
      const formattedAttributes = attributesRaw
        .split('\\x')
        .filter(item => item) // Remove any empty items
        .map(hex => hex.padStart(2, '0')) // Ensure each hex byte has two characters
        .join('');

      // Push each NFT entry into the parsedNfts array
      parsedNfts.push({
        name: name,
        attributes: formattedAttributes
      });
    }

    // Update the state with the parsed NFT data
    setNfts(parsedNfts);
    setLoading(false);  // Set loading to false once the data is parsed
  };

  return (
    <div>
      {loading ? (
        <p>Loading NFTs...</p>
      ) : (
        <div>
          <h1>NFT List</h1>
          <table border="1" cellPadding="10">
            <thead>
              <tr>
                <th>Name</th>
                <th>Attributes</th>
              </tr>
            </thead>
            <tbody>
              {nfts.map((nft, index) => (
                <tr key={index}>
                  <td>{nft.name}</td>
                  <td>{nft.attributes}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default NftList;

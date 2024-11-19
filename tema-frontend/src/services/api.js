import axios from 'axios';

const API_URL = "http://localhost:5000";  


export const uploadPem = (formData) => {
  return axios.post(`${API_URL}/upload-pem`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    }
  });
};


export const listPem = () => {
  return axios.get(`${API_URL}/list-pem`);
};


export const getNftSupply = () => {
  return axios.get(`${API_URL}/nft-supply`);
};


export const getNftDetails = (pemFileName) => {
  return axios.post(`${API_URL}/trans-nft-properties`, { file_name: pemFileName });
};

export const createNft = (pemFileName, nftData) => {
    return axios.post(`${API_URL}/create-nft`, {
        ntf_identifier: nftData.nftIdentifier,  
        nftName: nftData.nftName,              
        nftDetails: nftData.nftDetails,        
        uri: nftData.uri,                      
        file_name: pemFileName                 
      });
};

export const exchangeNft = (pemFileName, nftData) => {
    const { nftIdentifier, nftDetails, ownNftNonce } = nftData;
  
    return axios.post(`${API_URL}/exchange-nft`, {
      file_name: pemFileName,  
      nftDetails: nftDetails,  
      ntf_identifier: nftIdentifier,  
      own_nft_nounce: ownNftNonce  
    });
  };

export const getHistory = () => {
  return axios.get(`${API_URL}/history`);
};
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar.js';
import PemUpload from './components/PemUpload';
import PemList from './components/PemList';
import NftList from './components/NFTList';
import NftDetails from './components/NFTDetails';
import CreateNft from './components/CreateNft';
import ExchangeNft from './components/ExchangeNft';
import History from './components/History';

const App = () => {
  return (
    <Router>
      <Navbar />
      <div className="container mt-4">
      <Routes>
          <Route path="/" element={<History />} />
          <Route path="/upload-pem" element={<PemUpload/>} />
          <Route path="/list-pem" element={<PemList/>} />
          <Route path="/nft-list" element={<NftList/>} />
          <Route path="/nft-details" element={<NftDetails/>} />
          <Route path="/create-nft" element={<CreateNft/>} />
          <Route path="/exchange-nft" element={<ExchangeNft/>} />
          <Route path="/history" element={<History/>} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;

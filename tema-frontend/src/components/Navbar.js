import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <a className="navbar-brand" href="/">NFT App</a>
      <div className="collapse navbar-collapse" id="navbarNav">
        <ul className="navbar-nav">
          <li className="nav-item">
            <Link className="nav-link" to="/upload-pem">Upload PEM</Link>
          </li>
          <li className="nav-item">
            <Link className="nav-link" to="/list-pem">List PEMs</Link>
          </li>
          <li className="nav-item">
            <Link className="nav-link" to="/nft-list">NFT List</Link>
          </li>
          <li className="nav-item">
            <Link className="nav-link" to="/nft-details">NFT Details</Link>
          </li>
          <li className="nav-item">
            <Link className="nav-link" to="/create-nft">Create NFT</Link>
          </li>
          <li className="nav-item">
            <Link className="nav-link" to="/exchange-nft">Exchange NFT</Link>
          </li>
          <li className="nav-item">
            <Link className="nav-link" to="/history">History</Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;

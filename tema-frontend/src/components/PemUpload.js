import React, { useState } from 'react';
import { uploadPem } from '../services/api';
import { useNavigate } from 'react-router-dom'; // Updated import

const PemUpload = () => {
  const [file, setFile] = useState(null);
  const navigate = useNavigate(); // Updated usage of useNavigate

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (file) {
      const formData = new FormData();
      formData.append('file', file);
      try {
        await uploadPem(formData);
        navigate('/list-pem');  // Use navigate instead of history.push
      } catch (error) {
        console.error('Error uploading PEM:', error);
      }
    }
  };

  return (
    <div className="container mt-4">
      <h2>Upload PEM File</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="pemFile">Choose PEM File</label>
          <input type="file" id="pemFile" className="form-control" onChange={handleFileChange} />
        </div>
        <button type="submit" className="btn btn-primary mt-3">Upload</button>
      </form>
    </div>
  );
};

export default PemUpload;

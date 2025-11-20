import React, { useState, useEffect } from 'react';
import { getContracts } from '../services/api.js';
import './ContractList.css';

function ContractList({ refreshTrigger }) {
  const [contracts, setContracts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchContracts();
  }, [refreshTrigger]);

  const fetchContracts = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await getContracts(0, 20);
      setContracts(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch contracts');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'processed':
        return '#4caf50';
      case 'processing':
        return '#ff9800';
      case 'failed':
        return '#f44336';
      default:
        return '#9e9e9e';
    }
  };

  if (loading) {
    return <div className="contract-list loading">Loading contracts...</div>;
  }

  if (error) {
    return <div className="contract-list error">Error: {error}</div>;
  }

  return (
    <div className="contract-list">
      <h2>Recent Contracts</h2>
      {contracts.length === 0 ? (
        <p className="no-contracts">No contracts uploaded yet.</p>
      ) : (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Filename</th>
                <th>Upload Date</th>
                <th>Size</th>
                <th>Entities</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {contracts.map((contract) => (
                <tr key={contract.id}>
                  <td className="filename">{contract.filename}</td>
                  <td>{formatDate(contract.upload_date)}</td>
                  <td>{formatFileSize(contract.file_size)}</td>
                  <td className="entities-count">{contract.entities_count}</td>
                  <td>
                    <span
                      className="status-badge"
                      style={{ backgroundColor: getStatusColor(contract.status) }}
                    >
                      {contract.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default ContractList;

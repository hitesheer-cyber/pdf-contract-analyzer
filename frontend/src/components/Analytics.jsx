import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { getAnalytics } from '../services/api.js';
import './Analytics.css';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D'];

function Analytics({ refreshTrigger }) {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAnalytics();
  }, [refreshTrigger]);

  const fetchAnalytics = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await getAnalytics();
      setAnalytics(data);
    } catch (err) {
      console.error('Analytics fetch error:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to fetch analytics');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="analytics loading">Loading analytics...</div>;
  }

  if (error) {
    return <div className="analytics error">Error: {error}</div>;
  }

  if (!analytics) {
    return null;
  }

  // Prepare data for charts
  const entityTypeData = Object.entries(analytics.entity_type_distribution || {}).map(
    ([type, count]) => ({ name: type, value: count })
  );

  const frequentEntitiesData = (analytics.most_frequent_entities || []).slice(0, 8).map(
    (item) => ({ name: item.text, count: item.count })
  );

  return (
    <div className="analytics">
      <h2>Analytics Dashboard</h2>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Contracts</h3>
          <div className="stat-value">{analytics.total_contracts}</div>
        </div>
        <div className="stat-card">
          <h3>Total Entities</h3>
          <div className="stat-value">{analytics.total_entities}</div>
        </div>
        <div className="stat-card">
          <h3>Avg Entities/Contract</h3>
          <div className="stat-value">
            {analytics.total_contracts > 0
              ? Math.round(analytics.total_entities / analytics.total_contracts)
              : 0}
          </div>
        </div>
      </div>

      <div className="charts-grid">
        <div className="chart-container">
          <h3>Entity Type Distribution</h3>
          {entityTypeData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={entityTypeData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {entityTypeData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <p>No entity data available</p>
          )}
        </div>

        <div className="chart-container">
          <h3>Most Frequent Entities</h3>
          {frequentEntitiesData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={frequentEntitiesData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="count" fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p>No entity data available</p>
          )}
        </div>
      </div>

      {analytics.contracts_missing_key_entities && analytics.contracts_missing_key_entities.length > 0 && (
        <div className="missing-entities">
          <h3>Contracts with Missing Key Entities</h3>
          <div className="missing-list">
            {analytics.contracts_missing_key_entities.map((contract) => (
              <div key={contract.id} className="missing-item">
                <strong>{contract.filename}</strong>
                <span className="missing-types">
                  Missing: {contract.missing_types.join(', ')}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default Analytics;

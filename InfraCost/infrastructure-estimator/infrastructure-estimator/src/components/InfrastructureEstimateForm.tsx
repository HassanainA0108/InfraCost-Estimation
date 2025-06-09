import React, { useState } from 'react';

function InfrastructureEstimateForm(): React.ReactElement {
  const [formData, setFormData] = useState({
    vmType: 'medium',
    vmCount: 1,
    dbType: 'standard',
    dbCount: 1,
    storageType: 'standard',
    storageGB: 100,
    bandwidthGB: 50,
  });

  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'vmCount' || name === 'dbCount' || name === 'storageGB' || name === 'bandwidthGB' ? parseInt(value) : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://127.0.0.1:5000/api/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Failed to calculate cost. Please try again.');
      }

      const data = await response.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            VM Type:
            <select name="vmType" value={formData.vmType} onChange={handleChange}>
              <option value="small">Small</option>
              <option value="medium">Medium</option>
              <option value="large">Large</option>
            </select>
          </label>
        </div>
        <div>
          <label>
            VM Count:
            <input
              type="number"
              name="vmCount"
              value={formData.vmCount}
              onChange={handleChange}
              min="0"
            />
          </label>
        </div>
        <div>
          <label>
            Database Type:
            <select name="dbType" value={formData.dbType} onChange={handleChange}>
              <option value="standard">Standard</option>
              <option value="performant">Performant</option>
            </select>
          </label>
        </div>
        <div>
          <label>
            Database Count:
            <input
              type="number"
              name="dbCount"
              value={formData.dbCount}
              onChange={handleChange}
              min="0"
            />
          </label>
        </div>
        <div>
          <label>
            Storage Type:
            <select name="storageType" value={formData.storageType} onChange={handleChange}>
              <option value="standard">Standard</option>
              <option value="ssd">SSD</option>
            </select>
          </label>
        </div>
        <div>
          <label>
            Storage (GB):
            <input
              type="number"
              name="storageGB"
              value={formData.storageGB}
              onChange={handleChange}
              min="0"
            />
          </label>
        </div>
        <div>
          <label>
            Bandwidth (GB):
            <input
              type="number"
              name="bandwidthGB"
              value={formData.bandwidthGB}
              onChange={handleChange}
              min="0"
            />
          </label>
        </div>
        <button type="submit">Calculate Cost</button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}
      {result && (
        <div>
          <h3>Cost Estimate</h3>
          <p>Total Cost: ${result.totalCost}</p>
          <ul>
            {Object.entries(result.breakdown).map(([key, value]: any) => (
              <li key={key}>
                <strong>{value.label}:</strong> ${value.cost} ({value.details})
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default InfrastructureEstimateForm;
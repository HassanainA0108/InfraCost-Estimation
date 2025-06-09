import React from 'react';
import InfrastructureEstimateForm from './components/InfrastructureEstimateForm'; // Ensure correct path
import './App.css'; // Optional: Your main app styles

function App(): React.ReactElement {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to the Infrastructure Estimator</h1>
      </header>
      <main>
        <InfrastructureEstimateForm />
      </main>
    </div>
  );
}

export default App;
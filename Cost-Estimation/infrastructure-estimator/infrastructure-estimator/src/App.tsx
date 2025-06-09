// In App.tsx
import React from 'react';
import InfrastructureEstimateForm from './InfrastructureEstimateForm'; // Ensure correct path
import './App.css'; // Optional: Your main app styles

function App(): JSX.Element { // Add return type for the component
  return (
    <div className="App">
      <header className="App-header">
        {/* Other components or headers */}
      </header>
      <main>
        <InfrastructureEstimateForm />
      </main>
    </div>
  );
}

export default App;
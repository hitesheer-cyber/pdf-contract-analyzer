import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import Analytics from './components/Analytics';
import ContractList from './components/ContractList';
import './App.css';

function App() {
  const [refreshKey, setRefreshKey] = useState(0);

  const handleUploadSuccess = () => {
    // Trigger refresh of analytics and contract list
    setRefreshKey(oldKey => oldKey + 1);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>📄 Contract Entity Extraction & Analytics</h1>
        <p>AI-powered contract analysis powered by Hugging Face Transformers</p>
      </header>

      <main className="App-main">
        <FileUpload onUploadSuccess={handleUploadSuccess} />
        <Analytics refreshTrigger={refreshKey} />
        <ContractList refreshTrigger={refreshKey} />
      </main>

      <footer className="App-footer">
        <p>Built with FastAPI, React, and Hugging Face Transformers</p>
      </footer>
    </div>
  );
}

export default App;

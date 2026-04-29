import { useState } from 'react';
import SearchBar from './components/SearchBar';
import ResultsList from './components/ResultsList';
import { searchExperts } from './api';

function App() {
  const [results, setResults] = useState([]);
  const [count, setCount] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async (query, domain) => {
    setIsLoading(true);
    setError(null);
    setHasSearched(true);
    
    try {
      const data = await searchExperts(query, domain);
      setResults(data.experts || []);
      setCount(data.count || 0);
    } catch (err) {
      setError("Failed to fetch experts. Please ensure backend is running.");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>LinkedIn Similar Expert Finder</h1>
        <p>Discover high-quality technical professionals tailored to your domain</p>
      </header>
      
      <main className="app-main">
        <SearchBar onSearch={handleSearch} isLoading={isLoading} />
        
        {error && (
          <div className="error-message">
            <p>{error}</p>
          </div>
        )}
        
        {hasSearched && !isLoading && !error && (
          <ResultsList results={results} count={count} />
        )}
        
        {isLoading && (
          <div className="loading-state">
            <div className="spinner"></div>
            <p>Analyzing candidates and ranking quality...</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;

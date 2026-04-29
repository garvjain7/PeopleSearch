import { useState } from 'react';

const SearchBar = ({ onSearch, isLoading }) => {
  const [query, setQuery] = useState('');
  const [domain, setDomain] = useState('AI Infrastructure');

  const domains = [
    'AI Infrastructure',
    'Backend Systems',
    'RAG / Vector DB',
    'LLMOps',
    'Applied AI'
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query, domain);
    }
  };

  return (
    <div className="search-container">
      <form className="search-form" onSubmit={handleSubmit}>
        <div className="input-group">
          <input
            type="text"
            className="search-input"
            placeholder="Search by profile or keywords (e.g. 'RAG Engineer')"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={isLoading}
          />
        </div>
        
        <div className="input-group">
          <select 
            className="domain-select"
            value={domain}
            onChange={(e) => setDomain(e.target.value)}
            disabled={isLoading}
          >
            {domains.map((d) => (
              <option key={d} value={d}>{d}</option>
            ))}
          </select>
        </div>

        <button 
          type="submit" 
          className={`search-btn ${isLoading ? 'loading' : ''}`}
          disabled={isLoading || !query.trim()}
        >
          {isLoading ? 'Searching...' : 'Find Similar Experts'}
        </button>
      </form>
    </div>
  );
};

export default SearchBar;

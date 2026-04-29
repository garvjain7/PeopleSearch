import ExpertCard from './ExpertCard';

const ResultsList = ({ results, count }) => {
  if (!results || results.length === 0) {
    return (
      <div className="empty-state">
        <p>No experts found. Try a different query or domain.</p>
      </div>
    );
  }

  return (
    <div className="results-container">
      <div className="results-header">
        <h2>Discovery Results</h2>
        <span className="results-count">Found {count} expert{count !== 1 ? 's' : ''}</span>
      </div>
      
      <div className="cards-grid">
        {results.map((expert, idx) => (
          <ExpertCard key={idx} expert={expert} />
        ))}
      </div>
    </div>
  );
};

export default ResultsList;

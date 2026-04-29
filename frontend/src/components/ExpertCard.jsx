const ExpertCard = ({ expert }) => {
  const { profile, score, reason } = expert;
  
  // Extract initials for fallback avatar
  const getInitials = (name) => {
    const parts = name.split(' ');
    if (parts.length > 1) {
      return (parts[0][0] + parts[1][0]).toUpperCase();
    }
    return name.substring(0, 2).toUpperCase();
  };

  return (
    <div className="expert-card">
      <div className="card-header">
        <div className="avatar">
          {profile.image_url ? (
            <img src={profile.image_url} alt={profile.name} />
          ) : (
            <div className="avatar-fallback">{getInitials(profile.name)}</div>
          )}
        </div>
        <div className="card-title">
          <h3>{profile.name}</h3>
          <p className="role">{profile.title}</p>
          {profile.company && profile.company !== "Unknown" && (
            <span className="company-badge">{profile.company}</span>
          )}
        </div>
        <div className="score-container">
          <div className="score-badge">
            <span className="score-value">{score}</span>
            <span className="score-max">/100</span>
          </div>
          <span className="score-label">Match Score</span>
        </div>
      </div>
      
      <div className="card-body">
        <div className="reason-box">
          <span className="reason-icon">⚡</span>
          <p className="reason-text">{reason}</p>
        </div>
        <div className="snippet-box">
          <p>{profile.snippet}</p>
        </div>
      </div>
      
      <div className="card-footer">
        <a 
          href={profile.url} 
          target="_blank" 
          rel="noopener noreferrer" 
          className="linkedin-btn"
        >
          Open LinkedIn Profile
        </a>
      </div>
    </div>
  );
};

export default ExpertCard;

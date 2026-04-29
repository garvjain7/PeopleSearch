export const searchExperts = async (query, domain) => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/experts/find', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query, domain }),
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error("Error fetching experts:", error);
    throw error;
  }
};

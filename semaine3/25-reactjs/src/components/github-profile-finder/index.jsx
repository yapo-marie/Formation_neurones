import { useEffect, useState, useCallback } from "react";
import User from "./user";
import './styles.css';

export default function GithubProfileFinder() {
  const [userName, setUserName] = useState("sangammukherjee");
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchGithubUserData = useCallback(async () => {
    if (!userName) return;

    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`https://api.github.com/users/${userName}`);
      if (!res.ok) {
        throw new Error("Utilisateur non trouvé");
      }
      const data = await res.json();
      setUserData(data);
    } catch (err) {
      setUserData(null);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [userName]);

  const handleSubmit = () => {
    fetchGithubUserData();
  };

  useEffect(() => {
    fetchGithubUserData();
  }, [fetchGithubUserData]);

  return (
    <div className="github-profile-container">
      <div className="input-wrapper">
        <input
          name="search-by-username"
          type="text"
          placeholder="Search Github Username..."
          value={userName}
          onChange={(e) => setUserName(e.target.value)}
        />
        <button onClick={handleSubmit}>Search</button>
      </div>

      {loading && <h1>Loading data! Please wait...</h1>}
      {error && <p style={{ color: "red" }}>{error}</p>}
      {userData && <User user={userData} />}
    </div>
  );
}

import { useEffect, useState } from "react";
import Suggestions from "./suggesstions";

export default function SearchAutocomplete() {
  const [loading, setLoading] = useState(false);
  const [users, setUsers] = useState([]);
  const [searchParam, setSearchParam] = useState("");
  const [showDropdown, setShowDropdown] = useState(false);
  const [filteredUsers, setFilteredUsers] = useState([]);
  const [error, setError] = useState(null);

  const handleChange = (event) => {
    const query = event.target.value.toLowerCase();
    setSearchParam(query);

    if (query.length > 1 && users.length > 0) {
      const filtered = users.filter((item) =>
        item.toLowerCase().includes(query)
      );
      setFilteredUsers(filtered);
      setShowDropdown(true);
    } else {
      setShowDropdown(false);
      setFilteredUsers([]);
    }
  };

  const handleClick = (event) => {
    setSearchParam(event.target.innerText);
    setFilteredUsers([]);
    setShowDropdown(false);
  };

  const fetchListOfUsers = async () => {
    try {
      setLoading(true);
      const response = await fetch("https://dummyjson.com/users");
      const data = await response.json();

      if (data?.users?.length > 0) {
        const userNames = data.users.map((user) => user.firstName);
        setUsers(userNames);
      } else {
        setUsers([]);
        setError("Aucun utilisateur trouvé");
      }
    } catch (err) {
      setError("Erreur lors du chargement des utilisateurs");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchListOfUsers();
  }, []);

  return (
    <div className="search-autocomplete-container">
      {loading ? (
        <h1>Loading data... Please wait.</h1>
      ) : (
        <input
          type="text"
          name="search-users"
          placeholder="Search users here..."
          value={searchParam}
          onChange={handleChange}
        />
      )}

      {error && <p style={{ color: "red" }}>{error}</p>}

      {showDropdown && filteredUsers.length > 0 && (
        <Suggestions handleClick={handleClick} data={filteredUsers} />
      )}
    </div>
  );
}

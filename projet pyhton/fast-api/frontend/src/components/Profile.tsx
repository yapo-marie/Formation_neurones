import { useNavigate } from "react-router";
import BooksList from "./BooksList";

export default function Profile() {
  const navigate = useNavigate();

  const signOut = () => {
    localStorage.removeItem("temitope");
    navigate("/");
  };

  return (
    <>
      <div style={{ marginTop: 20, minHeight: 700 }}>
        <h1>Profile page</h1>
        <p>Hello there, welcome to your profile page</p>
        <BooksList />
        <button onClick={signOut}>sign out</button>
      </div>
    </>
  );
}

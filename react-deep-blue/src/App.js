import React, { useState } from "react";
import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Signup from "./components/Signup";
import Login from "./components/Login";
import Navbar from "./components/Navbar";
import MainPage from "./components/MainPage";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const LogIn = () => {
    setIsLoggedIn(true);
  };
  if (!isLoggedIn) {
    return (
      <>
        <Router>
          <Routes>
            <Route exact path="/" element={<Signup loggedIn={LogIn} />} />
            <Route exact path="/login" element={<Login loggedIn={LogIn} />} />
          </Routes>
        </Router>
      </>
    );
  }

  return (
    <>
      <Router>
        <Navbar setIsLoggedIn={setIsLoggedIn} />
        <Routes>
          <Route exact path="/" element={<MainPage />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;

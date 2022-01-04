import React from "react";
import { NavLink, useNavigate } from "react-router-dom";

import "./Navbar.css";

const Navbar = (props) => {
  const navigate = useNavigate();
  const navigateHandler = (event) => {
    props.setIsLoggedIn(false);
    navigate("/login");
  };

  return (
    <div className="topnav" id="myTopnav">
      <NavLink to="/">Summarize</NavLink>{" "}      
      <button id="btn" onClick={navigateHandler}>Logout</button>
    </div>
  );
};
export default Navbar;

import React from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Signup.css";

const Login = (props) => {
  const navigate = useNavigate();
  const submitHandler = (event) => {
    event.preventDefault();
    navigate("/");
    props.loggedIn();
  };
  return (
    <div id="formDiv">
      <form onSubmit={submitHandler}>
        <label htmlFor="emailID">Enter your email address: </label>
        <input type="email" id="emailID" required />
        <label htmlFor="password">Enter your password: </label>
        <input type="password" id="password" required />
        <div style={{ textAlign: "right" }}>
          <small>Forgot passwod?</small>
        </div>
        <div>
          <button
            type="submit"
            style={{
              display: "block",
              margin: "0 auto",
              border: "none",
              borderRadius: "2px",
            }}
          >
            Log In
          </button>
        </div>
      </form>
      <p>
        New User? <Link to="/">Click here.</Link>
      </p>
    </div>
  );
};

export default Login;

import React from "react";
import { Link } from "react-router-dom";
import "./Signup.css";

const Signup = (props) => {
  const submitHandler = (event) => {
    event.preventDefault();
    props.loggedIn();
  };
  return (
    <div id="formDiv">
      <form onSubmit={submitHandler}>
        <label htmlFor="emailID">Enter your email address : </label>
        <input id="emailID" type="email" required />
        <label htmlFor="phoneNumber">Enter your phone number : </label>
        <input id="phoneNumber" type="tel" required />
        <label htmlFor="passWord">Set the password : </label>
        <input id="passWord" type="password" required />
        <label htmlFor="Password">Confirm password : </label>
        <input id="Password" type="password" required />
        <button
          type="submit"
          style={{
            display: "block",
            margin: "0 auto",
            border: "none",
            borderRadius: "2px",
          }}
        >
          Submit
        </button>
      </form>
      <p>
        Already have an account? <Link to="/login">Click here.</Link>
      </p>
    </div>
  );
};

export default Signup;

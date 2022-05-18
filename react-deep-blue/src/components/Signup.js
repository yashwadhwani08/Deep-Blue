import React, { useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import "./Signup.css";

const Signup = (props) => {
  const valInput = useRef();
  useEffect(() => {
    fetchUser();
  }, []);
  const submitHandler = (event) => {
    event.preventDefault();
    // props.loggedIn();
    fetchUser();
    fetchParticularUser();
  };

  const fetchUser = () => {
    fetch("http://127.0.0.1:8000/api/user-list/")
      .then((response) => response.json())
      .then((data) => {
        console.log("Data: ", data);
      });
  };

  const fetchParticularUser = () => {
    const tempValue = valInput.current.value;
    // console.log(valInput);
    // console.log(valInput.current);
    // console.log(valInput.current.value);
    fetch(`http://127.0.0.1:8000/api/user-detail/${tempValue}`)
      .then((response) => response.json())
      .then((data) => {
        console.log("Data: ", data);
      });
  };

  return (
    <div id="formDiv">
      <form onSubmit={submitHandler}>
        <label htmlFor="emailID">Enter your email address : </label>
        <input id="emailID" type="email" ref={valInput} required />
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

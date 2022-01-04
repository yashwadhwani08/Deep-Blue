import React from "react";
import "./MainPage.css";

const MainPage = () => {
  return (
    <div className="row">
      <div className="column left">
        <label htmlFor="content">Enter your transcript here: </label>
        <textarea
          id="content"
          rows="30"
          style={{ "overflow-y": "scroll", width: "100%" }}
        />
      </div>
      <div className="column middle" style={{ textAlign: "center" }}>
        <button style={{ marginTop: "500px" }}>Summarize</button>
      </div>
      <div className="column right">
        <label htmlFor="contentSummary">Summary here : </label>
        <textarea
          id="contentSummary"
          rows="30"
          style={{ "overflow-y": "scroll", width: "100%" }}
          readOnly
        />
      </div>
    </div>
  );
};

export default MainPage;

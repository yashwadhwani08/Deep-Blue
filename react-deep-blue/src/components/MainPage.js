import React from "react";
import "./MainPage.css";

const MainPage = () => {
  return (
    <div className="row">
      <div className="column left" style={{ "background-color": "#F5F5F5" }}>
        <label htmlFor="content">Enter your transcript here: </label>
        <textarea
          id="content"
          rows="20"
          width="100%"
          style={{ "overflow-y": "scroll" }}
        />
      </div>
      <div className="column middle">
        <button>Summarize</button>
      </div>
      <div className="column right" style={{ "background-color": "#F5F5F5." }}>
        <label htmlFor="contentSummary">Summary here : </label>
        <textarea
          id="contentSummary"
          rows="20"
          width="100%"
          style={{ "overflow-y": "scroll" }}
        />
      </div>
    </div>
  );
};

export default MainPage;

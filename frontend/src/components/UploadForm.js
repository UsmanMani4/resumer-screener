import React, { useState } from "react";
import "./UploadForm.css";

function UploadForm() {
  const [file, setFile] = useState(null);
  const [jd, setJD] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("jd", jd);

      const response = await fetch("http://127.0.0.1:8000/score_resume", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      setResult(data);
    } catch (err) {
      alert("Error: Could not process resume");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard-container">
      <h1 className="title">AI Resume Screener Dashboard</h1>
      <form onSubmit={handleSubmit} className="form">
        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
          className="file-input"
        />
        <textarea
          placeholder="Paste job description here..."
          value={jd}
          onChange={(e) => setJD(e.target.value)}
          rows="6"
          className="jd-input"
        />
        <button type="submit" className="submit-btn">Upload & Analyze</button>
      </form>

      {loading && <p className="loading">Processing resume...</p>}

      {result && (
  <div className="dashboard">
    <div className="card">
      <h3>Resume Score</h3>
      <p className="score">{result.resume_score}</p>
      <p><strong>Feedback:</strong> {result.feedback}</p>
    </div>
    <div className="card">
      <h3>Job Match Analysis</h3>
      {result.match_percentage !== null ? (
        <p className="match">{result.match_percentage}%</p>
      ) : (
        <p>No job description provided</p>
      )}
    </div>
  </div>
)}

    </div>
  );
}

export default UploadForm;

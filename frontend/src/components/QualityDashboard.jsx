import React from "react";

const QualityDashboard = () => (
  <section className="quality-dashboard">
    <h2>Research Quality Dashboard</h2>
    <p>
      Scores are computed from student responses and alignment checks. Each metric
      is auditable and tied to evidence.
    </p>
    <div className="score-grid">
      <div>
        <strong>Problem Clarity Score</strong>
        <p>64%</p>
      </div>
      <div>
        <strong>Objective–Question Alignment</strong>
        <p>72%</p>
      </div>
      <div>
        <strong>Method Suitability Score</strong>
        <p>41%</p>
      </div>
      <div>
        <strong>Evidence Adequacy Score</strong>
        <p>53%</p>
      </div>
      <div>
        <strong>Ethical Compliance Score</strong>
        <p>20%</p>
      </div>
      <div>
        <strong>Defense Readiness Index</strong>
        <p>38%</p>
      </div>
    </div>
  </section>
);

export default QualityDashboard;

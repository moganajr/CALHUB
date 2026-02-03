import React from "react";

const SupervisorDashboard = () => (
  <section className="supervisor-dashboard">
    <h2>Supervisor Dashboard</h2>
    <p>
      Inspect logic maps, quality scores, and AI transparency logs before
      approving or triggering revisions.
    </p>
    <div className="score-grid">
      <div>
        <strong>Problem Clarity</strong>
        <p>58%</p>
      </div>
      <div>
        <strong>Objective–Question Alignment</strong>
        <p>71%</p>
      </div>
      <div>
        <strong>Method Suitability</strong>
        <p>45%</p>
      </div>
      <div>
        <strong>Defense Readiness Index</strong>
        <p>39%</p>
      </div>
    </div>
    <div className="prompt-list">
      <h3>Supervisor Prompts</h3>
      <ul>
        <li>Where is the empirical gap articulated?</li>
        <li>How are quantitative variables operationalized?</li>
        <li>Why is this research design appropriate?</li>
      </ul>
    </div>
  </section>
);

export default SupervisorDashboard;

import React from "react";

const StudentWorkspace = () => (
  <section className="student-workspace">
    <h2>Question-Driven Thinking Engine</h2>
    <p>
      Responses are the source of truth. Free-form proposal text is disabled
      until logical completeness and alignment checks pass.
    </p>
    <form className="question-form">
      <fieldset>
        <legend>Problem Statement</legend>
        <label htmlFor="gap">
          What is the empirical gap?
          <textarea id="gap" name="gap" rows="3" placeholder="Describe the gap" />
        </label>
        <label htmlFor="why">
          Why is this gap significant?
          <textarea id="why" name="why" rows="3" placeholder="Explain significance" />
        </label>
      </fieldset>
      <button type="button">Save Response</button>
    </form>
  </section>
);

export default StudentWorkspace;

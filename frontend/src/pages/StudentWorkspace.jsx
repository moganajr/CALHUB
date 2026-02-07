import React, { useEffect, useMemo, useState } from "react";

const sections = [
  {
    id: "problem",
    title: "Problem Statement",
    questions: [
      { id: "gap", label: "What is the empirical gap?" },
      { id: "significance", label: "Why is this gap significant?" },
      { id: "context", label: "What context makes the gap urgent?" }
    ]
  },
  {
    id: "objectives",
    title: "Research Objectives",
    questions: [
      { id: "objective-1", label: "State the primary objective in measurable terms." },
      { id: "objective-2", label: "State a secondary objective that supports the primary." }
    ]
  },
  {
    id: "methodology",
    title: "Methodology Guardrails",
    questions: [
      { id: "design", label: "Which research design is appropriate and why?" },
      { id: "variables", label: "How are key variables operationalized?" },
      { id: "analysis", label: "Which analysis plan fits the design?" }
    ]
  }
];

const StudentWorkspace = () => {
  const [activeIndex, setActiveIndex] = useState(0);
  const [responses, setResponses] = useState(() => {
    const stored = localStorage.getItem("rds-responses");
    return stored ? JSON.parse(stored) : {};
  });

  useEffect(() => {
    localStorage.setItem("rds-responses", JSON.stringify(responses));
  }, [responses]);

  const activeSection = sections[activeIndex];
  const isComplete = useMemo(() => {
    return activeSection.questions.every((question) => responses[question.id]?.trim());
  }, [activeSection, responses]);

  const handleChange = (questionId, value) => {
    setResponses((prev) => ({ ...prev, [questionId]: value }));
  };

  return (
    <section className="student-workspace">
      <h2>Question-Driven Thinking Engine</h2>
      <p>
        Responses are the source of truth. Free-form proposal text is disabled
        until logical completeness and alignment checks pass.
      </p>
      <form className="question-form">
        <fieldset>
          <legend>{activeSection.title}</legend>
          {activeSection.questions.map((question) => (
            <label htmlFor={question.id} key={question.id}>
              {question.label}
              <textarea
                id={question.id}
                name={question.id}
                rows="3"
                value={responses[question.id] || ""}
                placeholder="Provide a concise, evidence-based response"
                onChange={(event) => handleChange(question.id, event.target.value)}
              />
            </label>
          ))}
        </fieldset>
        <div className="form-actions">
          <button
            type="button"
            onClick={() => setActiveIndex((index) => Math.max(index - 1, 0))}
            disabled={activeIndex === 0}
          >
            Previous Section
          </button>
          <button type="button" disabled={!isComplete}>
            Save &amp; Continue
          </button>
          <button
            type="button"
            onClick={() => setActiveIndex((index) => Math.min(index + 1, sections.length - 1))}
            disabled={!isComplete || activeIndex === sections.length - 1}
          >
            Next Section
          </button>
        </div>
      </form>
      <p className="autosave-note">Autosave active (offline-ready via local storage).</p>
    </section>
  );
};

export default StudentWorkspace;

import React from "react";

import AlignmentGate from "./components/AlignmentGate.jsx";
import CompletenessGate from "./components/CompletenessGate.jsx";
import QualityDashboard from "./components/QualityDashboard.jsx";
import SupervisorDashboard from "./pages/SupervisorDashboard.jsx";
import StudentWorkspace from "./pages/StudentWorkspace.jsx";

const App = () => (
  <div className="app-shell">
    <header className="app-header">
      <h1>Research Development System</h1>
      <p>Structured thinking before writing. Transparent AI support only.</p>
    </header>
    <main>
      <StudentWorkspace />
      <section className="gates">
        <CompletenessGate />
        <AlignmentGate />
      </section>
      <QualityDashboard />
      <SupervisorDashboard />
    </main>
  </div>
);

export default App;

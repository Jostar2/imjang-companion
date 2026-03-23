import { ProjectShell } from "../components/projects/project-shell";
import { AuthPanel } from "../components/auth/auth-panel";

export default function HomePage() {
  return (
    <ProjectShell
      title="Imjang Companion MVP"
      description="A mobile-first workspace for field visits, structured scoring, property comparison, and post-visit reporting."
      tags={["Real estate", "Field visit", "Mobile-first"]}
    >
      <section className="section-grid">
        <article className="card">
          <h3>Core MVP</h3>
          <ul className="list">
            <li>Create visit projects</li>
            <li>Register candidate properties</li>
            <li>Capture visit notes and scores</li>
            <li>Compare properties and review red flags</li>
          </ul>
        </article>
        <article className="card">
          <h3>First Release Constraints</h3>
          <ul className="list">
            <li>Manual property entry only</li>
            <li>No production OCR or legal due diligence</li>
            <li>Staging-ready flow before production</li>
          </ul>
        </article>
        <article className="card">
          <h3>Planning Status</h3>
          <p>
            Planning, architecture, and bounded task packets are prepared under the current run
            package so the first backend and frontend slices can start without widening scope.
          </p>
        </article>
      </section>
      <AuthPanel />
    </ProjectShell>
  );
}

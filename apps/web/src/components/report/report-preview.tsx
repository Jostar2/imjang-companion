"use client";

import { useEffect, useState } from "react";

import { fetchLatestReport, listProjects, type Project, type VisitReportPayload } from "../../lib/imjang-api";

export function ReportPreview() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProjectId, setSelectedProjectId] = useState("");
  const [report, setReport] = useState<VisitReportPayload | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoadingProjects, setIsLoadingProjects] = useState(true);
  const [isLoadingReport, setIsLoadingReport] = useState(false);

  useEffect(() => {
    async function loadProjects() {
      try {
        const projectData = [...(await listProjects())].sort((left, right) => left.name.localeCompare(right.name));
        setProjects(projectData);
        if (projectData.length > 0) {
          setSelectedProjectId(projectData[0].id);
        }
      } catch (loadError) {
        setError(loadError instanceof Error ? loadError.message : "Failed to load projects");
      } finally {
        setIsLoadingProjects(false);
      }
    }

    void loadProjects();
  }, []);

  useEffect(() => {
    if (!selectedProjectId) {
      setReport(null);
      return;
    }

    async function loadReport() {
      try {
        setIsLoadingReport(true);
        setError(null);
        const payload = await fetchLatestReport({ projectId: selectedProjectId });
        setReport(payload);
      } catch (loadError) {
        setError(loadError instanceof Error ? loadError.message : "Failed to load report data");
      } finally {
        setIsLoadingReport(false);
      }
    }

    void loadReport();
  }, [selectedProjectId]);

  const isLoading = isLoadingProjects || isLoadingReport;

  return (
    <section className="section-grid">
      {projects.length > 0 ? (
        <article className="card">
          <div className="section-header">
            <div>
              <h3>Report scope</h3>
              <p>The report reads the latest completed visit inside one project workspace.</p>
            </div>
            <span className="badge">{report?.visit_date ?? "No completed visit"}</span>
          </div>
          <label className="field">
            <span>Project</span>
            <select value={selectedProjectId} onChange={(event) => setSelectedProjectId(event.target.value)}>
              {projects.map((project) => (
                <option key={project.id} value={project.id}>
                  {project.name}
                </option>
              ))}
            </select>
          </label>
        </article>
      ) : null}
      {error ? <p className="status-text error-text">{error}</p> : null}
      {isLoading ? <p className="status-text">Loading report payload...</p> : null}
      <article className="card">
        <div className="section-header">
          <div>
            <h3>Visit report</h3>
            <p>{report ? `${report.project_name} · ${report.address}` : "No completed visit yet"}</p>
          </div>
          <span className="badge">{report?.total_score ?? "Draft"}</span>
        </div>
        <div className="stack-list">
          {!isLoading && projects.length === 0 ? (
            <div className="data-card">
              <p>Create a project, complete a visit, and then return to this page for the summary report.</p>
            </div>
          ) : null}
          {!report ? (
            <div className="data-card">
              <p>Complete at least one visit to generate a report preview.</p>
            </div>
          ) : null}
          {report?.sections.map((section) => (
            <div key={section.title} className="data-card">
              <div className="data-card-topline">
                <strong>{section.title}</strong>
              </div>
              <p>{section.body}</p>
            </div>
          ))}
        </div>
      </article>
    </section>
  );
}

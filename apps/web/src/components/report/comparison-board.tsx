"use client";

import { useEffect, useState } from "react";

import { fetchComparison, listProjects, type ComparisonPayload, type Project } from "../../lib/imjang-api";

export function ComparisonBoard() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [comparison, setComparison] = useState<ComparisonPayload | null>(null);
  const [selectedProjectId, setSelectedProjectId] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isLoadingProjects, setIsLoadingProjects] = useState(true);
  const [isLoadingComparison, setIsLoadingComparison] = useState(false);

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
      setComparison(null);
      return;
    }

    async function loadComparison() {
      try {
        setIsLoadingComparison(true);
        setError(null);
        const payload = await fetchComparison(selectedProjectId);
        setComparison(payload);
      } catch (loadError) {
        setError(loadError instanceof Error ? loadError.message : "Failed to load comparison data");
      } finally {
        setIsLoadingComparison(false);
      }
    }

    void loadComparison();
  }, [selectedProjectId]);

  const rows = comparison?.entries ?? [];
  const isLoading = isLoadingProjects || isLoadingComparison;

  return (
    <section className="section-grid">
      {projects.length > 0 ? (
        <article className="card">
          <div className="section-header">
            <div>
              <h3>Comparison scope</h3>
              <p>Comparison stays inside one project workspace so scores and red flags do not mix across deal theses.</p>
            </div>
            <span className="badge">{comparison?.property_count ?? rows.length} properties</span>
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
      {isLoading ? <p className="status-text">Loading comparison payload...</p> : null}
      {!isLoading && projects.length === 0 ? (
        <article className="card">
          <p>Create a project and add at least two properties before opening comparison.</p>
        </article>
      ) : null}
      {rows.map((property) => (
        <article key={property.property_id} className="card">
          <div className="section-header">
            <div>
              <h3>{property.address}</h3>
              <p>
                {property.listing_price_label}
                {property.visit_date ? ` · Visit ${property.visit_date}` : ""}
              </p>
            </div>
            <span className={`badge ${property.total_score != null ? "badge-success" : ""}`}>
              {property.total_score != null ? property.total_score.toFixed(1) : property.visit_status === "draft" ? "Draft" : "No visit"}
            </span>
          </div>
          <div className="comparison-columns">
            <div>
              <strong>Strengths</strong>
              <ul className="list">
                {property.strengths.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>
            <div>
              <strong>Red flags</strong>
              <ul className="list">
                {property.red_flags.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>
          </div>
        </article>
      ))}
    </section>
  );
}

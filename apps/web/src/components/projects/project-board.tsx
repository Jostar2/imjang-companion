"use client";

import { useEffect, useMemo, useState } from "react";

import { createProject, listProjects, listProperties, type Project } from "../../lib/imjang-api";

export function ProjectBoard() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [propertyCounts, setPropertyCounts] = useState<Record<string, number>>({});
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [draft, setDraft] = useState({
    name: "",
    region: "",
    budget: "",
    notes: ""
  });

  useEffect(() => {
    async function load() {
      try {
        const [projectData, propertyData] = await Promise.all([listProjects(), listProperties()]);
        setProjects(projectData);
        setPropertyCounts(
          propertyData.reduce<Record<string, number>>((counts, property) => {
            counts[property.project_id] = (counts[property.project_id] ?? 0) + 1;
            return counts;
          }, {})
        );
      } catch (loadError) {
        setError(loadError instanceof Error ? loadError.message : "Failed to load projects");
      } finally {
        setIsLoading(false);
      }
    }

    void load();
  }, []);

  const projectCount = useMemo(() => projects.length, [projects]);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!draft.name.trim() || !draft.region.trim() || !draft.budget.trim()) {
      return;
    }

    try {
      setIsSaving(true);
      setError(null);
      const created = await createProject({
        name: draft.name.trim(),
        region: draft.region.trim(),
        budget: draft.budget.trim(),
        notes: draft.notes.trim() || undefined
      });
      setProjects((current) => [created, ...current]);
      setPropertyCounts((current) => ({ ...current, [created.id]: 0 }));
      setDraft({ name: "", region: "", budget: "", notes: "" });
    } catch (saveError) {
      setError(saveError instanceof Error ? saveError.message : "Failed to save project");
    } finally {
      setIsSaving(false);
    }
  }

  return (
    <section className="section-grid two-column-grid">
      <article className="card form-card">
        <h3>Create Visit Project</h3>
        <p>Keep the project narrow enough that the visit comparison remains credible.</p>
        <form className="form-stack" onSubmit={handleSubmit}>
          <label className="field">
            <span>Project name</span>
            <input
              value={draft.name}
              onChange={(event) => setDraft((current) => ({ ...current, name: event.target.value }))}
              placeholder="Mapo apartment shortlist"
            />
          </label>
          <label className="field">
            <span>Target region</span>
            <input
              value={draft.region}
              onChange={(event) => setDraft((current) => ({ ...current, region: event.target.value }))}
              placeholder="Mapo / Seogyo"
            />
          </label>
          <label className="field">
            <span>Budget band</span>
            <input
              value={draft.budget}
              onChange={(event) => setDraft((current) => ({ ...current, budget: event.target.value }))}
              placeholder="700M-900M KRW"
            />
          </label>
          <label className="field">
            <span>Working note</span>
            <textarea
              value={draft.notes}
              onChange={(event) => setDraft((current) => ({ ...current, notes: event.target.value }))}
              placeholder="Parking, school district, elevator maintenance..."
              rows={4}
            />
          </label>
          <button type="submit" className="primary-button">
            {isSaving ? "Saving..." : "Add project"}
          </button>
        </form>
      </article>
      <article className="card">
        <div className="section-header">
          <div>
            <h3>Active projects</h3>
            <p>Project data now loads from the backend API and reflects actual saved routes.</p>
          </div>
          <span className="badge">{projectCount} routes</span>
        </div>
        {error ? <p className="status-text error-text">{error}</p> : null}
        {isLoading ? <p className="status-text">Loading projects...</p> : null}
        <div className="stack-list">
          {projects.map((project) => (
            <div key={project.id} className="data-card">
              <div className="data-card-topline">
                <strong>{project.name}</strong>
                <span>{propertyCounts[project.id] ?? 0} properties</span>
              </div>
              <div className="meta-grid">
                <span>{project.region ?? "Region TBD"}</span>
                <span>{project.budget ?? "Budget TBD"}</span>
              </div>
              <p>{project.notes || "No working note yet."}</p>
            </div>
          ))}
        </div>
      </article>
    </section>
  );
}

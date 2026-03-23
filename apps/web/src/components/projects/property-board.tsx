"use client";

import { useEffect, useMemo, useState } from "react";

import {
  createProperty,
  formatPrice,
  listProjects,
  listProperties,
  type Project,
  type Property
} from "../../lib/imjang-api";

export function PropertyBoard() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [properties, setProperties] = useState<Property[]>([]);
  const [selectedProjectId, setSelectedProjectId] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [draft, setDraft] = useState({
    projectId: "",
    address: "",
    propertyType: "",
    listingPrice: "",
    source: ""
  });

  useEffect(() => {
    async function load() {
      try {
        const [projectData, propertyData] = await Promise.all([listProjects(), listProperties()]);
        setProjects(projectData);
        setProperties(propertyData);
        const defaultProjectId = projectData[0]?.id ?? "";
        setSelectedProjectId(defaultProjectId);
        setDraft((current) => ({ ...current, projectId: defaultProjectId }));
      } catch (loadError) {
        setError(loadError instanceof Error ? loadError.message : "Failed to load properties");
      } finally {
        setIsLoading(false);
      }
    }

    void load();
  }, []);

  const filteredProperties = useMemo(
    () => properties.filter((property) => property.project_id === selectedProjectId),
    [properties, selectedProjectId]
  );

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!draft.projectId || !draft.address.trim() || !draft.propertyType.trim()) {
      return;
    }

    try {
      setIsSaving(true);
      setError(null);
      const created = await createProperty({
        project_id: draft.projectId,
        address: draft.address.trim(),
        property_type: draft.propertyType.trim(),
        listing_price: draft.listingPrice.trim() ? Number(draft.listingPrice.replace(/[^\d]/g, "")) : null,
        source: draft.source.trim() || undefined
      });
      setProperties((current) => [created, ...current]);
      setSelectedProjectId(draft.projectId);
      setDraft((current) => ({ ...current, address: "", propertyType: "", listingPrice: "", source: "" }));
    } catch (saveError) {
      setError(saveError instanceof Error ? saveError.message : "Failed to save property");
    } finally {
      setIsSaving(false);
    }
  }

  return (
    <section className="section-grid two-column-grid">
      <article className="card form-card">
        <h3>Register Candidate Property</h3>
        <p>Manual entry stays in scope so the visit workflow can move before listing integrations exist.</p>
        <form className="form-stack" onSubmit={handleSubmit}>
          <label className="field">
            <span>Project</span>
            <select
              value={draft.projectId}
              onChange={(event) => setDraft((current) => ({ ...current, projectId: event.target.value }))}
            >
              {projects.map((project) => (
                <option key={project.id} value={project.id}>
                  {project.name}
                </option>
              ))}
            </select>
          </label>
          <label className="field">
            <span>Address</span>
            <input
              value={draft.address}
              onChange={(event) => setDraft((current) => ({ ...current, address: event.target.value }))}
              placeholder="231 Donggyo-ro, Mapo-gu"
            />
          </label>
          <label className="field">
            <span>Property type</span>
            <input
              value={draft.propertyType}
              onChange={(event) => setDraft((current) => ({ ...current, propertyType: event.target.value }))}
              placeholder="Apartment"
            />
          </label>
          <label className="field">
            <span>Listing price</span>
            <input
              value={draft.listingPrice}
              onChange={(event) => setDraft((current) => ({ ...current, listingPrice: event.target.value }))}
              placeholder="820000000"
            />
          </label>
          <label className="field">
            <span>Source</span>
            <input
              value={draft.source}
              onChange={(event) => setDraft((current) => ({ ...current, source: event.target.value }))}
              placeholder="Broker note"
            />
          </label>
          <button type="submit" className="primary-button">
            {isSaving ? "Saving..." : "Add property"}
          </button>
        </form>
      </article>
      <article className="card">
        <div className="section-header">
          <div>
            <h3>Candidate property list</h3>
            <p>Filter by project to keep each visit route bounded and comparable.</p>
          </div>
          <select
            className="mini-select"
            value={selectedProjectId}
            onChange={(event) => setSelectedProjectId(event.target.value)}
          >
            {projects.map((project) => (
              <option key={project.id} value={project.id}>
                {project.name}
              </option>
            ))}
          </select>
        </div>
        {error ? <p className="status-text error-text">{error}</p> : null}
        {isLoading ? <p className="status-text">Loading properties...</p> : null}
        <div className="stack-list">
          {filteredProperties.map((property) => (
            <div key={property.id} className="data-card">
              <div className="data-card-topline">
                <strong>{property.address}</strong>
                <span>{property.property_type ?? "Type TBD"}</span>
              </div>
              <div className="meta-grid">
                <span>{formatPrice(property.listing_price)}</span>
                <span>{property.source ?? "Manual entry"}</span>
              </div>
            </div>
          ))}
        </div>
      </article>
    </section>
  );
}

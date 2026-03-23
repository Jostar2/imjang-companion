"use client";

import { useEffect, useMemo, useState } from "react";

import {
  fetchLatestReport,
  listProjects,
  listProperties,
  listVisits,
  type Project,
  type VisitReportPayload
} from "../../lib/imjang-api";

type ReportVisitOption = {
  visitId: string;
  propertyId: string;
  propertyAddress: string;
  visitDate: string;
  status: string;
};

export function ReportPreview() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProjectId, setSelectedProjectId] = useState("");
  const [visitOptions, setVisitOptions] = useState<ReportVisitOption[]>([]);
  const [selectedVisitId, setSelectedVisitId] = useState("");
  const [report, setReport] = useState<VisitReportPayload | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoadingProjects, setIsLoadingProjects] = useState(true);
  const [isLoadingVisits, setIsLoadingVisits] = useState(false);
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
      setVisitOptions([]);
      setSelectedVisitId("");
      setReport(null);
      return;
    }

    setSelectedVisitId("");
    setReport(null);

    async function loadVisits() {
      try {
        setIsLoadingVisits(true);
        setError(null);
        const properties = await listProperties(selectedProjectId);
        const visitGroups = await Promise.all(
          properties.map(async (property) => ({
            property,
            visits: await listVisits(property.id)
          }))
        );
        const completedVisits = visitGroups
          .flatMap(({ property, visits }) =>
            visits
              .filter((visit) => visit.status === "completed")
              .map((visit) => ({
                visitId: visit.id,
                propertyId: property.id,
                propertyAddress: property.address,
                visitDate: visit.visit_date,
                status: visit.status
              }))
          )
          .sort((left, right) => {
            const dateCompare = right.visitDate.localeCompare(left.visitDate);
            if (dateCompare !== 0) {
              return dateCompare;
            }
            return right.visitId.localeCompare(left.visitId);
          });
        setVisitOptions(completedVisits);
        setSelectedVisitId((current) =>
          completedVisits.some((visit) => visit.visitId === current) ? current : (completedVisits[0]?.visitId ?? "")
        );
      } catch (loadError) {
        setError(loadError instanceof Error ? loadError.message : "Failed to load completed visits");
      } finally {
        setIsLoadingVisits(false);
      }
    }

    void loadVisits();
  }, [selectedProjectId]);

  useEffect(() => {
    if (!selectedProjectId || !selectedVisitId) {
      setReport(null);
      return;
    }

    async function loadReport() {
      try {
        setIsLoadingReport(true);
        setError(null);
        const payload = await fetchLatestReport({ projectId: selectedProjectId, visitId: selectedVisitId });
        setReport(payload);
      } catch (loadError) {
        setError(loadError instanceof Error ? loadError.message : "Failed to load report data");
      } finally {
        setIsLoadingReport(false);
      }
    }

    void loadReport();
  }, [selectedProjectId, selectedVisitId]);

  const selectedVisit = useMemo(
    () => visitOptions.find((visit) => visit.visitId === selectedVisitId) ?? null,
    [selectedVisitId, visitOptions]
  );
  const isLoading = isLoadingProjects || isLoadingVisits || isLoadingReport;

  return (
    <section className="section-grid">
      {projects.length > 0 ? (
        <article className="card">
          <div className="section-header">
            <div>
              <h3>Report scope</h3>
              <p>The report is anchored to one explicit completed visit inside the selected project workspace.</p>
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
          <label className="field">
            <span>Completed visit</span>
            <select value={selectedVisitId} onChange={(event) => setSelectedVisitId(event.target.value)} disabled={visitOptions.length === 0}>
              {visitOptions.length === 0 ? <option value="">No completed visit yet</option> : null}
              {visitOptions.map((visit) => (
                <option key={visit.visitId} value={visit.visitId}>
                  {visit.visitDate} · {visit.propertyAddress}
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
            <p>
              {report
                ? `${report.project_name} · ${report.address}`
                : selectedVisit
                  ? `${selectedVisit.propertyAddress} · ${selectedVisit.visitDate}`
                  : "No completed visit yet"}
            </p>
          </div>
          <span className="badge">{report?.total_score ?? "Draft"}</span>
        </div>
        <div className="stack-list">
          {!isLoading && projects.length === 0 ? (
            <div className="data-card">
              <p>Create a project, complete a visit, and then return to this page for the summary report.</p>
            </div>
          ) : null}
          {!isLoading && projects.length > 0 && visitOptions.length === 0 ? (
            <div className="data-card">
              <p>Complete one visit in this project to unlock an explicit report selection.</p>
            </div>
          ) : null}
          {!report ? (
            <div className="data-card">
              <p>Select a completed visit to generate a report preview.</p>
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

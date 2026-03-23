"use client";

import { useEffect, useState } from "react";

import { fetchLatestReport, type VisitReportPayload } from "../../lib/imjang-api";

export function ReportPreview() {
  const [report, setReport] = useState<VisitReportPayload | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const payload = await fetchLatestReport();
        setReport(payload);
      } catch (loadError) {
        setError(loadError instanceof Error ? loadError.message : "Failed to load report data");
      } finally {
        setIsLoading(false);
      }
    }

    void load();
  }, []);

  return (
    <section className="section-grid">
      {error ? <p className="status-text error-text">{error}</p> : null}
      {isLoading ? <p className="status-text">Loading report payload...</p> : null}
      <article className="card">
        <div className="section-header">
          <div>
            <h3>Visit report</h3>
            <p>{report?.address ?? "No completed visit yet"}</p>
          </div>
          <span className="badge">{report?.total_score ?? "Draft"}</span>
        </div>
        <div className="stack-list">
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

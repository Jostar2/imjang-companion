"use client";

import { useEffect, useState } from "react";

import { fetchComparison, type ComparisonEntry } from "../../lib/imjang-api";

export function ComparisonBoard() {
  const [rows, setRows] = useState<ComparisonEntry[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const payload = await fetchComparison();
        setRows(payload.entries);
      } catch (loadError) {
        setError(loadError instanceof Error ? loadError.message : "Failed to load comparison data");
      } finally {
        setIsLoading(false);
      }
    }

    void load();
  }, []);

  return (
    <section className="section-grid">
      {error ? <p className="status-text error-text">{error}</p> : null}
      {isLoading ? <p className="status-text">Loading comparison payload...</p> : null}
      {rows.map((property) => (
        <article key={property.property_id} className="card">
          <div className="section-header">
            <div>
              <h3>{property.address}</h3>
              <p>{property.listing_price_label}</p>
            </div>
            <span className={`badge ${property.total_score != null ? "badge-success" : ""}`}>
              {property.total_score != null ? property.total_score.toFixed(1) : "Draft"}
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

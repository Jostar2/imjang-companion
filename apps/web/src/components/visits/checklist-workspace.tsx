"use client";

import { useEffect, useMemo, useRef, useState } from "react";

import {
  createVisit,
  listProperties,
  listVisits,
  type Property,
  type Visit,
  updateVisit,
  uploadAttachment
} from "../../lib/imjang-api";

type SectionState = {
  score: string;
  note: string;
};

type SectionKey = "property" | "building" | "neighborhood" | "redflags";

const sectionOrder: Array<{ key: SectionKey; title: string; required: boolean; prompt: string }> = [
  {
    key: "property",
    title: "Property condition",
    required: true,
    prompt: "Layout, sunlight, smell, plumbing, noise from inside the unit"
  },
  {
    key: "building",
    title: "Building and maintenance",
    required: true,
    prompt: "Elevator, hallway, parking, security, visible maintenance quality"
  },
  {
    key: "neighborhood",
    title: "Neighborhood",
    required: true,
    prompt: "Transit, slope, convenience, school and late-night noise"
  },
  {
    key: "redflags",
    title: "Red flags",
    required: false,
    prompt: "Anything that may kill the deal or require a second check"
  }
];

function createInitialSections(): Record<SectionKey, SectionState> {
  return {
    property: { score: "4", note: "Bright living room and acceptable kitchen layout." },
    building: { score: "", note: "" },
    neighborhood: { score: "", note: "" },
    redflags: { score: "", note: "Check for wall crack near bedroom window." }
  };
}

const initialDraftSections = createInitialSections();

function cloneInitialSections(): Record<SectionKey, SectionState> {
  return {
    property: { ...initialDraftSections.property },
    building: { ...initialDraftSections.building },
    neighborhood: { ...initialDraftSections.neighborhood },
    redflags: { ...initialDraftSections.redflags }
  };
}

function isInitialDraftState(
  sections: Record<SectionKey, SectionState>,
  recommendation: string,
  attachmentNames: string[]
): boolean {
  return (
    recommendation.trim() === "" &&
    attachmentNames.length === 0 &&
    JSON.stringify(sections) === JSON.stringify(initialDraftSections)
  );
}

const autosaveKey = "imjang-visit-draft";

type VisitDraft = {
  selectedPropertyId: string;
  sections: Record<SectionKey, SectionState>;
  recommendation: string;
  attachmentNames: string[];
};

type UploadRecovery = {
  visitId: string;
  propertyId: string;
  failedFiles: File[];
  failedMessages: string[];
};

export function ChecklistWorkspace() {
  const [properties, setProperties] = useState<Property[]>([]);
  const [selectedPropertyId, setSelectedPropertyId] = useState("");
  const [sections, setSections] = useState(cloneInitialSections);
  const [recommendation, setRecommendation] = useState("");
  const [attachments, setAttachments] = useState<File[]>([]);
  const [draftAttachmentNames, setDraftAttachmentNames] = useState<string[]>([]);
  const [lastVisit, setLastVisit] = useState<Visit | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [draftRestored, setDraftRestored] = useState(false);
  const [autosaveStatus, setAutosaveStatus] = useState<string | null>(null);
  const [uploadRecovery, setUploadRecovery] = useState<UploadRecovery | null>(null);
  const autosavePausedRef = useRef(false);

  useEffect(() => {
    async function load() {
      try {
        const propertyData = await listProperties();
        setProperties(propertyData);
        const defaultPropertyId = propertyData[0]?.id ?? "";
        let restoredPropertyId = defaultPropertyId;

        if (typeof window !== "undefined") {
          const rawDraft = window.localStorage.getItem(autosaveKey);
          if (rawDraft) {
            try {
              const draft = JSON.parse(rawDraft) as VisitDraft;
              setSections(draft.sections);
              setRecommendation(draft.recommendation);
              setDraftAttachmentNames(draft.attachmentNames);
              restoredPropertyId = draft.selectedPropertyId || defaultPropertyId;
              setDraftRestored(true);
            } catch {
              window.localStorage.removeItem(autosaveKey);
            }
          }
        }

        setSelectedPropertyId(restoredPropertyId);
      } catch (loadError) {
        setError(loadError instanceof Error ? loadError.message : "Failed to load visit data");
      }
    }

    void load();
  }, []);

  useEffect(() => {
    if (typeof window === "undefined" || properties.length === 0) {
      return;
    }

    if (autosavePausedRef.current) {
      autosavePausedRef.current = false;
      return;
    }

    const attachmentNames = attachments.length > 0 ? attachments.map((attachment) => attachment.name) : draftAttachmentNames;
    if (isInitialDraftState(sections, recommendation, attachmentNames)) {
      window.localStorage.removeItem(autosaveKey);
      setAutosaveStatus(null);
      return;
    }

    const draft: VisitDraft = {
      selectedPropertyId,
      sections,
      recommendation,
      attachmentNames
    };
    window.localStorage.setItem(autosaveKey, JSON.stringify(draft));
    setAutosaveStatus(`Draft autosaved at ${new Date().toLocaleTimeString()}`);
  }, [attachments, draftAttachmentNames, properties.length, recommendation, sections, selectedPropertyId]);

  const requiredCompletion = useMemo(
    () =>
      sectionOrder
        .filter((section) => section.required)
        .map((section) => ({
          key: section.key,
          title: section.title,
          done: Boolean(sections[section.key].score && sections[section.key].note.trim())
        })),
    [sections]
  );

  const canComplete = requiredCompletion.every((section) => section.done);
  const hasPendingUploadRecovery = uploadRecovery !== null && uploadRecovery.failedFiles.length > 0;
  const totalScore = useMemo(() => {
    const scores = requiredCompletion
      .map((section) => Number(sections[section.key].score))
      .filter((value) => Number.isFinite(value) && value > 0);

    if (scores.length === 0) {
      return null;
    }

    return (scores.reduce((sum, score) => sum + score, 0) / scores.length).toFixed(1);
  }, [requiredCompletion, sections]);

  function clearDraftStorage() {
    if (typeof window !== "undefined") {
      window.localStorage.removeItem(autosaveKey);
    }
  }

  function resetSavedVisitForm() {
    setSections(cloneInitialSections());
    setRecommendation("");
    setDraftRestored(false);
    setAutosaveStatus(null);
  }

  async function refreshVisit(propertyId: string, visitId: string, fallback: Visit): Promise<Visit> {
    const refreshedVisits = await listVisits(propertyId);
    return refreshedVisits.find((item) => item.id === visitId) ?? fallback;
  }

  async function uploadVisitAttachments(
    visitId: string,
    files: File[]
  ): Promise<{ failedFiles: File[]; failedMessages: string[] }> {
    const failedFiles: File[] = [];
    const failedMessages: string[] = [];

    for (const attachment of files) {
      try {
        await uploadAttachment(visitId, "visit-photo", attachment);
      } catch (uploadError) {
        failedFiles.push(attachment);
        failedMessages.push(
          `${attachment.name}: ${uploadError instanceof Error ? uploadError.message : "Upload failed"}`
        );
      }
    }

    return { failedFiles, failedMessages };
  }

  async function handleCompleteVisit() {
    if (!selectedPropertyId || !canComplete || hasPendingUploadRecovery) {
      return;
    }

    try {
      setIsSubmitting(true);
      setError(null);
      setStatusMessage(null);
      setUploadRecovery(null);
      const visit = await createVisit({
        property_id: selectedPropertyId,
        visit_date: new Date().toISOString().slice(0, 10)
      });

      let updatedVisit = await updateVisit(visit.id, {
        sections: [
          { section_name: "property", score: Number(sections.property.score), note: sections.property.note },
          { section_name: "building", score: Number(sections.building.score), note: sections.building.note },
          { section_name: "neighborhood", score: Number(sections.neighborhood.score), note: sections.neighborhood.note }
        ],
        red_flags: sections.redflags.note
          ? sections.redflags.note
              .split(/\r?\n/)
              .map((line) => line.trim())
              .filter(Boolean)
          : [],
        recommendation_notes: recommendation,
        mark_complete: true
      });

      const uploadResult = await uploadVisitAttachments(visit.id, attachments);
      if (attachments.length > 0) {
        updatedVisit = await refreshVisit(selectedPropertyId, visit.id, updatedVisit);
      }

      setLastVisit(updatedVisit);
      autosavePausedRef.current = true;
      clearDraftStorage();
      resetSavedVisitForm();

      if (uploadResult.failedFiles.length > 0) {
        setAttachments(uploadResult.failedFiles);
        setDraftAttachmentNames(uploadResult.failedFiles.map((file) => file.name));
        setUploadRecovery({
          visitId: visit.id,
          propertyId: selectedPropertyId,
          failedFiles: uploadResult.failedFiles,
          failedMessages: uploadResult.failedMessages
        });
        setStatusMessage(
          `Visit saved, but ${uploadResult.failedFiles.length} attachment upload failed. Retry the remaining files below.`
        );
        return;
      }

      setAttachments([]);
      setDraftAttachmentNames([]);
      setAutosaveStatus(null);
      setStatusMessage("Visit saved and all attachments uploaded.");
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "Failed to complete visit");
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleRetryUploads() {
    if (!uploadRecovery) {
      return;
    }

    try {
      setIsSubmitting(true);
      setError(null);
      setStatusMessage(null);

      const uploadResult = await uploadVisitAttachments(uploadRecovery.visitId, uploadRecovery.failedFiles);
      const fallbackVisit = lastVisit;
      if (fallbackVisit) {
        const refreshedVisit = await refreshVisit(uploadRecovery.propertyId, uploadRecovery.visitId, fallbackVisit);
        setLastVisit(refreshedVisit);
      }

      if (uploadResult.failedFiles.length > 0) {
        setAttachments(uploadResult.failedFiles);
        setDraftAttachmentNames(uploadResult.failedFiles.map((file) => file.name));
        setUploadRecovery({
          ...uploadRecovery,
          failedFiles: uploadResult.failedFiles,
          failedMessages: uploadResult.failedMessages
        });
        setStatusMessage(
          `Retry completed, but ${uploadResult.failedFiles.length} attachment upload still failed.`
        );
        return;
      }

      setAttachments([]);
      setDraftAttachmentNames([]);
      setUploadRecovery(null);
      clearDraftStorage();
      autosavePausedRef.current = true;
      setAutosaveStatus(null);
      setStatusMessage("Remaining attachments uploaded successfully.");
    } catch (retryError) {
      setError(retryError instanceof Error ? retryError.message : "Failed to retry attachment uploads");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <section className="section-grid two-column-grid">
      <article className="card">
        <div className="section-header">
          <div>
            <h3>Visit completion gate</h3>
            <p>The visit cannot close until the required sections are scored and described.</p>
          </div>
          <span className={`badge ${canComplete ? "badge-success" : "badge-warning"}`}>
            {canComplete ? "Ready to complete" : "Missing required sections"}
          </span>
        </div>
        <div className="stack-list">
          {requiredCompletion.map((section) => (
            <div key={section.key} className="data-card">
              <div className="data-card-topline">
                <strong>{section.title}</strong>
                <span>{section.done ? "Complete" : "Incomplete"}</span>
              </div>
            </div>
          ))}
        </div>
        <div className="metric-strip">
          <div className="metric-card">
            <span>Required sections</span>
            <strong>{requiredCompletion.filter((section) => section.done).length}/3</strong>
          </div>
          <div className="metric-card">
            <span>Average score</span>
            <strong>{totalScore ?? "-"}</strong>
          </div>
        </div>
        {draftRestored ? (
          <div className="status-panel">
            <strong>Draft restored</strong>
            <p>Your local visit draft was restored from browser storage.</p>
          </div>
        ) : null}
        {lastVisit ? (
          <div className="status-panel">
            <strong>Latest saved visit</strong>
            <p>
              Status: {lastVisit.status} | Missing sections: {lastVisit.missing_sections.length} | Attachments:{" "}
              {lastVisit.attachments.length}
            </p>
          </div>
        ) : null}
        {uploadRecovery ? (
          <div className="status-panel warning-panel">
            <strong>Attachment uploads pending</strong>
            <p>Visit data is already saved. Retry the remaining files before leaving this page.</p>
            <div className="attachment-list">
              {uploadRecovery.failedFiles.map((file) => (
                <span key={file.name} className="chip">
                  {file.name}
                </span>
              ))}
            </div>
            <ul className="list">
              {uploadRecovery.failedMessages.map((message) => (
                <li key={message}>{message}</li>
              ))}
            </ul>
            <button
              type="button"
              className="secondary-button"
              disabled={isSubmitting}
              onClick={() => void handleRetryUploads()}
            >
              {isSubmitting ? "Retrying uploads..." : "Retry failed uploads"}
            </button>
          </div>
        ) : null}
      </article>
      <article className="card form-card">
        <h3>Visit checklist shell</h3>
        <p>This flow now persists through the backend API and keeps a local autosave draft for field use.</p>
        <div className="form-stack">
          <label className="field">
            <span>Property</span>
            <select value={selectedPropertyId} onChange={(event) => setSelectedPropertyId(event.target.value)}>
              {properties.map((property) => (
                <option key={property.id} value={property.id}>
                  {property.address}
                </option>
              ))}
            </select>
          </label>
          {sectionOrder.map((section) => (
            <div key={section.key} className="visit-section">
              <div className="visit-section-header">
                <strong>{section.title}</strong>
                <span>{section.required ? "Required" : "Optional"}</span>
              </div>
              <p>{section.prompt}</p>
              <div className="score-grid">
                <label className="field">
                  <span>Score</span>
                  <select
                    value={sections[section.key].score}
                    onChange={(event) =>
                      setSections((current) => ({
                        ...current,
                        [section.key]: { ...current[section.key], score: event.target.value }
                      }))
                    }
                  >
                    <option value="">Choose</option>
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3">3</option>
                    <option value="4">4</option>
                    <option value="5">5</option>
                  </select>
                </label>
                <label className="field wide-field">
                  <span>Note</span>
                  <textarea
                    rows={3}
                    value={sections[section.key].note}
                    onChange={(event) =>
                      setSections((current) => ({
                        ...current,
                        [section.key]: { ...current[section.key], note: event.target.value }
                      }))
                    }
                    placeholder="Record the strongest signal from the field visit."
                  />
                </label>
              </div>
            </div>
          ))}
          <label className="field">
            <span>Recommendation note</span>
            <textarea
              rows={4}
              value={recommendation}
              onChange={(event) => setRecommendation(event.target.value)}
              placeholder="Why should this property advance or be rejected?"
            />
          </label>
          <label className="field">
            <span>Visit photos</span>
            <input
              type="file"
              multiple
              onChange={(event) => {
                const files = Array.from(event.target.files ?? []);
                setAttachments(files);
                setDraftAttachmentNames(files.map((file) => file.name));
              }}
            />
          </label>
          {draftAttachmentNames.length > 0 ? (
            <div className="attachment-list">
              {draftAttachmentNames.map((attachment) => (
                <span key={attachment} className="chip">
                  {attachment}
                </span>
              ))}
            </div>
          ) : null}
          {draftAttachmentNames.length > 0 && attachments.length === 0 ? (
            <p className="status-text">
              Draft restored file names. Re-select files before final submission because browsers do not restore file binaries.
            </p>
          ) : null}
          {autosaveStatus ? <p className="status-text">{autosaveStatus}</p> : null}
          {statusMessage ? <p className="status-text">{statusMessage}</p> : null}
          {error ? <p className="status-text error-text">{error}</p> : null}
          <button
            type="button"
            className="primary-button"
            disabled={!canComplete || !selectedPropertyId || isSubmitting || hasPendingUploadRecovery}
            onClick={() => void handleCompleteVisit()}
          >
            {isSubmitting ? "Saving visit..." : hasPendingUploadRecovery ? "Visit saved; retry uploads above" : "Mark visit complete"}
          </button>
        </div>
      </article>
    </section>
  );
}

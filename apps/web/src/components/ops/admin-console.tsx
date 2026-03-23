"use client";

import { useEffect, useState } from "react";

import {
  acknowledgeLaunchOsAlert,
  acknowledgeLaunchOsBlocker,
  clearSession,
  fetchLaunchOsAttempts,
  fetchLaunchOsAlerts,
  fetchLaunchOsBlockers,
  fetchLaunchOsEvents,
  fetchLaunchOsQueue,
  fetchLaunchOsSynthesis,
  fetchLaunchOsStatus,
  fetchOpsSummary,
  fetchReleaseReadiness,
  getStoredSession,
  me,
  pauseLaunchOs,
  resumeLaunchOs,
  retryLaunchOsQueueItem,
  type LaunchOsAttempt,
  type LaunchOsAlert,
  type LaunchOsBlocker,
  type LaunchOsEvent,
  type LaunchOsQueueItem,
  type LaunchOsStatus,
  type LaunchOsSynthesis,
  type Me,
  type OpsSummary,
  type ReleaseReadiness
} from "../../lib/imjang-api";

export function AdminConsole() {
  const [currentUser, setCurrentUser] = useState<Me | null>(null);
  const [opsSummary, setOpsSummary] = useState<OpsSummary | null>(null);
  const [readiness, setReadiness] = useState<ReleaseReadiness | null>(null);
  const [launchOsStatus, setLaunchOsStatus] = useState<LaunchOsStatus | null>(null);
  const [queueItems, setQueueItems] = useState<LaunchOsQueueItem[]>([]);
  const [events, setEvents] = useState<LaunchOsEvent[]>([]);
  const [attempts, setAttempts] = useState<LaunchOsAttempt[]>([]);
  const [alerts, setAlerts] = useState<LaunchOsAlert[]>([]);
  const [blockers, setBlockers] = useState<LaunchOsBlocker[]>([]);
  const [synthesis, setSynthesis] = useState<LaunchOsSynthesis | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [actionState, setActionState] = useState<string | null>(null);

  async function loadConsole(): Promise<void> {
    const session = getStoredSession();
    if (!session) {
      setError("No active session. Sign in from the home page first.");
      setIsLoading(false);
      return;
    }

    try {
      const user = await me();
      setCurrentUser(user);
      if (user.role !== "admin") {
        setError("Admin role required for ops access.");
        return;
      }

      const [nextReadiness, nextOpsSummary, nextLaunchOsStatus, nextQueueItems, nextEvents, nextAttempts, nextAlerts, nextBlockers, nextSynthesis] = await Promise.all([
        fetchReleaseReadiness(),
        fetchOpsSummary(),
        fetchLaunchOsStatus(),
        fetchLaunchOsQueue(),
        fetchLaunchOsEvents(),
        fetchLaunchOsAttempts(),
        fetchLaunchOsAlerts(),
        fetchLaunchOsBlockers(),
        fetchLaunchOsSynthesis()
      ]);
      setReadiness(nextReadiness);
      setOpsSummary(nextOpsSummary);
      setLaunchOsStatus(nextLaunchOsStatus);
      setQueueItems(nextQueueItems);
      setEvents(nextEvents);
      setAttempts(nextAttempts);
      setAlerts(nextAlerts);
      setBlockers(nextBlockers);
      setSynthesis(nextSynthesis);
      setError(null);
    } catch (loadError) {
      clearSession();
      setError(loadError instanceof Error ? loadError.message : "Failed to load ops console");
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    void loadConsole();
  }, []);

  async function runAction(actionLabel: string, action: () => Promise<unknown>) {
    setActionState(actionLabel);
    try {
      await action();
      await loadConsole();
    } catch (actionError) {
      setError(actionError instanceof Error ? actionError.message : `Failed to ${actionLabel}`);
    } finally {
      setActionState(null);
    }
  }

  if (isLoading) {
    return <p className="status-text">Loading admin console...</p>;
  }

  if (error) {
    return <p className="status-text error-text">{error}</p>;
  }

  if (!currentUser || currentUser.role !== "admin" || !opsSummary || !readiness || !launchOsStatus || !synthesis) {
    return <p className="status-text">Admin console unavailable.</p>;
  }

  return (
    <section className="section-grid">
      <article className="card">
        <h3>Launch OS runtime</h3>
        <div className="stack-list">
          <div className="data-card">
            <div className="data-card-topline">
              <strong>Runner</strong>
              <span>{launchOsStatus.runner_state}</span>
            </div>
            <p>
              Project {launchOsStatus.active_project_slug} / Run {launchOsStatus.active_run_id}
            </p>
            <p>Current phase: {launchOsStatus.current_phase}</p>
            <p>Open blockers: {launchOsStatus.open_blocker_count}</p>
            <p>Open alerts: {launchOsStatus.open_alert_count}</p>
          </div>
          <div className="data-card">
            <div className="data-card-topline">
              <strong>Current queue item</strong>
              <span>{launchOsStatus.current_queue_item?.owner_agent ?? "idle"}</span>
            </div>
            <p>{launchOsStatus.current_queue_item?.label ?? "No leased work item"}</p>
            <p>Last error: {launchOsStatus.last_error ?? "none"}</p>
          </div>
          <div className="data-card">
            <div className="data-card-topline">
              <strong>Queue counts</strong>
              <span>{Object.values(launchOsStatus.queue_counts).reduce((sum, value) => sum + value, 0)}</span>
            </div>
            <ul className="list">
              {Object.entries(launchOsStatus.queue_counts).map(([key, value]) => (
                <li key={key}>
                  {key}: {value}
                </li>
              ))}
            </ul>
            <p>Runtime completed: {launchOsStatus.runtime_completed.length}</p>
          </div>
          <div className="data-card">
            <div className="data-card-topline">
              <strong>Controls</strong>
              <span>{actionState ?? "ready"}</span>
            </div>
            <div className="section-grid two-column-grid">
              <button
                type="button"
                className="button"
                disabled={actionState !== null}
                onClick={() => void runAction("pause runner", pauseLaunchOs)}
              >
                Pause
              </button>
              <button
                type="button"
                className="button secondary"
                disabled={actionState !== null}
                onClick={() => void runAction("resume runner", resumeLaunchOs)}
              >
                Resume
              </button>
            </div>
          </div>
        </div>
      </article>

      <article className="card">
        <h3>Launch OS alerts</h3>
        <div className="stack-list">
          {alerts.length === 0 ? <p className="status-text">No open alerts.</p> : null}
          {alerts.map((alert) => (
            <div key={alert.id} className="data-card">
              <div className="data-card-topline">
                <strong>{alert.title}</strong>
                <span>
                  {alert.severity} / {alert.status}
                </span>
              </div>
              <p>{alert.message}</p>
              <button
                type="button"
                className="button secondary"
                disabled={actionState !== null}
                onClick={() => void runAction(`ack alert ${alert.id}`, () => acknowledgeLaunchOsAlert(alert.id))}
              >
                Ack alert
              </button>
            </div>
          ))}
        </div>
      </article>

      <article className="card">
        <h3>Launch OS blockers</h3>
        <div className="stack-list">
          {blockers.length === 0 ? <p className="status-text">No active blockers.</p> : null}
          {blockers.map((blocker) => (
            <div key={blocker.id} className="data-card">
              <div className="data-card-topline">
                <strong>{blocker.title}</strong>
                <span>{blocker.status}</span>
              </div>
              <p>{blocker.reason}</p>
              <button
                type="button"
                className="button secondary"
                disabled={actionState !== null}
                onClick={() => void runAction(`ack blocker ${blocker.id}`, () => acknowledgeLaunchOsBlocker(blocker.id))}
              >
                Ack blocker
              </button>
            </div>
          ))}
        </div>
      </article>

      <article className="card">
        <h3>Launch OS queue</h3>
        <div className="stack-list">
          {queueItems.length === 0 ? <p className="status-text">No queued work.</p> : null}
          {queueItems.map((item) => (
            <div key={item.id} className="data-card">
              <div className="data-card-topline">
                <strong>{item.label}</strong>
                <span>
                  {item.owner_agent} / {item.status}
                </span>
              </div>
              <p>Attempts: {item.attempt_count}</p>
              <p>Source: {item.source}</p>
              <p>Available at: {item.available_at_utc ?? "now"}</p>
              <button
                type="button"
                className="button secondary"
                disabled={actionState !== null || item.status !== "failed"}
                onClick={() => void runAction(`retry queue item ${item.id}`, () => retryLaunchOsQueueItem(item.id))}
              >
                Retry
              </button>
            </div>
          ))}
        </div>
      </article>

      <article className="card">
        <h3>Recent attempts</h3>
        <div className="stack-list">
          {attempts.length === 0 ? <p className="status-text">No recorded attempts.</p> : null}
          {attempts.map((attempt) => (
            <div key={attempt.attempt_id} className="data-card">
              <div className="data-card-topline">
                <strong>{attempt.label}</strong>
                <span>
                  {attempt.agent_role} / {attempt.result_status}
                </span>
              </div>
              <p>Exit code: {attempt.exit_code ?? "n/a"}</p>
              <p>Scope completed: {attempt.structured_summary.scope_completed || "not reported"}</p>
              <p>Tests: {attempt.structured_summary.test_status || "not reported"}</p>
              <p>Recommended next owner: {attempt.structured_summary.recommended_next_owner || "none"}</p>
              <p>Blockers: {attempt.structured_summary.blockers.length ? attempt.structured_summary.blockers.join(", ") : "none"}</p>
              <p>Residual risks: {attempt.structured_summary.residual_risks.length ? attempt.structured_summary.residual_risks.join(", ") : "none"}</p>
              <p>{attempt.summary ?? "No summary recorded."}</p>
            </div>
          ))}
        </div>
      </article>

      <article className="card">
        <h3>Synthesized queue plan</h3>
        <div className="stack-list">
          {synthesis.queue_candidates.length === 0 ? <p className="status-text">No synthesized candidates.</p> : null}
          {synthesis.queue_candidates.map((candidate) => (
            <div key={candidate.queue_key} className="data-card">
              <div className="data-card-topline">
                <strong>{candidate.label}</strong>
                <span>
                  {candidate.owner_agent} / {candidate.source}
                </span>
              </div>
              <p>Priority: {candidate.priority}</p>
            </div>
          ))}
        </div>
      </article>

      <article className="card">
        <h3>Release readiness</h3>
        <div className="stack-list">
          <div className="data-card">
            <div className="data-card-topline">
              <strong>Status</strong>
              <span>{readiness.run_status}</span>
            </div>
            <p>Current phase: {readiness.current_phase}</p>
            <p>Blocked: {readiness.blocked.length ? readiness.blocked.join(", ") : "none"}</p>
          </div>
          <div className="data-card">
            <div className="data-card-topline">
              <strong>Next tasks</strong>
              <span>{readiness.next_tasks.length}</span>
            </div>
            <ul className="list">
              {readiness.next_tasks.map((task) => (
                <li key={task}>{task}</li>
              ))}
            </ul>
          </div>
        </div>
      </article>

      <article className="card">
        <h3>Repository footprint</h3>
        <div className="section-grid two-column-grid">
          <div className="data-card">
            <strong>{opsSummary.total_users}</strong>
            <p>Users</p>
          </div>
          <div className="data-card">
            <strong>{opsSummary.total_projects}</strong>
            <p>Projects</p>
          </div>
          <div className="data-card">
            <strong>{opsSummary.total_properties}</strong>
            <p>Properties</p>
          </div>
          <div className="data-card">
            <strong>{opsSummary.total_visits}</strong>
            <p>Visits</p>
          </div>
          <div className="data-card">
            <strong>{opsSummary.total_completed_visits}</strong>
            <p>Completed visits</p>
          </div>
          <div className="data-card">
            <strong>{opsSummary.total_attachments}</strong>
            <p>Attachments</p>
          </div>
        </div>
      </article>

      <article className="card">
        <h3>Recent events</h3>
        <div className="stack-list">
          {events.length === 0 ? <p className="status-text">No recorded runtime events.</p> : null}
          {events.map((event) => (
            <div key={event.id} className="data-card">
              <div className="data-card-topline">
                <strong>{event.kind}</strong>
                <span>{event.created_at_utc}</span>
              </div>
              <p>{event.message}</p>
              {typeof event.metadata.recommended_next_owner === "string" && event.metadata.recommended_next_owner ? (
                <p>Next owner: {event.metadata.recommended_next_owner}</p>
              ) : null}
              {Array.isArray(event.metadata.blockers) && event.metadata.blockers.length > 0 ? (
                <p>
                  Reported blockers:{" "}
                  {event.metadata.blockers.filter((item): item is string => typeof item === "string").join(", ")}
                </p>
              ) : null}
              {Array.isArray(event.metadata.residual_risks) && event.metadata.residual_risks.length > 0 ? (
                <p>
                  Residual risks:{" "}
                  {event.metadata.residual_risks.filter((item): item is string => typeof item === "string").join(", ")}
                </p>
              ) : null}
            </div>
          ))}
        </div>
      </article>
    </section>
  );
}

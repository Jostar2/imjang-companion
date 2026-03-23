export type Project = {
  id: string;
  name: string;
  region: string | null;
  budget: string | null;
  notes: string | null;
};

export type Property = {
  id: string;
  project_id: string;
  address: string;
  listing_price: number | null;
  property_type: string | null;
  source: string | null;
};

export type Attachment = {
  id: string;
  visit_id: string;
  filename: string;
  content_type: string;
  category: string;
  storage_backend: string;
  storage_key: string;
  size_bytes: number;
};

export type Visit = {
  id: string;
  property_id: string;
  visit_date: string;
  status: string;
  completed_sections: string[];
  missing_sections: string[];
  total_score: number | null;
  red_flags: string[];
  recommendation_notes: string | null;
  attachments: Attachment[];
};

export type ComparisonEntry = {
  property_id: string;
  address: string;
  listing_price_label: string;
  total_score: number | null;
  strengths: string[];
  red_flags: string[];
};

export type ComparisonPayload = {
  project_count: number;
  entries: ComparisonEntry[];
};

export type ReportSection = {
  title: string;
  body: string;
};

export type VisitReportPayload = {
  property_id: string;
  address: string;
  total_score: number | null;
  sections: ReportSection[];
};

export type SessionInfo = {
  token: string;
  user_id: string;
  email: string;
  display_name: string;
  role: "buyer" | "admin";
};

export type Me = {
  user_id: string;
  email: string;
  display_name: string;
  role: "buyer" | "admin";
};

export type ReleaseReadiness = {
  run_status: string;
  current_phase: string;
  next_tasks: string[];
  blocked: string[];
};

export type OpsUserSummary = {
  user_id: string;
  email: string;
  display_name: string;
  role: string;
  project_count: number;
  property_count: number;
  visit_count: number;
};

export type OpsSummary = {
  total_users: number;
  total_projects: number;
  total_properties: number;
  total_visits: number;
  total_completed_visits: number;
  total_attachments: number;
  users: OpsUserSummary[];
};

export type LaunchOsQueueItem = {
  id: number;
  project_slug: string;
  run_id: string;
  queue_key: string;
  label: string;
  owner_agent: string;
  status: string;
  priority: number;
  payload: Record<string, unknown>;
  source: string;
  attempt_count: number;
  last_error: string | null;
  created_at_utc: string;
  updated_at_utc: string;
  available_at_utc: string | null;
  leased_at_utc: string | null;
  finished_at_utc: string | null;
};

export type LaunchOsBlocker = {
  id: number;
  project_slug: string;
  run_id: string;
  blocker_key: string;
  title: string;
  reason: string;
  source: string;
  status: string;
  metadata: Record<string, unknown>;
  created_at_utc: string;
  updated_at_utc: string;
  resolved_at_utc: string | null;
};

export type LaunchOsAlert = {
  id: number;
  project_slug: string;
  queue_item_id: number | null;
  blocker_id: number | null;
  severity: string;
  status: string;
  title: string;
  message: string;
  source: string;
  metadata: Record<string, unknown>;
  created_at_utc: string;
  updated_at_utc: string;
  resolved_at_utc: string | null;
};

export type LaunchOsEvent = {
  id: number;
  project_slug: string;
  queue_item_id: number | null;
  blocker_id: number | null;
  kind: string;
  message: string;
  metadata: Record<string, unknown>;
  created_at_utc: string;
};

export type LaunchOsAttemptSummary = {
  scope_completed: string;
  files_changed: string[];
  commands_run: string[];
  test_status: string;
  residual_risks: string[];
  blockers: string[];
  recommended_next_owner: string;
};

export type LaunchOsAttempt = {
  attempt_id: number;
  queue_item_id: number;
  label: string;
  agent_role: string;
  result_status: string;
  exit_code: number | null;
  summary: string | null;
  structured_summary: LaunchOsAttemptSummary;
  started_at_utc: string;
  finished_at_utc: string | null;
};

export type LaunchOsStatus = {
  active_project_slug: string;
  active_run_id: string;
  run_status: string;
  current_phase: string;
  next_tasks: string[];
  runtime_completed: string[];
  effective_completed: string[];
  run_blocked: string[];
  runner_state: string;
  current_queue_item: LaunchOsQueueItem | null;
  queue_counts: Record<string, number>;
  open_blocker_count: number;
  blockers: LaunchOsBlocker[];
  open_alert_count: number;
  alerts: LaunchOsAlert[];
  human_gates: string[];
  last_heartbeat_utc: string | null;
  last_error: string | null;
};

export type LaunchOsSynthesisCandidate = {
  queue_key: string;
  label: string;
  owner_agent: string;
  source: string;
  priority: number;
  payload: Record<string, unknown>;
};

export type LaunchOsSynthesis = {
  active_project_slug: string;
  active_run_id: string;
  run_status: string;
  current_phase: string;
  completed: string[];
  next_tasks: string[];
  queue_candidates: LaunchOsSynthesisCandidate[];
};

export type LaunchOsControlResponse = {
  ok: boolean;
  runner_state: string;
  message: string;
};

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";
const sessionStorageKey = "imjang-session";

function readStoredSession(): SessionInfo | null {
  if (typeof window === "undefined") {
    return null;
  }

  const raw = window.localStorage.getItem(sessionStorageKey);
  if (!raw) {
    return null;
  }

  try {
    return JSON.parse(raw) as SessionInfo;
  } catch {
    window.localStorage.removeItem(sessionStorageKey);
    return null;
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const session = readStoredSession();
  const response = await fetch(`${apiBaseUrl}${path}`, {
    ...init,
    headers: {
      ...(init?.body instanceof FormData ? {} : { "Content-Type": "application/json" }),
      ...(session ? { Authorization: `Bearer ${session.token}` } : {}),
      ...init?.headers
    },
    cache: "no-store"
  });

  if (!response.ok) {
    const rawDetail = await response.text();
    let detail = rawDetail;
    try {
      const payload = JSON.parse(rawDetail) as { detail?: string };
      if (typeof payload.detail === "string" && payload.detail.trim()) {
        detail = payload.detail;
      }
    } catch {
      // Ignore parsing errors and fall back to the raw response body.
    }
    throw new Error(detail || `Request failed: ${response.status}`);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}

export function formatPrice(value: number | null): string {
  if (value == null) {
    return "TBD";
  }

  return `${new Intl.NumberFormat("en-US").format(value)} KRW`;
}

export function storeSession(session: SessionInfo): void {
  if (typeof window !== "undefined") {
    window.localStorage.setItem(sessionStorageKey, JSON.stringify(session));
  }
}

export function clearSession(): void {
  if (typeof window !== "undefined") {
    window.localStorage.removeItem(sessionStorageKey);
  }
}

export function getStoredSession(): SessionInfo | null {
  return readStoredSession();
}

export function login(payload: { email: string; display_name: string; role: "buyer" | "admin" }): Promise<SessionInfo> {
  return request<SessionInfo>("/auth/login", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function me(): Promise<Me> {
  return request<Me>("/auth/me");
}

export function listProjects(): Promise<Project[]> {
  return request<Project[]>("/projects");
}

export function createProject(payload: {
  name: string;
  region?: string;
  budget?: string;
  notes?: string;
}): Promise<Project> {
  return request<Project>("/projects", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function listProperties(projectId?: string): Promise<Property[]> {
  const query = projectId ? `?project_id=${encodeURIComponent(projectId)}` : "";
  return request<Property[]>(`/properties${query}`);
}

export function createProperty(payload: {
  project_id: string;
  address: string;
  listing_price?: number | null;
  property_type?: string;
  source?: string;
}): Promise<Property> {
  return request<Property>("/properties", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function listVisits(propertyId?: string): Promise<Visit[]> {
  const query = propertyId ? `?property_id=${encodeURIComponent(propertyId)}` : "";
  return request<Visit[]>(`/visits${query}`);
}

export function fetchComparison(): Promise<ComparisonPayload> {
  return request<ComparisonPayload>("/reports/comparison");
}

export function fetchLatestReport(): Promise<VisitReportPayload> {
  return request<VisitReportPayload>("/reports/latest");
}

export function fetchReleaseReadiness(): Promise<ReleaseReadiness> {
  return request<ReleaseReadiness>("/ops/release-readiness");
}

export function fetchOpsSummary(): Promise<OpsSummary> {
  return request<OpsSummary>("/ops/summary");
}

export function fetchLaunchOsStatus(): Promise<LaunchOsStatus> {
  return request<LaunchOsStatus>("/ops/launch-os/status");
}

export function fetchLaunchOsQueue(): Promise<LaunchOsQueueItem[]> {
  return request<LaunchOsQueueItem[]>("/ops/launch-os/queue");
}

export function fetchLaunchOsEvents(): Promise<LaunchOsEvent[]> {
  return request<LaunchOsEvent[]>("/ops/launch-os/events");
}

export function fetchLaunchOsAlerts(): Promise<LaunchOsAlert[]> {
  return request<LaunchOsAlert[]>("/ops/launch-os/alerts");
}

export function fetchLaunchOsAttempts(): Promise<LaunchOsAttempt[]> {
  return request<LaunchOsAttempt[]>("/ops/launch-os/attempts");
}

export function fetchLaunchOsBlockers(): Promise<LaunchOsBlocker[]> {
  return request<LaunchOsBlocker[]>("/ops/launch-os/blockers");
}

export function fetchLaunchOsSynthesis(): Promise<LaunchOsSynthesis> {
  return request<LaunchOsSynthesis>("/ops/launch-os/synthesis");
}

export function pauseLaunchOs(): Promise<LaunchOsControlResponse> {
  return request<LaunchOsControlResponse>("/ops/launch-os/pause", {
    method: "POST"
  });
}

export function resumeLaunchOs(): Promise<LaunchOsControlResponse> {
  return request<LaunchOsControlResponse>("/ops/launch-os/resume", {
    method: "POST"
  });
}

export function retryLaunchOsQueueItem(queueItemId: number): Promise<LaunchOsControlResponse> {
  return request<LaunchOsControlResponse>(`/ops/launch-os/queue/${queueItemId}/retry`, {
    method: "POST"
  });
}

export function acknowledgeLaunchOsBlocker(blockerId: number): Promise<LaunchOsControlResponse> {
  return request<LaunchOsControlResponse>(`/ops/launch-os/blockers/${blockerId}/ack`, {
    method: "POST"
  });
}

export function acknowledgeLaunchOsAlert(alertId: number): Promise<LaunchOsControlResponse> {
  return request<LaunchOsControlResponse>(`/ops/launch-os/alerts/${alertId}/ack`, {
    method: "POST"
  });
}

export function createVisit(payload: { property_id: string; visit_date: string }): Promise<Visit> {
  return request<Visit>("/visits", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function updateVisit(
  visitId: string,
  payload: {
    sections: Array<{ section_name: string; score: number; note: string }>;
    red_flags: string[];
    recommendation_notes: string;
    mark_complete: boolean;
  }
): Promise<Visit> {
  return request<Visit>(`/visits/${visitId}`, {
    method: "PATCH",
    body: JSON.stringify(payload)
  });
}

export function uploadAttachment(visitId: string, category: string, file: File): Promise<Attachment> {
  const formData = new FormData();
  formData.append("category", category);
  formData.append("file", file);

  return request<Attachment>(`/visits/${visitId}/attachments/upload`, {
    method: "POST",
    body: formData
  });
}

"use client";

import { useEffect, useState } from "react";

import { clearSession, getStoredSession, login, me, storeSession, type Me } from "../../lib/imjang-api";

export function AuthPanel() {
  const [currentUser, setCurrentUser] = useState<Me | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [draft, setDraft] = useState({
    email: "buyer@example.com",
    displayName: "Field Buyer",
    role: "buyer" as "buyer" | "admin"
  });

  useEffect(() => {
    async function loadCurrentUser() {
      const session = getStoredSession();
      if (!session) {
        setIsLoading(false);
        return;
      }

      try {
        const user = await me();
        setCurrentUser(user);
      } catch {
        clearSession();
      } finally {
        setIsLoading(false);
      }
    }

    void loadCurrentUser();
  }, []);

  async function handleLogin(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!draft.email.trim() || !draft.displayName.trim()) {
      return;
    }

    try {
      setIsSubmitting(true);
      setError(null);
      const session = await login({
        email: draft.email.trim(),
        display_name: draft.displayName.trim(),
        role: draft.role
      });
      storeSession(session);
      setCurrentUser({
        user_id: session.user_id,
        email: session.email,
        display_name: session.display_name,
        role: session.role
      });
    } catch (loginError) {
      setError(loginError instanceof Error ? loginError.message : "Failed to sign in");
    } finally {
      setIsSubmitting(false);
    }
  }

  function handleLogout() {
    clearSession();
    setCurrentUser(null);
  }

  return (
    <section className="section-grid two-column-grid">
      <article className="card form-card">
        <h3>Sign in</h3>
        <p>Use a lightweight dev session so project, property, and visit data are scoped to one user.</p>
        <form className="form-stack" onSubmit={handleLogin}>
          <label className="field">
            <span>Email</span>
            <input
              value={draft.email}
              onChange={(event) => setDraft((current) => ({ ...current, email: event.target.value }))}
            />
          </label>
          <label className="field">
            <span>Display name</span>
            <input
              value={draft.displayName}
              onChange={(event) => setDraft((current) => ({ ...current, displayName: event.target.value }))}
            />
          </label>
          <label className="field">
            <span>Role</span>
            <select
              value={draft.role}
              onChange={(event) =>
                setDraft((current) => ({ ...current, role: event.target.value as "buyer" | "admin" }))
              }
            >
              <option value="buyer">buyer</option>
              <option value="admin">admin</option>
            </select>
          </label>
          {error ? <p className="status-text error-text">{error}</p> : null}
          <button type="submit" className="primary-button">
            {isSubmitting ? "Signing in..." : "Create session"}
          </button>
        </form>
      </article>
      <article className="card">
        <h3>Current session</h3>
        {isLoading ? <p className="status-text">Checking current session...</p> : null}
        {currentUser ? (
          <>
            <div className="stack-list">
              <div className="data-card">
                <div className="data-card-topline">
                  <strong>{currentUser.display_name}</strong>
                  <span>{currentUser.user_id}</span>
                </div>
                <p>{currentUser.email}</p>
                <p>Role: {currentUser.role}</p>
              </div>
            </div>
            <button type="button" className="primary-button" onClick={handleLogout}>
              Sign out
            </button>
          </>
        ) : (
          <p className="status-text">No active session yet. Sign in before using the project routes.</p>
        )}
      </article>
    </section>
  );
}

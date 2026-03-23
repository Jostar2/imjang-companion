"use client";

import { useEffect, useState } from "react";

import { clearSession, getStoredSession, me, type Me } from "../../lib/imjang-api";

export function SessionBanner() {
  const [currentUser, setCurrentUser] = useState<Me | null>(null);

  useEffect(() => {
    async function load() {
      const session = getStoredSession();
      if (!session) {
        return;
      }

      try {
        const user = await me();
        setCurrentUser(user);
      } catch {
        clearSession();
      }
    }

    void load();
  }, []);

  return (
    <div className="session-banner">
      {currentUser ? (
        <>
          <strong>{currentUser.display_name}</strong>
          <span>{currentUser.email}</span>
          <span>{currentUser.role}</span>
        </>
      ) : (
        <span>No active session. Sign in from the home page first.</span>
      )}
    </div>
  );
}

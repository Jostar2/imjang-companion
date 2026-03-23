import Link from "next/link";

import { SessionBanner } from "../auth/session-banner";

type NavItem = {
  href: string;
  title: string;
  description: string;
};

const navItems: NavItem[] = [
  {
    href: "/projects",
    title: "Projects",
    description: "Create and track visit projects by area or deal thesis."
  },
  {
    href: "/properties",
    title: "Properties",
    description: "Register candidate properties with listing and visit metadata."
  },
  {
    href: "/visits",
    title: "Visit Flow",
    description: "Run the checklist, capture scores, and attach notes and photos."
  },
  {
    href: "/comparison",
    title: "Comparison",
    description: "Compare candidates with scores, red flags, and visit summaries."
  },
  {
    href: "/report",
    title: "Report",
    description: "Generate a summary report for post-visit review."
  },
  {
    href: "/ops",
    title: "Ops",
    description: "Admin-only release readiness and portfolio summary."
  }
];

export function ProjectShell({
  title,
  description,
  tags,
  children
}: {
  title: string;
  description: string;
  tags: string[];
  children: React.ReactNode;
}) {
  return (
    <main>
      <div className="page-shell">
        <section className="hero">
          <div className="chip-row">
            {tags.map((tag) => (
              <span key={tag} className="chip">
                {tag}
              </span>
            ))}
          </div>
          <SessionBanner />
          <h1>{title}</h1>
          <p>{description}</p>
        </section>
        {children}
        <section className="nav-grid">
          {navItems.map((item) => (
            <Link key={item.href} href={item.href} className="nav-tile">
              <strong>{item.title}</strong>
              <span>{item.description}</span>
            </Link>
          ))}
        </section>
      </div>
    </main>
  );
}

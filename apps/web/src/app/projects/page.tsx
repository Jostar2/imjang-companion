import { ProjectShell } from "../../components/projects/project-shell";
import { ProjectBoard } from "../../components/projects/project-board";

export default function ProjectsPage() {
  return (
    <ProjectShell
      title="Visit Projects"
      description="Each project groups candidate properties under one search mission such as a district, a budget band, or an investment thesis."
      tags={["FE-001", "Project CRUD"]}
    >
      <ProjectBoard />
    </ProjectShell>
  );
}

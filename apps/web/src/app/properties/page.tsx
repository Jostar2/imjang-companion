import { ProjectShell } from "../../components/projects/project-shell";
import { PropertyBoard } from "../../components/projects/property-board";

export default function PropertiesPage() {
  return (
    <ProjectShell
      title="Candidate Properties"
      description="Manual property entry stays in scope for the MVP so the team can focus on visit workflow instead of listing integration."
      tags={["FE-001", "Property list"]}
    >
      <PropertyBoard />
    </ProjectShell>
  );
}

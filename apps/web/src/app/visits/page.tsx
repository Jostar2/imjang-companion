import { ProjectShell } from "../../components/projects/project-shell";
import { ChecklistWorkspace } from "../../components/visits/checklist-workspace";

export default function VisitsPage() {
  return (
    <ProjectShell
      title="Visit Checklist"
      description="This route will host the structured property, building, neighborhood, and red-flag checklist flow."
      tags={["FE-002", "Visit flow"]}
    >
      <ChecklistWorkspace />
    </ProjectShell>
  );
}

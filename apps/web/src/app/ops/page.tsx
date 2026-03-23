import { AdminConsole } from "../../components/ops/admin-console";
import { ProjectShell } from "../../components/projects/project-shell";

export default function OpsPage() {
  return (
    <ProjectShell
      title="Ops Console"
      description="Admin-only release readiness and dataset visibility for bounded staging and release decisions."
      tags={["Ops", "Admin", "Release"]}
    >
      <AdminConsole />
    </ProjectShell>
  );
}

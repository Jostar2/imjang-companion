import { ProjectShell } from "../../components/projects/project-shell";
import { ReportPreview } from "../../components/report/report-preview";

export default function ReportPage() {
  return (
    <ProjectShell
      title="Visit Report"
      description="This route will summarize a single visit with scores, findings, and recommendation notes."
      tags={["FE-003", "Report"]}
    >
      <ReportPreview />
    </ProjectShell>
  );
}

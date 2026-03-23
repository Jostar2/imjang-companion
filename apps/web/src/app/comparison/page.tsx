import { ProjectShell } from "../../components/projects/project-shell";
import { ComparisonBoard } from "../../components/report/comparison-board";

export default function ComparisonPage() {
  return (
    <ProjectShell
      title="Comparison View"
      description="This route is reserved for side-by-side property comparison with aggregate scores and red flags."
      tags={["FE-003", "Comparison"]}
    >
      <ComparisonBoard />
    </ProjectShell>
  );
}

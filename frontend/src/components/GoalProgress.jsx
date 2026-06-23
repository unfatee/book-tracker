import { Target } from "lucide-react";

import { clampProgress } from "../utils/progressUtils";

export default function GoalProgress({ progress }) {
  if (!progress) {
    return (
      <div className="goal-panel">
        <Target size={24} />
        <div>
          <h3>No reading goal yet</h3>
          <p>Create a goal for this year to track completed books.</p>
        </div>
      </div>
    );
  }

  const percent = clampProgress(progress.progress_percent);

  return (
    <div className="goal-panel">
      <Target size={24} />
      <div className="goal-content">
        <div className="progress-meta">
          <span>
            {progress.completed_books} of {progress.target_books} books completed
          </span>
          <strong>{percent}%</strong>
        </div>
        <div className="progress-track">
          <span style={{ width: `${percent}%` }} />
        </div>
        <p>{progress.remaining_books} books remaining in {progress.year}</p>
      </div>
    </div>
  );
}

import { clampProgress, progressLabel } from "../utils/progressUtils";

export default function BookProgress({ book }) {
  const progress = clampProgress(book.progress_percent);

  return (
    <div className="progress-stack">
      <div className="progress-meta">
        <span>{progressLabel(book)}</span>
        <strong>{progress}%</strong>
      </div>
      <div className="progress-track" aria-label="Reading progress">
        <span style={{ width: `${progress}%` }} />
      </div>
    </div>
  );
}

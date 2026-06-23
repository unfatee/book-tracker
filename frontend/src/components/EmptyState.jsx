import { BookOpen } from "lucide-react";

export default function EmptyState({ title = "No data yet", message = "Create your first entry to see it here." }) {
  return (
    <div className="empty-state">
      <BookOpen size={32} />
      <h3>{title}</h3>
      <p>{message}</p>
    </div>
  );
}

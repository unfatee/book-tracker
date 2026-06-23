export const BOOK_STATUSES = [
  { value: "want_to_read", label: "Want to Read" },
  { value: "reading", label: "Reading" },
  { value: "completed", label: "Completed" },
  { value: "paused", label: "Paused" },
  { value: "dropped", label: "Dropped" },
];

export const SORT_OPTIONS = [
  { value: "updated_at", label: "Recently updated" },
  { value: "created_at", label: "Recently added" },
  { value: "title", label: "Title" },
  { value: "author", label: "Author" },
  { value: "rating", label: "Rating" },
  { value: "progress", label: "Progress" },
  { value: "finish_date", label: "Finish date" },
];

export function getStatusLabel(status) {
  return BOOK_STATUSES.find((item) => item.value === status)?.label || status;
}

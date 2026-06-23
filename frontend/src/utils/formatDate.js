export function formatDate(value) {
  if (!value) return "Not set";
  return new Intl.DateTimeFormat("en", {
    year: "numeric",
    month: "short",
    day: "numeric",
  }).format(new Date(value));
}

export function toDateInput(value) {
  if (!value) return "";
  return String(value).slice(0, 10);
}

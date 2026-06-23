export function clampProgress(value) {
  const number = Number(value) || 0;
  return Math.max(0, Math.min(100, number));
}

export function progressLabel(book) {
  return `${book.current_page || 0} / ${book.total_pages || 0} pages`;
}

import { Save } from "lucide-react";
import { useEffect, useState } from "react";

import { BOOK_STATUSES } from "../utils/constants";
import { toDateInput } from "../utils/formatDate";

const emptyBook = {
  title: "",
  author: "",
  description: "",
  genre: "",
  total_pages: 1,
  current_page: 0,
  status: "want_to_read",
  rating: "",
  cover_url: "",
  start_date: "",
  finish_date: "",
  is_favorite: false,
  personal_notes: "",
};

export default function BookForm({ initialBook, onSubmit, submitLabel = "Save Book", loading = false }) {
  const [form, setForm] = useState(emptyBook);

  useEffect(() => {
    if (!initialBook) {
      setForm(emptyBook);
      return;
    }
    setForm({
      ...emptyBook,
      ...initialBook,
      rating: initialBook.rating ?? "",
      start_date: toDateInput(initialBook.start_date),
      finish_date: toDateInput(initialBook.finish_date),
      cover_url: initialBook.cover_url || "",
      description: initialBook.description || "",
      genre: initialBook.genre || "",
      personal_notes: initialBook.personal_notes || "",
    });
  }, [initialBook]);

  const updateField = (event) => {
    const { name, value, type, checked } = event.target;
    setForm((current) => ({ ...current, [name]: type === "checkbox" ? checked : value }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const payload = {
      ...form,
      total_pages: Number(form.total_pages),
      current_page: Number(form.current_page || 0),
      rating: form.rating === "" ? null : Number(form.rating),
      description: form.description || null,
      genre: form.genre || null,
      cover_url: form.cover_url || null,
      start_date: form.start_date || null,
      finish_date: form.finish_date || null,
      personal_notes: form.personal_notes || null,
    };
    onSubmit(payload);
  };

  return (
    <form className="form-grid" onSubmit={handleSubmit}>
      <label>
        <span>Title</span>
        <input name="title" value={form.title} onChange={updateField} required />
      </label>
      <label>
        <span>Author</span>
        <input name="author" value={form.author} onChange={updateField} required />
      </label>
      <label>
        <span>Genre</span>
        <input name="genre" value={form.genre} onChange={updateField} placeholder="Programming" />
      </label>
      <label>
        <span>Status</span>
        <select name="status" value={form.status} onChange={updateField}>
          {BOOK_STATUSES.map((status) => (
            <option key={status.value} value={status.value}>
              {status.label}
            </option>
          ))}
        </select>
      </label>
      <label>
        <span>Total pages</span>
        <input name="total_pages" type="number" min="1" value={form.total_pages} onChange={updateField} required />
      </label>
      <label>
        <span>Current page</span>
        <input name="current_page" type="number" min="0" value={form.current_page} onChange={updateField} />
      </label>
      <label>
        <span>Rating</span>
        <select name="rating" value={form.rating} onChange={updateField}>
          <option value="">Not rated</option>
          {[1, 2, 3, 4, 5].map((rating) => (
            <option key={rating} value={rating}>
              {rating}/5
            </option>
          ))}
        </select>
      </label>
      <label>
        <span>Cover URL</span>
        <input name="cover_url" value={form.cover_url} onChange={updateField} placeholder="https://..." />
      </label>
      <label>
        <span>Start date</span>
        <input name="start_date" type="date" value={form.start_date} onChange={updateField} />
      </label>
      <label>
        <span>Finish date</span>
        <input name="finish_date" type="date" value={form.finish_date} onChange={updateField} />
      </label>
      <label className="checkbox-row">
        <input name="is_favorite" type="checkbox" checked={form.is_favorite} onChange={updateField} />
        <span>Favorite book</span>
      </label>
      <label className="full-span">
        <span>Description</span>
        <textarea name="description" rows="4" value={form.description} onChange={updateField} />
      </label>
      <label className="full-span">
        <span>Personal notes</span>
        <textarea name="personal_notes" rows="4" value={form.personal_notes} onChange={updateField} />
      </label>
      <div className="full-span form-actions">
        <button className="button primary" type="submit" disabled={loading}>
          <Save size={16} />
          {loading ? "Saving..." : submitLabel}
        </button>
      </div>
    </form>
  );
}

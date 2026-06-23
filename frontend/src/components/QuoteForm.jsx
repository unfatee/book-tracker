import { Save } from "lucide-react";
import { useState } from "react";

export default function QuoteForm({ onSubmit, loading = false }) {
  const [form, setForm] = useState({ text: "", page: "", note: "" });

  const updateField = (event) => {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    await onSubmit({
      text: form.text,
      page: form.page ? Number(form.page) : null,
      note: form.note || null,
    });
    setForm({ text: "", page: "", note: "" });
  };

  return (
    <form className="quote-form" onSubmit={handleSubmit}>
      <label>
        <span>Quote</span>
        <textarea name="text" rows="3" value={form.text} onChange={updateField} required />
      </label>
      <label>
        <span>Page</span>
        <input name="page" type="number" min="1" value={form.page} onChange={updateField} />
      </label>
      <label>
        <span>Note</span>
        <input name="note" value={form.note} onChange={updateField} />
      </label>
      <button className="button primary" type="submit" disabled={loading}>
        <Save size={16} />
        {loading ? "Saving..." : "Add Quote"}
      </button>
    </form>
  );
}

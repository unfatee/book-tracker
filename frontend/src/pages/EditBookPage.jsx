import { ArrowLeft } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

import { getApiError } from "../api/axiosClient";
import { booksApi } from "../api/booksApi";
import BookForm from "../components/BookForm.jsx";

export default function EditBookPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [book, setBook] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    async function loadBook() {
      try {
        const data = await booksApi.getBook(id);
        setBook(data);
      } catch (err) {
        setError(getApiError(err, "Could not load book"));
      } finally {
        setLoading(false);
      }
    }
    loadBook();
  }, [id]);

  const handleSubmit = async (payload) => {
    setSaving(true);
    setError("");
    try {
      await booksApi.updateBook(id, payload);
      navigate(`/books/${id}`);
    } catch (err) {
      setError(getApiError(err, "Could not update book"));
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="loading-panel">Loading book...</div>;

  return (
    <div className="stack">
      <Link className="button ghost fit-content" to={`/books/${id}`}>
        <ArrowLeft size={16} />
        Back to Details
      </Link>
      <section className="panel">
        <div className="section-heading">
          <h1>Edit Book</h1>
        </div>
        {error ? <p className="error-text">{error}</p> : null}
        {book ? <BookForm initialBook={book} onSubmit={handleSubmit} submitLabel="Save Changes" loading={saving} /> : null}
      </section>
    </div>
  );
}

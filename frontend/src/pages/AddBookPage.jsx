import { ArrowLeft } from "lucide-react";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { getApiError } from "../api/axiosClient";
import { booksApi } from "../api/booksApi";
import BookForm from "../components/BookForm.jsx";

export default function AddBookPage() {
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (payload) => {
    setLoading(true);
    setError("");
    try {
      const book = await booksApi.createBook(payload);
      navigate(`/books/${book.id}`);
    } catch (err) {
      setError(getApiError(err, "Could not create book"));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="stack">
      <Link className="button ghost fit-content" to="/books">
        <ArrowLeft size={16} />
        Back to Books
      </Link>
      <section className="panel">
        <div className="section-heading">
          <h1>Add Book</h1>
        </div>
        {error ? <p className="error-text">{error}</p> : null}
        <BookForm onSubmit={handleSubmit} submitLabel="Create Book" loading={loading} />
      </section>
    </div>
  );
}

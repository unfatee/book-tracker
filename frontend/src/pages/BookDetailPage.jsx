import { ArrowLeft, Edit, Heart, RefreshCw, Trash2 } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

import { getApiError } from "../api/axiosClient";
import { booksApi } from "../api/booksApi";
import { quotesApi } from "../api/quotesApi";
import BookProgress from "../components/BookProgress.jsx";
import EmptyState from "../components/EmptyState.jsx";
import QuoteForm from "../components/QuoteForm.jsx";
import QuoteList from "../components/QuoteList.jsx";
import { BOOK_STATUSES, getStatusLabel } from "../utils/constants";
import { formatDate } from "../utils/formatDate";

function DetailCover({ book }) {
  if (book.cover_url) {
    return <img className="detail-cover" src={book.cover_url} alt={`${book.title} cover`} />;
  }

  return (
    <div className="detail-cover placeholder-cover">
      <span>{book.title?.charAt(0)?.toUpperCase() || "B"}</span>
    </div>
  );
}

export default function BookDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [book, setBook] = useState(null);
  const [quotes, setQuotes] = useState([]);
  const [progressPage, setProgressPage] = useState("");
  const [statusChoice, setStatusChoice] = useState("reading");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [quoteLoading, setQuoteLoading] = useState(false);

  const loadDetail = async () => {
    setLoading(true);
    setError("");
    try {
      const [bookData, quoteData] = await Promise.all([booksApi.getBook(id), quotesApi.getBookQuotes(id)]);
      setBook(bookData);
      setQuotes(quoteData);
      setProgressPage(bookData.current_page);
      setStatusChoice(bookData.status);
    } catch (err) {
      setError(getApiError(err, "Could not load book details"));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDetail();
  }, [id]);

  const updateProgress = async (event) => {
    event.preventDefault();
    try {
      const updated = await booksApi.updateProgress(id, Number(progressPage));
      setBook(updated);
    } catch (err) {
      setError(getApiError(err, "Could not update progress"));
    }
  };

  const updateStatus = async () => {
    try {
      const updated = await booksApi.updateStatus(id, statusChoice);
      setBook(updated);
      setProgressPage(updated.current_page);
    } catch (err) {
      setError(getApiError(err, "Could not update status"));
    }
  };

  const toggleFavorite = async () => {
    try {
      const updated = await booksApi.toggleFavorite(id);
      setBook(updated);
    } catch (err) {
      setError(getApiError(err, "Could not update favorite"));
    }
  };

  const deleteBook = async () => {
    if (!window.confirm("Delete this book and its quotes?")) return;
    try {
      await booksApi.deleteBook(id);
      navigate("/books");
    } catch (err) {
      setError(getApiError(err, "Could not delete book"));
    }
  };

  const createQuote = async (payload) => {
    setQuoteLoading(true);
    try {
      await quotesApi.createQuote(id, payload);
      const quoteData = await quotesApi.getBookQuotes(id);
      setQuotes(quoteData);
    } catch (err) {
      setError(getApiError(err, "Could not add quote"));
    } finally {
      setQuoteLoading(false);
    }
  };

  const deleteQuote = async (quoteId) => {
    try {
      await quotesApi.deleteQuote(id, quoteId);
      setQuotes((current) => current.filter((quote) => quote.id !== quoteId));
    } catch (err) {
      setError(getApiError(err, "Could not delete quote"));
    }
  };

  if (loading) return <div className="loading-panel">Loading book...</div>;
  if (!book) return <EmptyState title="Book not found" message={error || "The requested book is unavailable."} />;

  return (
    <div className="stack">
      <Link className="button ghost fit-content" to="/books">
        <ArrowLeft size={16} />
        Back to Books
      </Link>

      {error ? <p className="error-text">{error}</p> : null}

      <section className="detail-layout">
        <DetailCover book={book} />
        <div className="panel detail-panel">
          <div className="detail-title-row">
            <div>
              <p className="eyebrow">{book.genre || "Uncategorized"}</p>
              <h1>{book.title}</h1>
              <p className="muted">{book.author}</p>
            </div>
            <button
              type="button"
              className={`icon-button ${book.is_favorite ? "is-active" : ""}`}
              onClick={toggleFavorite}
              title={book.is_favorite ? "Remove from favorites" : "Mark as favorite"}
            >
              <Heart size={20} />
            </button>
          </div>

          <div className="detail-facts">
            <span className={`status-pill status-${book.status}`}>{getStatusLabel(book.status)}</span>
            <span>Rating {book.rating ? `${book.rating}/5` : "not set"}</span>
            <span>Started {formatDate(book.start_date)}</span>
            <span>Finished {formatDate(book.finish_date)}</span>
          </div>

          <BookProgress book={book} />
          {book.description ? <p>{book.description}</p> : null}
          {book.personal_notes ? (
            <div className="notes-box">
              <h3>Personal Notes</h3>
              <p>{book.personal_notes}</p>
            </div>
          ) : null}

          <div className="detail-actions">
            <Link className="button secondary" to={`/books/${book.id}/edit`}>
              <Edit size={16} />
              Edit
            </Link>
            <button className="button danger ghost" type="button" onClick={deleteBook}>
              <Trash2 size={16} />
              Delete
            </button>
          </div>
        </div>
      </section>

      <section className="two-column align-start">
        <article className="panel">
          <div className="section-heading">
            <h2>Update Reading</h2>
          </div>
          <form className="inline-form" onSubmit={updateProgress}>
            <label>
              <span>Current page</span>
              <input
                type="number"
                min="0"
                max={book.total_pages}
                value={progressPage}
                onChange={(event) => setProgressPage(event.target.value)}
              />
            </label>
            <button className="button primary" type="submit">
              <RefreshCw size={16} />
              Update
            </button>
          </form>
          <div className="inline-form">
            <label>
              <span>Status</span>
              <select value={statusChoice} onChange={(event) => setStatusChoice(event.target.value)}>
                {BOOK_STATUSES.map((status) => (
                  <option key={status.value} value={status.value}>
                    {status.label}
                  </option>
                ))}
              </select>
            </label>
            <button className="button secondary" type="button" onClick={updateStatus}>
              <RefreshCw size={16} />
              Save Status
            </button>
          </div>
        </article>

        <article className="panel">
          <div className="section-heading">
            <h2>Add Quote</h2>
          </div>
          <QuoteForm onSubmit={createQuote} loading={quoteLoading} />
        </article>
      </section>

      <section className="panel">
        <div className="section-heading">
          <h2>Quotes</h2>
          <span>{quotes.length}</span>
        </div>
        {quotes.length ? (
          <QuoteList quotes={quotes} onDelete={deleteQuote} />
        ) : (
          <EmptyState title="No quotes yet" message="Save memorable passages from this book." />
        )}
      </section>
    </div>
  );
}

import { Search } from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { getApiError } from "../api/axiosClient";
import { quotesApi } from "../api/quotesApi";
import EmptyState from "../components/EmptyState.jsx";

export default function QuotesPage() {
  const [quotes, setQuotes] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadQuotes() {
      setLoading(true);
      setError("");
      try {
        const data = await quotesApi.getQuotes({ search: search || undefined });
        setQuotes(data);
      } catch (err) {
        setError(getApiError(err, "Could not load quotes"));
      } finally {
        setLoading(false);
      }
    }
    loadQuotes();
  }, [search]);

  return (
    <div className="stack">
      <div className="page-header">
        <div>
          <p className="eyebrow">Highlights</p>
          <h1>Quotes</h1>
        </div>
      </div>

      <section className="filters-panel single">
        <label className="search-field">
          <Search size={18} />
          <input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search quotes" />
        </label>
      </section>

      {error ? <p className="error-text">{error}</p> : null}
      {loading ? <div className="loading-panel">Loading quotes...</div> : null}
      {!loading && !quotes.length ? (
        <EmptyState title="No quotes found" message="Quotes saved from book detail pages will appear here." />
      ) : null}

      <section className="quote-list">
        {quotes.map((quote) => (
          <article className="quote-card" key={quote.id}>
            <blockquote>{quote.text}</blockquote>
            <div className="quote-meta">
              <Link to={`/books/${quote.book_id}`}>{quote.book_title || "Book"}</Link>
              {quote.page ? <span>Page {quote.page}</span> : null}
            </div>
            {quote.note ? <p className="muted">{quote.note}</p> : null}
          </article>
        ))}
      </section>
    </div>
  );
}

import { Download, Plus, Search } from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { getApiError } from "../api/axiosClient";
import { booksApi } from "../api/booksApi";
import { exportApi } from "../api/exportApi";
import BookCard from "../components/BookCard.jsx";
import EmptyState from "../components/EmptyState.jsx";
import { BOOK_STATUSES, SORT_OPTIONS } from "../utils/constants";

export default function BooksPage() {
  const [books, setBooks] = useState([]);
  const [filters, setFilters] = useState({
    search: "",
    status: "",
    genre: "",
    rating: "",
    favorites: false,
    sort_by: "updated_at",
    sort_order: "desc",
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadBooks = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await booksApi.getBooks({
        search: filters.search || undefined,
        status: filters.status || undefined,
        genre: filters.genre || undefined,
        rating: filters.rating || undefined,
        is_favorite: filters.favorites ? true : undefined,
        sort_by: filters.sort_by,
        sort_order: filters.sort_order,
      });
      setBooks(data);
    } catch (err) {
      setError(getApiError(err, "Could not load books"));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadBooks();
  }, [filters]);

  const updateFilter = (event) => {
    const { name, value, type, checked } = event.target;
    setFilters((current) => ({ ...current, [name]: type === "checkbox" ? checked : value }));
  };

  const toggleFavorite = async (bookId) => {
    try {
      const updated = await booksApi.toggleFavorite(bookId);
      setBooks((current) => current.map((book) => (book.id === bookId ? updated : book)));
    } catch (err) {
      setError(getApiError(err, "Could not update favorite"));
    }
  };

  const exportCsv = async () => {
    try {
      const blob = await exportApi.booksCsv();
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "books.csv";
      link.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError(getApiError(err, "Could not export CSV"));
    }
  };

  return (
    <div className="stack">
      <div className="page-header">
        <div>
          <p className="eyebrow">Library</p>
          <h1>Books</h1>
        </div>
        <div className="header-actions">
          <button className="button secondary" type="button" onClick={exportCsv}>
            <Download size={16} />
            Export CSV
          </button>
          <Link className="button primary" to="/books/new">
            <Plus size={16} />
            Add Book
          </Link>
        </div>
      </div>

      <section className="filters-panel">
        <label className="search-field">
          <Search size={18} />
          <input name="search" value={filters.search} onChange={updateFilter} placeholder="Search title or author" />
        </label>
        <select name="status" value={filters.status} onChange={updateFilter}>
          <option value="">All statuses</option>
          {BOOK_STATUSES.map((status) => (
            <option key={status.value} value={status.value}>
              {status.label}
            </option>
          ))}
        </select>
        <input name="genre" value={filters.genre} onChange={updateFilter} placeholder="Genre" />
        <select name="rating" value={filters.rating} onChange={updateFilter}>
          <option value="">Any rating</option>
          {[1, 2, 3, 4, 5].map((rating) => (
            <option key={rating} value={rating}>
              {rating}/5
            </option>
          ))}
        </select>
        <select name="sort_by" value={filters.sort_by} onChange={updateFilter}>
          {SORT_OPTIONS.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
        <select name="sort_order" value={filters.sort_order} onChange={updateFilter}>
          <option value="desc">Desc</option>
          <option value="asc">Asc</option>
        </select>
        <label className="checkbox-row compact">
          <input name="favorites" type="checkbox" checked={filters.favorites} onChange={updateFilter} />
          <span>Favorites</span>
        </label>
      </section>

      {error ? <p className="error-text">{error}</p> : null}
      {loading ? <div className="loading-panel">Loading books...</div> : null}
      {!loading && !books.length ? (
        <EmptyState title="No books found" message="Adjust filters or add a new book." />
      ) : null}
      <section className="books-grid">
        {books.map((book) => (
          <BookCard key={book.id} book={book} onFavorite={toggleFavorite} />
        ))}
      </section>
    </div>
  );
}

import { Edit, Eye, Heart } from "lucide-react";
import { Link } from "react-router-dom";

import { getStatusLabel } from "../utils/constants";
import { formatDate } from "../utils/formatDate";
import BookProgress from "./BookProgress.jsx";

function Cover({ book }) {
  if (book.cover_url) {
    return <img className="book-cover" src={book.cover_url} alt={`${book.title} cover`} />;
  }

  return (
    <div className="book-cover placeholder-cover">
      <span>{book.title?.charAt(0)?.toUpperCase() || "B"}</span>
    </div>
  );
}

export default function BookCard({ book, onFavorite }) {
  return (
    <article className="book-card">
      <Cover book={book} />
      <div className="book-card-body">
        <div className="book-card-top">
          <div>
            <p className="eyebrow">{book.genre || "Uncategorized"}</p>
            <h3>{book.title}</h3>
            <p className="muted">{book.author}</p>
          </div>
          <button
            type="button"
            className={`icon-button ${book.is_favorite ? "is-active" : ""}`}
            onClick={() => onFavorite?.(book.id)}
            title={book.is_favorite ? "Remove from favorites" : "Mark as favorite"}
          >
            <Heart size={18} />
          </button>
        </div>

        <BookProgress book={book} />

        <div className="book-card-details">
          <span className={`status-pill status-${book.status}`}>{getStatusLabel(book.status)}</span>
          <span>Rating {book.rating ? `${book.rating}/5` : "not set"}</span>
          <span>Updated {formatDate(book.updated_at)}</span>
        </div>

        <div className="card-actions">
          <Link className="button secondary" to={`/books/${book.id}`}>
            <Eye size={16} />
            Details
          </Link>
          <Link className="button ghost" to={`/books/${book.id}/edit`}>
            <Edit size={16} />
            Edit
          </Link>
        </div>
      </div>
    </article>
  );
}

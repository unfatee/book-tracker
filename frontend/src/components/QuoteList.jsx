import { Trash2 } from "lucide-react";

export default function QuoteList({ quotes, onDelete }) {
  return (
    <div className="quote-list">
      {quotes.map((quote) => (
        <article className="quote-card" key={quote.id}>
          <blockquote>{quote.text}</blockquote>
          <div className="quote-meta">
            <span>{quote.book_title || "This book"}</span>
            {quote.page ? <span>Page {quote.page}</span> : null}
          </div>
          {quote.note ? <p className="muted">{quote.note}</p> : null}
          {onDelete ? (
            <button className="button danger ghost" type="button" onClick={() => onDelete(quote.id)}>
              <Trash2 size={16} />
              Delete
            </button>
          ) : null}
        </article>
      ))}
    </div>
  );
}

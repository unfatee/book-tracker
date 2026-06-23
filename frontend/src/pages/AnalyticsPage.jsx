import { BookOpen, CheckCircle2, FileText, Heart, Star } from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { analyticsApi } from "../api/analyticsApi";
import { getApiError } from "../api/axiosClient";
import EmptyState from "../components/EmptyState.jsx";
import GenreChart from "../components/GenreChart.jsx";
import MonthlyReadingChart from "../components/MonthlyReadingChart.jsx";
import SummaryCard from "../components/SummaryCard.jsx";
import { formatDate } from "../utils/formatDate";

export default function AnalyticsPage() {
  const [state, setState] = useState({ summary: null, genres: [], monthly: [], authors: [], recent: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadAnalytics() {
      setLoading(true);
      setError("");
      try {
        const year = new Date().getFullYear();
        const [summary, genres, monthly, authors, recent] = await Promise.all([
          analyticsApi.summary(),
          analyticsApi.byGenre(),
          analyticsApi.monthlyReading(year),
          analyticsApi.topAuthors(),
          analyticsApi.recentActivity(),
        ]);
        setState({ summary, genres, monthly, authors, recent });
      } catch (err) {
        setError(getApiError(err, "Could not load analytics"));
      } finally {
        setLoading(false);
      }
    }
    loadAnalytics();
  }, []);

  if (loading) return <div className="loading-panel">Loading analytics...</div>;

  const summary = state.summary || {};

  return (
    <div className="stack">
      <div className="page-header">
        <div>
          <p className="eyebrow">Insights</p>
          <h1>Analytics</h1>
        </div>
      </div>

      {error ? <p className="error-text">{error}</p> : null}

      <section className="summary-grid">
        <SummaryCard icon={BookOpen} label="Total Books" value={summary.total_books} accent="blue" />
        <SummaryCard icon={CheckCircle2} label="Completed" value={summary.completed_books} accent="green" />
        <SummaryCard icon={FileText} label="Pages Read" value={summary.total_pages_read} accent="slate" />
        <SummaryCard icon={Star} label="Average Rating" value={summary.average_rating ?? "Not rated"} accent="amber" />
        <SummaryCard icon={Heart} label="Favorites" value={summary.favorite_books} accent="red" />
      </section>

      <section className="two-column">
        <article className="panel">
          <div className="section-heading">
            <h2>Genre Breakdown</h2>
          </div>
          <GenreChart data={state.genres} />
        </article>
        <article className="panel">
          <div className="section-heading">
            <h2>Books Completed by Month</h2>
          </div>
          <MonthlyReadingChart data={state.monthly} />
        </article>
      </section>

      <section className="two-column align-start">
        <article className="panel">
          <div className="section-heading">
            <h2>Top Authors</h2>
          </div>
          {state.authors.length ? (
            <div className="rank-list">
              {state.authors.map((author, index) => (
                <div key={author.author} className="rank-row">
                  <span>{index + 1}</span>
                  <strong>{author.author}</strong>
                  <em>{author.books_count} books</em>
                </div>
              ))}
            </div>
          ) : (
            <EmptyState title="No author data" message="Add books to see top authors." />
          )}
        </article>

        <article className="panel">
          <div className="section-heading">
            <h2>Recent Activity</h2>
          </div>
          {state.recent.length ? (
            <div className="activity-list">
              {state.recent.map((book) => (
                <Link key={book.id} to={`/books/${book.id}`}>
                  <strong>{book.title}</strong>
                  <span>{book.progress_percent}% complete | {formatDate(book.updated_at)}</span>
                </Link>
              ))}
            </div>
          ) : (
            <EmptyState title="No recent activity" message="Your updates will show up here." />
          )}
        </article>
      </section>
    </div>
  );
}

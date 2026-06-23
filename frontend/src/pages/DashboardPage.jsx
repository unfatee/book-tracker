import { BookOpen, CheckCircle2, FileText, Library, Plus, Sparkles, Star, Target } from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { analyticsApi } from "../api/analyticsApi";
import { getApiError } from "../api/axiosClient";
import { booksApi } from "../api/booksApi";
import EmptyState from "../components/EmptyState.jsx";
import GenreChart from "../components/GenreChart.jsx";
import MonthlyReadingChart from "../components/MonthlyReadingChart.jsx";
import SummaryCard from "../components/SummaryCard.jsx";
import { formatDate } from "../utils/formatDate";

export default function DashboardPage() {
  const [state, setState] = useState({ summary: null, genres: [], monthly: [], recent: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [demoLoading, setDemoLoading] = useState(false);

  const loadDashboard = async () => {
    setLoading(true);
    setError("");
    try {
      const year = new Date().getFullYear();
      const [summary, genres, monthly, recent] = await Promise.all([
        analyticsApi.summary(),
        analyticsApi.byGenre(),
        analyticsApi.monthlyReading(year),
        analyticsApi.recentActivity(),
      ]);
      setState({ summary, genres, monthly, recent });
    } catch (err) {
      setError(getApiError(err, "Could not load dashboard"));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboard();
  }, []);

  const createDemoData = async () => {
    setDemoLoading(true);
    setError("");
    try {
      await booksApi.createDemoData();
      await loadDashboard();
    } catch (err) {
      setError(getApiError(err, "Could not create demo data"));
    } finally {
      setDemoLoading(false);
    }
  };

  if (loading) return <div className="loading-panel">Loading dashboard...</div>;

  const summary = state.summary || {};

  return (
    <div className="stack">
      <div className="page-header">
        <div>
          <p className="eyebrow">Reading workspace</p>
          <h1>Dashboard</h1>
        </div>
        <div className="header-actions">
          <Link className="button primary" to="/books/new">
            <Plus size={16} />
            Add Book
          </Link>
          <button className="button secondary" type="button" onClick={createDemoData} disabled={demoLoading}>
            <Sparkles size={16} />
            {demoLoading ? "Creating..." : "Create Demo Data"}
          </button>
        </div>
      </div>

      {error ? <p className="error-text">{error}</p> : null}

      <section className="summary-grid">
        <SummaryCard icon={Library} label="Total Books" value={summary.total_books} accent="blue" />
        <SummaryCard icon={CheckCircle2} label="Completed" value={summary.completed_books} accent="green" />
        <SummaryCard icon={BookOpen} label="Currently Reading" value={summary.reading_books} accent="cyan" />
        <SummaryCard icon={Target} label="Want To Read" value={summary.want_to_read_books} accent="amber" />
        <SummaryCard icon={FileText} label="Pages Read" value={summary.total_pages_read} accent="slate" />
        <SummaryCard icon={Star} label="Average Rating" value={summary.average_rating ?? "Not rated"} accent="red" />
      </section>

      <section className="two-column">
        <article className="panel">
          <div className="section-heading">
            <h2>Reading Goal</h2>
            <span>{summary.current_year_goal_progress ?? 0}%</span>
          </div>
          <div className="progress-track large">
            <span style={{ width: `${Math.min(summary.current_year_goal_progress ?? 0, 100)}%` }} />
          </div>
          <p className="muted">
            {summary.current_year_completed || 0} completed this year
            {summary.current_year_goal ? ` of ${summary.current_year_goal}` : ""}
          </p>
        </article>
        <article className="panel">
          <div className="section-heading">
            <h2>Recently Updated</h2>
            <Link to="/books">View all</Link>
          </div>
          {state.recent.length ? (
            <div className="activity-list">
              {state.recent.slice(0, 5).map((book) => (
                <Link key={book.id} to={`/books/${book.id}`}>
                  <strong>{book.title}</strong>
                  <span>{book.status} | {formatDate(book.updated_at)}</span>
                </Link>
              ))}
            </div>
          ) : (
            <EmptyState title="No activity" message="Add books or create demo data to fill this area." />
          )}
        </article>
      </section>

      <section className="two-column">
        <article className="panel">
          <div className="section-heading">
            <h2>Books by Genre</h2>
          </div>
          <GenreChart data={state.genres} />
        </article>
        <article className="panel">
          <div className="section-heading">
            <h2>Monthly Reading</h2>
          </div>
          <MonthlyReadingChart data={state.monthly} />
        </article>
      </section>
    </div>
  );
}

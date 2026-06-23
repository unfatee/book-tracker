import { Save, Trash2 } from "lucide-react";
import { useEffect, useState } from "react";

import { getApiError } from "../api/axiosClient";
import { goalsApi } from "../api/goalsApi";
import GoalProgress from "../components/GoalProgress.jsx";

export default function SettingsPage() {
  const year = new Date().getFullYear();
  const [goal, setGoal] = useState(null);
  const [progress, setProgress] = useState(null);
  const [targetBooks, setTargetBooks] = useState(12);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  const loadGoal = async () => {
    setLoading(true);
    setError("");
    try {
      const [goalData, progressData] = await Promise.all([goalsApi.getGoal(year), goalsApi.progress(year)]);
      setGoal(goalData);
      setProgress(progressData);
      setTargetBooks(goalData.target_books);
    } catch (err) {
      if (err.response?.status !== 404) {
        setError(getApiError(err, "Could not load reading goal"));
      }
      setGoal(null);
      setProgress(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadGoal();
  }, []);

  const saveGoal = async (event) => {
    event.preventDefault();
    setSaving(true);
    setError("");
    try {
      await goalsApi.createOrUpdate({ year, target_books: Number(targetBooks) });
      await loadGoal();
    } catch (err) {
      setError(getApiError(err, "Could not save reading goal"));
    } finally {
      setSaving(false);
    }
  };

  const deleteGoal = async () => {
    if (!goal || !window.confirm("Delete this reading goal?")) return;
    try {
      await goalsApi.delete(year);
      setGoal(null);
      setProgress(null);
      setTargetBooks(12);
    } catch (err) {
      setError(getApiError(err, "Could not delete reading goal"));
    }
  };

  if (loading) return <div className="loading-panel">Loading settings...</div>;

  return (
    <div className="stack">
      <div className="page-header">
        <div>
          <p className="eyebrow">Preferences</p>
          <h1>Settings</h1>
        </div>
      </div>

      {error ? <p className="error-text">{error}</p> : null}

      <section className="two-column align-start">
        <article className="panel">
          <div className="section-heading">
            <h2>Reading Goal for {year}</h2>
          </div>
          <form className="inline-form" onSubmit={saveGoal}>
            <label>
              <span>Target books</span>
              <input
                type="number"
                min="1"
                value={targetBooks}
                onChange={(event) => setTargetBooks(event.target.value)}
              />
            </label>
            <button className="button primary" type="submit" disabled={saving}>
              <Save size={16} />
              {saving ? "Saving..." : "Save Goal"}
            </button>
          </form>
          {goal ? (
            <button className="button danger ghost fit-content" type="button" onClick={deleteGoal}>
              <Trash2 size={16} />
              Delete Goal
            </button>
          ) : null}
        </article>

        <article className="panel">
          <div className="section-heading">
            <h2>Goal Progress</h2>
          </div>
          <GoalProgress progress={progress} />
        </article>
      </section>
    </div>
  );
}

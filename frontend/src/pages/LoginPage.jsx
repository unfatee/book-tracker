import { BookOpen, LogIn } from "lucide-react";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { getApiError } from "../api/axiosClient";
import { useAuth } from "../context/AuthContext.jsx";

export default function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const updateField = (event) => {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      await login(form);
      navigate("/dashboard");
    } catch (err) {
      setError(getApiError(err, "Could not sign in"));
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="auth-card">
      <div className="auth-brand">
        <BookOpen size={34} />
        <h1>Book Tracker</h1>
        <p>Manage your reading library, quotes and yearly goals.</p>
      </div>
      <form className="auth-form" onSubmit={handleSubmit}>
        <label>
          <span>Email</span>
          <input name="email" type="email" value={form.email} onChange={updateField} required />
        </label>
        <label>
          <span>Password</span>
          <input name="password" type="password" value={form.password} onChange={updateField} required />
        </label>
        {error ? <p className="error-text">{error}</p> : null}
        <button className="button primary full-width" type="submit" disabled={loading}>
          <LogIn size={16} />
          {loading ? "Signing in..." : "Sign In"}
        </button>
      </form>
      <p className="auth-switch">
        New here? <Link to="/register">Create an account</Link>
      </p>
    </section>
  );
}

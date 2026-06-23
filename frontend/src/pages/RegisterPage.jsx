import { BookOpen, UserPlus } from "lucide-react";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { getApiError } from "../api/axiosClient";
import { useAuth } from "../context/AuthContext.jsx";

export default function RegisterPage() {
  const navigate = useNavigate();
  const { register } = useAuth();
  const [form, setForm] = useState({ name: "", email: "", password: "" });
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
      await register(form);
      navigate("/dashboard");
    } catch (err) {
      setError(getApiError(err, "Could not create account"));
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="auth-card">
      <div className="auth-brand">
        <BookOpen size={34} />
        <h1>Create Account</h1>
        <p>Start building a searchable reading history.</p>
      </div>
      <form className="auth-form" onSubmit={handleSubmit}>
        <label>
          <span>Name</span>
          <input name="name" value={form.name} onChange={updateField} required />
        </label>
        <label>
          <span>Email</span>
          <input name="email" type="email" value={form.email} onChange={updateField} required />
        </label>
        <label>
          <span>Password</span>
          <input name="password" type="password" minLength="6" value={form.password} onChange={updateField} required />
        </label>
        {error ? <p className="error-text">{error}</p> : null}
        <button className="button primary full-width" type="submit" disabled={loading}>
          <UserPlus size={16} />
          {loading ? "Creating..." : "Create Account"}
        </button>
      </form>
      <p className="auth-switch">
        Already registered? <Link to="/login">Sign in</Link>
      </p>
    </section>
  );
}

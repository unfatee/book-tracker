import { createContext, useContext, useEffect, useMemo, useState } from "react";

import { authApi } from "../api/authApi";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem("book_tracker_token"));
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const logout = () => {
    localStorage.removeItem("book_tracker_token");
    setToken(null);
    setUser(null);
  };

  useEffect(() => {
    const handleLogout = () => logout();
    window.addEventListener("book-tracker:logout", handleLogout);
    return () => window.removeEventListener("book-tracker:logout", handleLogout);
  }, []);

  useEffect(() => {
    let ignore = false;

    async function loadUser() {
      if (!token) {
        setLoading(false);
        return;
      }
      try {
        const me = await authApi.me();
        if (!ignore) setUser(me);
      } catch {
        if (!ignore) logout();
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    loadUser();
    return () => {
      ignore = true;
    };
  }, [token]);

  const login = async (credentials) => {
    const data = await authApi.login(credentials);
    localStorage.setItem("book_tracker_token", data.access_token);
    setToken(data.access_token);
    setUser(data.user);
    return data.user;
  };

  const register = async (payload) => {
    await authApi.register(payload);
    return login({ email: payload.email, password: payload.password });
  };

  const value = useMemo(
    () => ({ user, token, loading, login, register, logout }),
    [user, token, loading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }
  return context;
}

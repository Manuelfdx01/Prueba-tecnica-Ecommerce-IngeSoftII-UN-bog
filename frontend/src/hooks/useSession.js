import { useCallback, useEffect, useState } from "react";

import { api } from "../services/api";

export function useSession() {
  const [token, setToken] = useState(
    () => localStorage.getItem("nexo_token") || "",
  );
  const [user, setUser] = useState(
    () => JSON.parse(localStorage.getItem("nexo_user") || "null"),
  );

  const logout = useCallback(() => {
    localStorage.removeItem("nexo_token");
    localStorage.removeItem("nexo_user");
    setToken("");
    setUser(null);
  }, []);

  useEffect(() => {
    if (!token) {
      setUser(null);
      return;
    }

    let active = true;

    api.getCurrentUser(token)
      .then((currentUser) => {
        if (!active) return;
        setUser(currentUser);
        localStorage.setItem("nexo_user", JSON.stringify(currentUser));
      })
      .catch(() => {
        if (!active) return;
        logout();
      });

    return () => {
      active = false;
    };
  }, [token, logout]);

  async function login(email, password) {
    const session = await api.login(email, password);
    localStorage.setItem("nexo_token", session.access_token);
    localStorage.setItem("nexo_user", JSON.stringify(session.user));
    setToken(session.access_token);
    setUser(session.user);
    return session.user;
  }

  async function register(payload) {
    return api.register(payload);
  }

  return { token, user, login, register, logout };
}

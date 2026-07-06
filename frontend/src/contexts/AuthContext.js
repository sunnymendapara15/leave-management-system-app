import { createContext, useContext, useEffect, useMemo, useState } from "react";

import {
  registerUser,
  loginUser,
  fetchProfile,
  setAuthHeader,
} from "../services/api";

const STORAGE_KEY = "leave_app_token";
const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(() => localStorage.getItem(STORAGE_KEY));
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      setAuthHeader(token);
      fetchProfile()
        .then((response) => setUser(response.data))
        .catch(() => {
          setToken(null);
          localStorage.removeItem(STORAGE_KEY);
        })
        .finally(() => setLoading(false));
    } else {
      setAuthHeader(null);
      setLoading(false);
    }
  }, [token]);

  const signIn = async (payload) => {
    const response = await loginUser(payload);
    const accessToken = response.data.access_token;
    localStorage.setItem(STORAGE_KEY, accessToken);
    setToken(accessToken);
    setAuthHeader(accessToken);
    const profile = await fetchProfile();
    setUser(profile.data);
  };

  const signUp = async (payload) => {
    await registerUser(payload);
    await signIn({ email: payload.email, password: payload.password });
  };

  const signOut = () => {
    localStorage.removeItem(STORAGE_KEY);
    setToken(null);
    setUser(null);
    setAuthHeader(null);
  };

  const value = useMemo(
    () => ({ user, token, loading, signIn, signOut, signUp }),
    [user, token, loading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
};

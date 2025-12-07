// src/AuthContext.js
import React, { createContext, useState, useEffect } from 'react';
import API from './api';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  const loadUser = async () => {
    const access = localStorage.getItem('access_token');
    if (!access) { setUser(null); return; }
    try {
      const res = await API.get('auth/me/'); // protected endpoint
      setUser(res.data);
    } catch (err) {
      setUser(null);
    }
  };

  useEffect(() => {
    loadUser();
  }, []);

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
    window.location.href = '/'; // redirect to login
  };

  return (
    <AuthContext.Provider value={{ user, setUser, loadUser, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

import React, { useState } from "react";
import axios from "axios";
import { FaUser, FaLock, FaSpinner } from "react-icons/fa";
import "./Login.css";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // ✅ Backend login endpoint
  const LOGIN_URL = "http://127.0.0.1:8000/api/auth/login/";

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      // ✅ Send credentials to backend
      const res = await axios.post(LOGIN_URL, { username, password });

      // ✅ Extract JWT tokens from response
      const access = res.data.tokens.access;
      const refresh = res.data.tokens.refresh;

      // ✅ Store in browser
      localStorage.setItem("access_token", access);
      localStorage.setItem("refresh_token", refresh);

      // ✅ Redirect user to dashboard
      window.location.href = "/dashboard";
    } catch (err) {
      console.error("Login failed:", err);
      setError("Invalid username or password. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <h1 className="login-title">Welcome Back 👋</h1>
        <p className="login-subtitle">Sign in to continue to Placement Portal</p>

        {error && <p className="error">{error}</p>}

        <form onSubmit={handleLogin}>
          {/* Username Field */}
          <div className="input-group">
            <FaUser className="input-icon" />
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          {/* Password Field */}
          <div className="input-group">
            <FaLock className="input-icon" />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {/* Submit Button */}
          <button className="login-btn" type="submit" disabled={loading}>
            {loading ? <FaSpinner className="spinner" /> : "Login"}
          </button>
        </form>

        {/* Links */}
        <div className="extra-links">
          <a href="/forgot-password" className="forgot-link">
            Forgot Password?
          </a>
          <p>
            Don’t have an account?{" "}
            <a href="/signup" className="signup-link">
              Sign Up
            </a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;

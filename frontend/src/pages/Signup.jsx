import React, { useState } from "react";
import axios from "axios";
import { FaUser, FaEnvelope, FaLock, FaSpinner } from "react-icons/fa";
import "./Login.css";

const Signup = () => {
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  // ✅ Correct backend register API
  const REGISTER_URL = "http://127.0.0.1:8000/api/auth/register/";

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSignup = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    try {
      await axios.post(REGISTER_URL, form);

      setSuccess("✅ Account created successfully! Redirecting…");

      setTimeout(() => {
        window.location.href = "/login";
      }, 1500);
    } catch (err) {
      console.error(err);
      setError("Signup failed. Username or email may already exist.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <h1 className="login-title">Create Account</h1>
        <p className="login-subtitle">Sign up to continue</p>

        {error && <p className="error">{error}</p>}
        {success && <p className="success">{success}</p>}

        <form onSubmit={handleSignup}>

          <div className="input-group">
            <FaUser className="input-icon" />
            <input
              type="text"
              name="username"
              placeholder="Username"
              value={form.username}
              onChange={handleChange}
              required
            />
          </div>

          <div className="input-group">
            <FaEnvelope className="input-icon" />
            <input
              type="email"
              name="email"
              placeholder="Email Address"
              value={form.email}
              onChange={handleChange}
              required
            />
          </div>

          <div className="input-group">
            <FaLock className="input-icon" />
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={form.password}
              onChange={handleChange}
              required
            />
          </div>

          <button className="login-btn" type="submit" disabled={loading}>
            {loading ? <FaSpinner className="spinner" /> : "Sign Up"}
          </button>
        </form>

        <div className="extra-links">
          <p>
            Already have an account?{" "}
            <a href="/login" className="signup-link">
              Login
            </a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Signup;

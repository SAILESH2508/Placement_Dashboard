import React, { useState } from "react";
import axios from "axios";
import { FaEnvelope, FaSpinner } from "react-icons/fa";
import "./Login.css";

const ForgotPassword = () => {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  // ✅ Correct backend API
  const FORGOT_URL = "http://127.0.0.1:8000/api/auth/forgot-password/";

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");
    setLoading(true);

    try {
      // ✅ Always return generic “sent” message
      await axios.post(FORGOT_URL, { email });

      setMessage("✅ If the email exists, reset instructions were sent.");
    } catch (err) {
      // ✅ Same message on error (security best practice)
      setMessage("✅ If the email exists, reset instructions were sent.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <h1 className="login-title">Reset Password</h1>
        <p className="login-subtitle">Enter your email to receive reset link</p>

        {message && <p className="success">{message}</p>}

        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <FaEnvelope className="input-icon" />
            <input
              type="email"
              placeholder="Email Address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <button className="login-btn" type="submit" disabled={loading}>
            {loading ? <FaSpinner className="spinner" /> : "Send Reset Link"}
          </button>
        </form>

        <div className="extra-links">
          <a href="/login" className="forgot-link">
            Back to Login
          </a>
        </div>
      </div>
    </div>
  );
};

export default ForgotPassword;

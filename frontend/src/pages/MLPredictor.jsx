import React, { useState } from "react";
import Sidebar from "../components/Sidebar";
import API from "../api";
import "./MLPredictor.css";
import { FaBrain, FaChartLine, FaLightbulb, FaCheckCircle, FaTimesCircle } from "react-icons/fa";

const MLPredictor = () => {
  const [formData, setFormData] = useState({
    cgpa: "",
    internships: "",
    projects: "",
    communication: "",
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    setError("");
  };

  const handlePredict = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setPrediction(null);

    try {
      const response = await API.post("ml/predict/", {
        cgpa: parseFloat(formData.cgpa),
        internships: parseInt(formData.internships),
        projects: parseInt(formData.projects),
        communication: parseInt(formData.communication),
      });

      setPrediction(response.data);
    } catch (err) {
      setError(err.response?.data?.error || "Failed to get prediction. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const getRecommendations = () => {
    if (!prediction) return [];

    const recommendations = [];
    const { input_features } = prediction;

    if (input_features.cgpa < 7.0) {
      recommendations.push({
        icon: "📚",
        title: "Improve Academic Performance",
        desc: "Focus on improving your CGPA. Aim for at least 7.0+ for better placement opportunities.",
      });
    }

    if (input_features.internships < 2) {
      recommendations.push({
        icon: "💼",
        title: "Gain More Internship Experience",
        desc: "Try to complete at least 2-3 internships. They significantly boost your placement chances.",
      });
    }

    if (input_features.projects < 3) {
      recommendations.push({
        icon: "🚀",
        title: "Build More Projects",
        desc: "Work on 3-4 substantial projects. Showcase them on GitHub and your resume.",
      });
    }

    if (input_features.communication < 7) {
      recommendations.push({
        icon: "🗣️",
        title: "Enhance Communication Skills",
        desc: "Practice speaking, join clubs, participate in presentations to improve communication.",
      });
    }

    if (recommendations.length === 0) {
      recommendations.push({
        icon: "⭐",
        title: "Excellent Profile!",
        desc: "Your profile looks strong. Keep up the good work and prepare well for interviews.",
      });
    }

    return recommendations;
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return "#4caf50";
    if (confidence >= 0.6) return "#ff9800";
    return "#f44336";
  };

  return (
    <div className="page-container">
      <Sidebar />
      <div className="page-content">
        <div className="ml-predictor-content">
        <div className="ml-header">
          <FaBrain size={40} className="ml-icon" />
          <div>
            <h1>AI Placement Predictor</h1>
            <p>Get AI-powered insights on your placement probability</p>
          </div>
        </div>

        <div className="ml-content">
          {/* Input Form */}
          <div className="ml-card prediction-form">
            <h2>Enter Your Details</h2>
            <form onSubmit={handlePredict}>
              <div className="form-group">
                <label>
                  <FaChartLine /> CGPA (0-10)
                </label>
                <input
                  type="number"
                  name="cgpa"
                  step="0.01"
                  min="0"
                  max="10"
                  value={formData.cgpa}
                  onChange={handleChange}
                  placeholder="e.g., 8.5"
                  required
                />
                <small>Your cumulative grade point average</small>
              </div>

              <div className="form-group">
                <label>
                  💼 Number of Internships
                </label>
                <input
                  type="number"
                  name="internships"
                  min="0"
                  max="10"
                  value={formData.internships}
                  onChange={handleChange}
                  placeholder="e.g., 2"
                  required
                />
                <small>Total internships completed</small>
              </div>

              <div className="form-group">
                <label>
                  🚀 Number of Projects
                </label>
                <input
                  type="number"
                  name="projects"
                  min="0"
                  max="20"
                  value={formData.projects}
                  onChange={handleChange}
                  placeholder="e.g., 3"
                  required
                />
                <small>Substantial projects you've built</small>
              </div>

              <div className="form-group">
                <label>
                  🗣️ Communication Skills (1-10)
                </label>
                <input
                  type="number"
                  name="communication"
                  min="1"
                  max="10"
                  value={formData.communication}
                  onChange={handleChange}
                  placeholder="e.g., 8"
                  required
                />
                <small>Rate your communication abilities</small>
              </div>

              {error && <div className="error-message">{error}</div>}

              <button type="submit" className="predict-btn" disabled={loading}>
                {loading ? (
                  <>
                    <span className="spinner"></span> Analyzing...
                  </>
                ) : (
                  <>
                    <FaBrain /> Predict My Chances
                  </>
                )}
              </button>
            </form>
          </div>

          {/* Prediction Result */}
          {prediction && (
            <div className="ml-card prediction-result">
              <div className="result-header">
                {prediction.prediction === "Placed" ? (
                  <FaCheckCircle className="icon-success" size={50} />
                ) : (
                  <FaTimesCircle className="icon-warning" size={50} />
                )}
                <h2>{prediction.prediction}</h2>
              </div>

              {prediction.confidence && (
                <div className="confidence-section">
                  <h3>Confidence Score</h3>
                  <div className="confidence-bar-container">
                    <div
                      className="confidence-bar"
                      style={{
                        width: `${prediction.confidence * 100}%`,
                        backgroundColor: getConfidenceColor(prediction.confidence),
                      }}
                    >
                      <span>{(prediction.confidence * 100).toFixed(1)}%</span>
                    </div>
                  </div>
                  <p className="confidence-text">
                    {prediction.confidence >= 0.8
                      ? "High confidence - Strong profile!"
                      : prediction.confidence >= 0.6
                      ? "Moderate confidence - Good chances with improvements"
                      : "Lower confidence - Focus on skill development"}
                  </p>
                </div>
              )}

              <div className="feature-importance">
                <h3>Your Profile Summary</h3>
                <div className="features-grid">
                  <div className="feature-item">
                    <span className="feature-label">CGPA</span>
                    <span className="feature-value">{prediction.input_features.cgpa}</span>
                  </div>
                  <div className="feature-item">
                    <span className="feature-label">Internships</span>
                    <span className="feature-value">{prediction.input_features.internships}</span>
                  </div>
                  <div className="feature-item">
                    <span className="feature-label">Projects</span>
                    <span className="feature-value">{prediction.input_features.projects}</span>
                  </div>
                  <div className="feature-item">
                    <span className="feature-label">Communication</span>
                    <span className="feature-value">{prediction.input_features.communication}/10</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Recommendations */}
          {prediction && (
            <div className="ml-card recommendations">
              <h2>
                <FaLightbulb /> Personalized Recommendations
              </h2>
              <div className="recommendations-grid">
                {getRecommendations().map((rec, index) => (
                  <div key={index} className="recommendation-card">
                    <div className="rec-icon">{rec.icon}</div>
                    <h3>{rec.title}</h3>
                    <p>{rec.desc}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Model Info */}
          <div className="ml-card model-info">
            <h3>About the AI Model</h3>
            <div className="info-grid">
              <div className="info-item">
                <strong>Algorithm:</strong> Random Forest Classifier
              </div>
              <div className="info-item">
                <strong>Accuracy:</strong> 75%
              </div>
              <div className="info-item">
                <strong>Training Data:</strong> 200+ samples
              </div>
              <div className="info-item">
                <strong>Most Important Factor:</strong> Internships (36.5%)
              </div>
            </div>
            <p className="info-note">
              💡 This prediction is based on historical placement data and should be used as guidance only.
              Your actual placement depends on many factors including interview performance, company requirements, and market conditions.
            </p>
          </div>
        </div>
        </div>
      </div>
    </div>
  );
};

export default MLPredictor;

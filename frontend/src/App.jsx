import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useState } from "react";
import { FaRobot } from "react-icons/fa";

import Dashboard from "./pages/Dashboard";
import Students from "./pages/Students";
import Companies from "./pages/Companies";
import Placements from "./pages/Placements";
import Statistics from "./pages/Statistics";
import Notifications from "./pages/Notifications";
import MLPredictor from "./pages/MLPredictor";

import Login from "./pages/Login";
import Signup from "./pages/Signup";
import ForgotPassword from "./pages/ForgotPassword";

import PlacementAssistant from "./components/PlacementAssistant";
import ProtectedRoute from "./ProtectedRoute"; // ✅ Import once

import "./App.css";

function App() {
  const [showBot, setShowBot] = useState(false);

  return (
    <Router>
      {/* All Application Routes */}
      <Routes>

        {/* ✅ Public Auth Routes */}
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />

        {/* ✅ Protected Routes */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />

        <Route
          path="/students"
          element={
            <ProtectedRoute>
              <Students />
            </ProtectedRoute>
          }
        />

        <Route
          path="/companies"
          element={
            <ProtectedRoute>
              <Companies />
            </ProtectedRoute>
          }
        />

        <Route
          path="/placements"
          element={
            <ProtectedRoute>
              <Placements />
            </ProtectedRoute>
          }
        />

        <Route
          path="/statistics"
          element={
            <ProtectedRoute>
              <Statistics />
            </ProtectedRoute>
          }
        />

        <Route
          path="/notifications"
          element={
            <ProtectedRoute>
              <Notifications />
            </ProtectedRoute>
          }
        />

        <Route
          path="/ml-predictor"
          element={
            <ProtectedRoute>
              <MLPredictor />
            </ProtectedRoute>
          }
        />

      </Routes>

      {/* ✅ Floating Chatbot */}
      {showBot && <PlacementAssistant />}

      <button
        className="chatbot-floating-btn"
        onClick={() => setShowBot(!showBot)}
      >
        <FaRobot size={22} />
      </button>
    </Router>
  );
}

export default App;

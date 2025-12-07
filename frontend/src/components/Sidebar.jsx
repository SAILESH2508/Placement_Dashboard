import React from "react";
import { Link, useLocation } from "react-router-dom";

import {
  FaTachometerAlt,
  FaUserGraduate,
  FaBuilding,
  FaChartPie,
  FaChartBar,
  FaBell,
  FaSignOutAlt,
  FaMoon,
  FaSun,
  FaBrain
} from "react-icons/fa";

import { useTheme } from "../context/ThemeContext";
import "./Sidebar.css";

const Sidebar = () => {
  const location = useLocation();
  const { theme, toggleTheme } = useTheme();

  // ✅ Logout redirect
  const handleLogout = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  window.location.href = "/login";
};

  // ✅ Navigation items
  const navItems = [
    { path: "/dashboard", label: "Dashboard", icon: <FaTachometerAlt /> },
    { path: "/students", label: "Students", icon: <FaUserGraduate /> },
    { path: "/companies", label: "Companies", icon: <FaBuilding /> },
    { path: "/placements", label: "Placement Status", icon: <FaChartBar /> },
    { path: "/statistics", label: "Statistics", icon: <FaChartPie /> },
    { path: "/ml-predictor", label: "AI Predictor", icon: <FaBrain /> },
    { path: "/notifications", label: "Notifications", icon: <FaBell /> },
  ];

  return (
    <div className={`sidebar ${theme === "dark" ? "dark" : ""}`}>
      {/* HEADER */}
      <div className="sidebar-header">
        <h2>Placement Portal</h2>
      </div>

      {/* NAVIGATION */}
      <ul className="sidebar-menu">
        {navItems.map((item) => (
          <li
            key={item.path}
            className={location.pathname === item.path ? "active-link" : ""}
          >
            <Link to={item.path}>
              <span className="icon">{item.icon}</span>
              <span className="label">{item.label}</span>
            </Link>
          </li>
        ))}
      </ul>

      {/* THEME SWITCHER */}
      <div className="sidebar-footer">
        <button className="toggle-btn" onClick={toggleTheme}>
          {theme === "light" ? <FaMoon /> : <FaSun />}
          <span>{theme === "light" ? "Dark Mode" : "Light Mode"}</span>
        </button>

        {/* LOGOUT */}
        <button className="logout-btn" onClick={handleLogout}>
          <FaSignOutAlt className="icon" />
          <span>Logout</span>
        </button>
      </div>
    </div>
  );
};

export default Sidebar;

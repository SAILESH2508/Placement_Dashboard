import React, { useState, useMemo } from "react";
import Sidebar from "../components/Sidebar";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";
// Assuming you use the same CSS file for styling the main panels
import "./Dashboard.css"; 

// --- MOCK DATA ---
const DEPARTMENT_DATA = [
  { department: "AGRI", placed: 40 },
  { department: "AIML", placed: 45 },
  { department: "AUTO", placed: 32 },
  { department: "BT", placed: 25 },
  { department: "CHE", placed: 28 },
  { department: "CIVIL", placed: 20 },
  { department: "CSE", placed: 46 },
  { department: "DS", placed: 30 },
  { department: "ECE", placed: 20 },
  { department: "EEE", placed: 25 },
  { department: "FT", placed: 28 },
  { department: "IT", placed: 25 },
  { department: "MECH", placed: 30 },
];

const MONTHLY_DATA = [
  { month: "2025-01", placed: 40 },
  { month: "2025-02", placed: 42 },
  { month: "2025-03", placed: 42 },
  { month: "2025-04", placed: 32 },
  { month: "2025-05", placed: 45 },
  { month: "2025-06", placed: 35 },
  { month: "2025-07", placed: 34 },
  { month: "2025-08", placed: 33 },
  { month: "2025-09", placed: 30 },
  { month: "2025-10", placed: 48 },
  { month: "2025-11", placed: 10 },
];

const generateDailyMock = () => {
  const data = [];
  const today = new Date();
  for (let i = 29; i >= 0; i--) {
    const date = new Date(today);
    date.setDate(today.getDate() - i);
    data.push({
      date: date.toISOString().slice(5, 10), // MM-DD format
      placed: Math.floor(Math.random() * 10) + 5,
    });
  }
  return data;
};

const Statistics = () => {
  const [selectedYear, setSelectedYear] = useState("2025");
  
  // Use useMemo for guaranteed, stable daily trend data
  const dailyTrend = useMemo(() => generateDailyMock(), []);

  // Function to format XAxis labels for Monthly Chart
  const formatMonthlyTick = (tick) => {
    // Example: changes "2025-01" to "2025-01" or a shorter label
    return tick.slice(5);
  };

  return (
    <div className="page-container">
      <Sidebar />

      <main className="page-content">
        
        {/* Title and Selector */}
        <section className="section-block">
          <h1 className="page-title">Placement Statistics</h1>
          <div className="stats-controls">
            <label htmlFor="year-select">Select Year: </label>
            <select
              id="year-select"
              value={selectedYear}
              onChange={(e) => setSelectedYear(e.target.value)}
              className="year-selector"
            >
              <option value="2025">2025</option>
              <option value="2024">2024</option>
              {/* Add more years as needed */}
            </select>
          </div>
        </section>

        {/* --- CHARTS SECTION (GRID-2) --- */}
        <section className="section-block">
          <div className="grid-2">

            {/* 1. Department Chart */}
            <article className="panel chart-panel">
              <header className="panel-title">Department-wise Placements</header>
              <div className="chart-wrap">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={DEPARTMENT_DATA} margin={{ top: 20, right: 10, left: -20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} />
                    <XAxis dataKey="department" angle={-45} textAnchor="end" height={60} interval={0} />
                    <YAxis domain={[0, 60]} ticks={[15, 30, 45, 60]} />
                    <Tooltip />
                    <Bar dataKey="placed" fill="#2563eb" radius={[5, 5, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </article>

            {/* 2. Monthly Chart */}
            <article className="panel chart-panel">
              <header className="panel-title">Monthly Placements</header>
              <div className="chart-wrap">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={MONTHLY_DATA} margin={{ top: 20, right: 20, left: -20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} />
                    <XAxis dataKey="month" tickFormatter={formatMonthlyTick} />
                    <YAxis domain={[0, 60]} ticks={[15, 30, 45, 60]} />
                    <Tooltip />
                    <Line
                      type="monotone"
                      dataKey="placed"
                      stroke="#00C49F" // A different color for distinction
                      strokeWidth={2}
                      dot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </article>
          </div>
        </section>

        {/* --- DAILY CHART (FULL WIDTH) --- */}
        <section className="section-block">
            <article className="panel full-width-panel">
                <header className="panel-title">Daily Placements (Last 30 Days)</header>
                <div className="chart-wrap-large">
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={dailyTrend} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="date" />
                        <YAxis />
                        <Tooltip />
                        <Line type="monotone" dataKey="placed" stroke="#ffc658" strokeWidth={2} dot={false} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
            </article>
        </section>

      </main>
    </div>
  );
};

export default Statistics;
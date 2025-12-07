import React, { useEffect, useState, useMemo } from "react";
import Sidebar from "../components/Sidebar";
import API from "../api"; // Assuming this is defined correctly
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
import "./Dashboard.css";

// ✅ STATIC MOCK DATA DEFINITIONS
const DEMO_TOP_COMPANIES = [
  { name: "TechNova Solutions", offers: 45 },
  { name: "Global Digital", offers: 38 },
  { name: "Innovate AI", offers: 32 },
  { name: "Fusion Systems", offers: 25 },
  { name: "Quantum Corp", offers: 21 },
  { name: "Apex Consulting", offers: 18 },
  { name: "BlueSky Software", offers: 15 },
];

const DEMO_DEPT = [
  { department: "CSE", placed: 260 },
  { department: "IT", placed: 210 },
  { department: "ECE", placed: 180 },
  { department: "EEE", placed: 140 },
  { department: "MECH", placed: 130 },
  { department: "CIVIL", placed: 95 },
];

// New static data set for the Line Chart
const STATIC_DAILY_TREND = [
  { date: "2025-01-01", placed: 5 },
  { date: "2025-01-05", placed: 12 },
  { date: "2025-01-10", placed: 6 },
  { date: "2025-01-15", placed: 16 },
  { date: "2025-01-20", placed: 11 },
  { date: "2025-01-25", placed: 11 },
  { date: "2025-01-30", placed: 16 },
];

// Mock data for the Summary KPI block
const DEMO_SUMMARY = {
    total_students: 1250,
    total_companies: 90,
    total_placements: 600,
    avg_package_lpa: 7.25,
};


const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState({});
  const [summary, setSummary] = useState({});

  const [deptStats, setDeptStats] = useState([]);
  const [topCompanies, setTopCompanies] = useState([]);
  const [dailyTrend, setDailyTrend] = useState([]);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [meRes, summaryRes, deptRes, dailyRes, topRes] = await Promise.allSettled([
          API.get("auth/me/"),
          API.get("dashboard/summary/"),
          API.get("statistics/dept/?year=2025"),
          API.get("statistics/daily/?days=30"), // Added back the daily API call for comprehensive fallback
          API.get("companies/top/?limit=7"),
        ]);

        // ✅ USER (Falls back to 'USER' in JSX if API fails)
        if (meRes.status === "fulfilled") setUser(meRes.value.data);

        // ✅ SUMMARY (Falls back to DEMO_SUMMARY)
        if (summaryRes.status === "fulfilled" && summaryRes.value.data) {
          const s = summaryRes.value.data;
          setSummary({
            total_students: s.total_students || 0,
            total_companies: s.total_companies || 0,
            total_placements: s.total_placements || 0,
            avg_package_lpa: s.avg_package_lpa || 0,
          });
        } else {
            console.warn("Using fallback Summary Stats");
            setSummary(DEMO_SUMMARY);
        }

        // ✅ DEPARTMENT STATS (Falls back to DEMO_DEPT)
        if (deptRes.status === "fulfilled" && deptRes.value.data.results) {
          const list = deptRes.value.data.results || [];
          setDeptStats(
            list.map((d) => ({
              department: d.department,
              placed: d.placed,
            }))
          );
        } else {
          console.warn("Using fallback Dept Stats");
          setDeptStats(DEMO_DEPT);
        }

        // ✅ DAILY TREND (Falls back to STATIC_DAILY_TREND)
        if (dailyRes.status === "fulfilled" && dailyRes.value.data.results) {
          setDailyTrend(dailyRes.value.data.results || []);
        } else {
          console.warn("Using fallback Daily Trend");
          setDailyTrend(STATIC_DAILY_TREND);
        }

        // ✅ TOP COMPANIES (Falls back to DEMO_TOP_COMPANIES)
        if (topRes.status === "fulfilled" && topRes.value.data?.ranking) {
          const ranking = topRes.value.data?.ranking || [];
          const mapped = ranking.map((c) => ({
            name: c.company,
            offers: c.total_placements,
          }));
          setTopCompanies(mapped);
        } else {
          console.warn("Using fallback TOP COMPANIES");
          setTopCompanies(DEMO_TOP_COMPANIES);
        }
      } catch (err) {
        console.error("DASHBOARD LOAD ERROR: Full fallback triggered.", err);

        // ✅ CATCH-ALL FULL FALLBACK MODE (If Promise.allSettled fails completely)
        setSummary(DEMO_SUMMARY);
        setDeptStats(DEMO_DEPT);
        setDailyTrend(STATIC_DAILY_TREND);
        setTopCompanies(DEMO_TOP_COMPANIES);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  // Recalculate KPIs based on the final summary data (API or Mock)
  const kpis = useMemo(
    () => [
      { label: "Total Students", value: summary.total_students },
      { label: "Total Companies", value: summary.total_companies },
      { label: "Total Placements", value: summary.total_placements },
      {
        label: "Avg Package (LPA)",
        value: Number(summary.avg_package_lpa).toFixed(2),
      },
    ],
    [summary]
  );

  // ✅ Loading Screen
  if (loading) {
    return (
      <div className="page-container">
        <Sidebar />
        <main className="page-content">
          <div className="loading">Loading dashboard…</div>
        </main>
      </div>
    );
  }

  return (
    <div className="page-container">
      <Sidebar />
      <main className="page-content">
        
        {/* TITLE */}
        <section className="section-block">
          <h1 className="page-title">
            Welcome, {user.username?.toUpperCase() ?? "USER"} 👋 — Placement Dashboard
          </h1>
        </section>

        {/* --- KPI SECTION --- */}
        <section className="section-block">
          <div className="kpi-grid">
            {kpis.map((k) => (
              <article className="kpi-card" key={k.label}>
                <div className="kpi-value">{k.value}</div>
                <div className="kpi-label">{k.label}</div>
              </article>
            ))}
          </div>
        </section>

        {/* --- CHARTS SECTION --- */}
        <section className="section-block">
          <div className="grid-2">

            {/* DEPARTMENT CHART */}
            <article className="panel">
              <header className="panel-title">Department-wise Placements</header>
              <div className="chart-wrap">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={deptStats}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="department" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="placed" fill="#2563eb" radius={[8, 8, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </article>

            {/* DAILY TREND */}
            <article className="panel">
              <header className="panel-title">
                Daily Placements (Last 30 Days)
              </header>
              <div className="chart-wrap">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={dailyTrend}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Line
                      type="monotone"
                      dataKey="placed"
                      stroke="#4B7BE5"
                      strokeWidth={3}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </article>

          </div>
        </section>

        {/* --- TOP COMPANIES SECTION --- */}
        <section className="section-block">
          <article className="panel">
            <header className="panel-title">Top Hiring Companies</header>

            <ul className="top-list">
              {topCompanies.map((c) => (
                <li key={c.name} className="top-item">
                  <span className="top-name">{c.name}</span>
                  <span className="top-count">{c.offers} offers</span>
                </li>
              ))}
            </ul>
          </article>
        </section>

      </main>
    </div>
  );
};

export default Dashboard;
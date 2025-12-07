import React, { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import API from "../api";
import "./Placements.css";

const Placements = () => {
  const [placements, setPlacements] = useState([]);
  const [filtered, setFiltered] = useState([]);

  const [search, setSearch] = useState("");
  const [company, setCompany] = useState("All");
  const [status, setStatus] = useState("All");

  useEffect(() => {
    API.get("placements/")
      .then((res) => {
        // Handle paginated response from backend
        const data = res.data.results || res.data;
        setPlacements(data);
        setFiltered(data);
      })
      .catch(() => {
        // Fallback demo
        const demo = [
          { id: 1, student: { roll_no: "23CSE101" }, company: { name: "TCS" }, position: "Software Engineer", package_lpa: 3.6, confirmed: true },
          { id: 2, student: { roll_no: "23ECE402" }, company: { name: "Infosys" }, position: "Analyst", package_lpa: 4.2, confirmed: false },
        ];
        setPlacements(demo);
        setFiltered(demo);
      });
  }, []);

  useEffect(() => {
    let data = [...placements];

    if (search.trim() !== "") {
      data = data.filter((p) =>
        p.student.roll_no.toLowerCase().includes(search.toLowerCase()) ||
        p.company.name.toLowerCase().includes(search.toLowerCase())
      );
    }

    if (company !== "All") {
      data = data.filter((p) => p.company.name === company);
    }

    if (status !== "All") {
      data = data.filter((p) => (status === "Confirmed" ? p.confirmed : !p.confirmed));
    }

    setFiltered(data);
  }, [search, company, status, placements]);

  const companies = ["All", ...new Set(placements.map((p) => p.company.name))];

  return (
    <div className="page-container">
      <Sidebar />

      <div className="page-content">
        <h1 className="page-title">Placement Offers</h1>

        <div className="filters-row">
          <input
            type="text"
            placeholder="Search by roll / company..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />

          <select value={company} onChange={(e) => setCompany(e.target.value)}>
            {companies.map((c) => (
              <option key={c}>{c}</option>
            ))}
          </select>

          <select value={status} onChange={(e) => setStatus(e.target.value)}>
            <option>All</option>
            <option>Confirmed</option>
            <option>Pending</option>
          </select>
        </div>

        <table className="styled-table">
          <thead>
            <tr>
              <th>Roll No</th>
              <th>Company</th>
              <th>Position</th>
              <th>Package (LPA)</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((p) => (
              <tr key={p.id}>
                <td>{p.student.roll_no}</td>
                <td>{p.company.name}</td>
                <td>{p.position}</td>
                <td>{p.package_lpa}</td>
                <td className={p.confirmed ? "status-confirmed" : "status-pending"}>
                  {p.confirmed ? "Confirmed" : "Pending"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>

      </div>
    </div>
  );
};

export default Placements;

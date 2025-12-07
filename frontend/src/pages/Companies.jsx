import React, { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import API from "../api";
import "./Companies.css";

const Companies = () => {
  const [companies, setCompanies] = useState([]);
  const [filtered, setFiltered] = useState([]);

  const [search, setSearch] = useState("");
  const [location, setLocation] = useState("All");

  useEffect(() => {
    API.get("companies/")
      .then((res) => {
        // Handle paginated response from backend
        const data = res.data.results || res.data;
        setCompanies(data);
        setFiltered(data);
      })
      .catch(() => {
        // Fallback demo data
        const demo = [
          { id: 1, name: "TCS", location: "Chennai", recruiter_contact: "hr@tcs.com", website: "https://tcs.com" },
          { id: 2, name: "Infosys", location: "Bangalore", recruiter_contact: "hr@infosys.com", website: "https://infosys.com" },
        ];
        setCompanies(demo);
        setFiltered(demo);
      });
  }, []);

  useEffect(() => {
    let data = [...companies];

    if (search.trim() !== "") {
      data = data.filter((c) =>
        c.name.toLowerCase().includes(search.toLowerCase())
      );
    }

    if (location !== "All") {
      data = data.filter((c) => c.location === location);
    }

    setFiltered(data);
  }, [search, location, companies]);

  const locations = ["All", "Chennai", "Bangalore", "Hyderabad", "Pune", "Delhi", "Coimbatore"];

  return (
    <div className="page-container">
      <Sidebar />

      <div className="page-content">
        <h1 className="page-title">Companies</h1>

        {/* Filters */}
        <div className="filters-row">
          <input
            type="text"
            placeholder="Search companies..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />

          <select value={location} onChange={(e) => setLocation(e.target.value)}>
            {locations.map((loc) => (
              <option key={loc}>{loc}</option>
            ))}
          </select>
        </div>

        <table className="styled-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Location</th>
              <th>Contact</th>
              <th>Website</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((c) => (
              <tr key={c.id}>
                <td>{c.name}</td>
                <td>{c.location}</td>
                <td>{c.recruiter_contact}</td>
                <td>
                  <a href={c.website} target="_blank" rel="noreferrer">
                    Visit
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

      </div>
    </div>
  );
};

export default Companies;

import React, { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import API from "../api";
import "./Students.css";


const Students = () => {
  const [students, setStudents] = useState([]);
  const [filtered, setFiltered] = useState([]);

  const [search, setSearch] = useState("");
  const [branch, setBranch] = useState("All");
  const [year, setYear] = useState("All");
  const [sort, setSort] = useState("none");

  const BRANCHES = [
    "CSE", "IT", "ECE", "EEE", "MECH", "CIVIL",
    "AIDS", "AIML", "BT", "FT", "BME", "AGRI", "CHEM"
  ];

  useEffect(() => {
    API.get("students/")
      .then((res) => {
        // Handle paginated response from backend
        const data = res.data.results || res.data;
        setStudents(data);
        setFiltered(data);
      })
      .catch((err) => console.error("Error loading Students:", err));
  }, []);

  useEffect(() => {
    let data = [...students];

    // ✅ Search Filter
    if (search.trim() !== "") {
      data = data.filter((s) =>
        s.roll_no.toLowerCase().includes(search.toLowerCase()) ||
        s.branch.toLowerCase().includes(search.toLowerCase())
      );
    }

    // ✅ Branch Filter
    if (branch !== "All") {
      data = data.filter((s) => s.branch === branch);
    }

    // ✅ Year Filter
    if (year !== "All") {
      data = data.filter((s) => String(s.year) === year);
    }

    // ✅ Sorting
    if (sort === "cgpa") data.sort((a, b) => b.cgpa - a.cgpa);
    if (sort === "roll") data.sort((a, b) => a.roll_no.localeCompare(b.roll_no));

    setFiltered(data);
  }, [search, branch, year, sort, students]);

  return (
    <div className="page-container">
      <Sidebar />
      <div className="page-content">
        <h1>Students</h1>

        {/* ✅ Filters */}
        <div className="filters-row">
          <input
            type="text"
            placeholder="Search by roll/branch..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="search-input"
          />

          <select value={branch} onChange={(e) => setBranch(e.target.value)}>
            <option value="All">All Branches</option>
            {BRANCHES.map((b) => (
              <option key={b} value={b}>{b}</option>
            ))}
          </select>

          <select value={year} onChange={(e) => setYear(e.target.value)}>
            <option value="All">All Years</option>
            <option value="2">2nd Year</option>
            <option value="3">3rd Year</option>
            <option value="4">Final Year</option>
          </select>

          <select value={sort} onChange={(e) => setSort(e.target.value)}>
            <option value="none">Sort</option>
            <option value="cgpa">CGPA (High → Low)</option>
            <option value="roll">Roll Number (A → Z)</option>
          </select>
        </div>

        {/* ✅ Student Table */}
        <table className="styled-table">
          <thead>
            <tr>
              <th>Roll No</th>
              <th>Branch</th>
              <th>Year</th>
              <th>CGPA</th>
              <th>Resume</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((stu) => (
              <tr key={stu.roll_no}>
                <td>{stu.roll_no}</td>
                <td>{stu.branch}</td>
                <td>{stu.year}</td>
                <td>{stu.cgpa}</td>
                <td>
                  <a href={stu.resume_link} target="_blank" rel="noreferrer">
                    View Resume
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

export default Students;

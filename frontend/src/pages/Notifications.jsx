import React, { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import API from "../api";
import "./Notifications.css";

// Define the initial demo data outside the component
const initialDemoNotes = [
  { id: 1, title: "Placement Drive", message: "TCS drive starts tomorrow. All registered students must attend the briefing session.", pinned: true },
  { id: 2, title: "Results Released", message: "Infosys interview results posted. Check the career portal for your status.", pinned: false },
  { id: 3, title: "Career Workshop", message: "Workshop on 'Cracking the Coding Interview' scheduled for next Friday.", pinned: true },
];

const Notifications = () => {
  // Use the demo data as the initial state
  const [notes, setNotes] = useState(initialDemoNotes); 

  useEffect(() => {
    // Attempt to fetch real data from the API
    API.get("notifications/")
      .then((res) => {
        // Only update if the response data is a non-empty array
        if (Array.isArray(res.data) && res.data.length > 0) {
            setNotes(res.data);
        }
      })
      .catch((error) => {
        console.log("API fetch failed, displaying fallback demo data.", error);
      });
  }, []);

  return (
    <div className="page-container">
      <Sidebar />

      <div className="page-content">
        <h1 className="page-title">Notifications 🔔</h1>

        {/* Conditional rendering: Check if 'notes' is an array and has items */}
        {Array.isArray(notes) && notes.length > 0 ? (
          <div className="notif-list">
            {/* Sort pinned items to the top */}
            {notes
              .sort((a, b) => (b.pinned === a.pinned ? 0 : b.pinned ? 1 : -1))
              .map((n) => (
                <div key={n.id} className={`notif-card ${n.pinned ? "pinned" : ""}`}>
                  <h3>{n.title}</h3>
                  <p>{n.message}</p>
                  {/* Pinned Badge */}
                  {n.pinned && <span className="pin-badge">📌 PINNED</span>}
                </div>
              ))}
          </div>
        ) : (
          /* Display this message if 'notes' is empty or not an array */
          <div className="no-notifications-message">
            <h3>No new notifications at this time.</h3>
            <p>Please check back later.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Notifications;
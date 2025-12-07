import React, { useState } from "react";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

const Contact = () => {
  const [name, setName] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    alert(`Thanks ${name}! Your message has been sent.`);
    setName("");
    setMessage("");
  };

  return (
    <>
      <Navbar />
      <div className="page-container">
        <h2>Contact Us</h2>
        <form onSubmit={handleSubmit} className="form">
          <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Your Name" required />
          <textarea value={message} onChange={(e) => setMessage(e.target.value)} placeholder="Your Message" required></textarea>
          <button type="submit">Send</button>
        </form>
      </div>
      <Footer />
    </>
  );
};

export default Contact;

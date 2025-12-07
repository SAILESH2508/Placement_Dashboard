import React, { useState } from "react";
import "./PlacementAssistant.css";
import { FaPaperPlane, FaRobot } from "react-icons/fa";
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.REACT_APP_OPENAI_API_KEY,
  dangerouslyAllowBrowser: true
});

const PlacementAssistant = ({ useAI }) => {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hello! I'm your Placement Assistant 🤖\nAsk me anything about placements!" }
  ]);

  const [input, setInput] = useState("");
  const [typing, setTyping] = useState(false);

  // Enhanced local responses
  const localResponse = (msg) => {
    const t = msg.toLowerCase();

    // Greetings
    if (t.includes("hi") || t.includes("hello") || t.includes("hey")) {
      return "Hello! 👋 I'm your Placement Assistant.\n\nI can help you with:\n• Company information\n• Package details\n• Resume tips\n• Interview preparation\n• CGPA requirements\n\nWhat would you like to know?";
    }

    // Companies
    if (t.includes("company") || t.includes("companies") || t.includes("recruiter")) {
      return "🏢 We have 150+ recruiting companies including:\n\n• TCS, Infosys, Wipro\n• Amazon, Google, Microsoft\n• Zoho, Freshworks\n• Accenture, Cognizant\n\nVisit the Companies page for more!";
    }

    // Package/Salary
    if (t.includes("package") || t.includes("salary") || t.includes("ctc") || t.includes("lpa")) {
      return "💰 Placement Package Info:\n\n• Highest: ₹32 LPA\n• Average: ₹6-8 LPA\n• Common: ₹3.5-5 LPA\n\nPackages vary by company and role!";
    }

    // Resume
    if (t.includes("resume") || t.includes("cv")) {
      return "📄 Resume Tips:\n\n• Keep it 1-2 pages\n• Use ATS-friendly format\n• Highlight projects\n• Include technical skills\n• Quantify achievements\n\nNeed help? Contact placement cell!";
    }

    // Interview
    if (t.includes("interview") || t.includes("preparation")) {
      return "🎯 Interview Tips:\n\n• Practice coding daily\n• Know your projects well\n• Research the company\n• Be confident & honest\n• Prepare STAR stories\n\nGood luck! 🍀";
    }

    // CGPA
    if (t.includes("cgpa") || t.includes("marks") || t.includes("grade")) {
      return "📚 CGPA Requirements:\n\n• Most companies: 6.0+\n• Top companies: 7.0+\n• Dream companies: 8.0+\n\nRemember: Skills matter too!";
    }

    // Skills
    if (t.includes("skill") || t.includes("learn") || t.includes("technology")) {
      return "💻 Important Skills:\n\n• Programming: Java, Python\n• Web: React, Node.js\n• Database: SQL, MongoDB\n• Tools: Git, Docker\n\nFocus on depth over breadth!";
    }

    // Internship
    if (t.includes("internship") || t.includes("intern")) {
      return "🎓 Internship Tips:\n\n• Start early (2nd/3rd year)\n• Apply to multiple companies\n• Build LinkedIn profile\n• Complete 2-3 internships\n\nInternships boost placement chances!";
    }

    // Projects
    if (t.includes("project")) {
      return "🚀 Project Ideas:\n\n• Build full-stack web app\n• Create mobile app\n• Contribute to open source\n• Solve real problems\n• Deploy and showcase\n\nQuality > Quantity!";
    }

    // Help
    if (t.includes("help") || t.includes("what can")) {
      return "🤖 I can help with:\n\n✓ Companies & packages\n✓ Resume & interviews\n✓ CGPA requirements\n✓ Skills & projects\n✓ Statistics\n\nJust ask me anything!";
    }

    // Default
    return "I'm here to help! 😊\n\nAsk me about:\n• Companies & packages\n• Resume & interview tips\n• CGPA requirements\n• Skills & projects\n\nWhat would you like to know?";
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { sender: "me", text: input };
    const userInput = input;
    setMessages(prev => [...prev, userMsg]);
    setInput("");
    setTyping(true);

    let botReply = "";

    try {
      if (!useAI || !process.env.REACT_APP_OPENAI_API_KEY) {
        // Local mode (default)
        botReply = localResponse(userInput);
      } else {
        // AI mode
        try {
          const res = await client.chat.completions.create({
            model: "gpt-4o-mini",
            messages: [
              { role: "system", content: "You are a helpful placement assistant for engineering students. Provide concise, practical advice." },
              { role: "user", content: userInput }
            ],
            max_tokens: 200,
            temperature: 0.7
          });
          botReply = res.choices[0].message.content;
        } catch (error) {
          console.error("AI Error:", error);
          botReply = "⚠️ AI unavailable. Using local mode.\n\n" + localResponse(userInput);
        }
      }
    } catch (error) {
      console.error("Error:", error);
      botReply = "Sorry, I encountered an error. Please try again.";
    }

    // Typing animation delay
    setTimeout(() => {
      setMessages(prev => [...prev, { sender: "bot", text: botReply }]);
      setTyping(false);
    }, 800);
  };

  return (
    <div className="assistant-modern-box">
      <div className="assistant-header">
        <FaRobot size={20} />
        <span>Placement Assistant</span>
      </div>

      <div className="assistant-body">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`assistant-message ${msg.sender === "me" ? "me" : "bot"}`}
          >
            <div className="bubble">
              {msg.text.split('\n').map((line, i) => (
                <React.Fragment key={i}>
                  {line}
                  {i < msg.text.split('\n').length - 1 && <br />}
                </React.Fragment>
              ))}
            </div>
          </div>
        ))}

        {typing && (
          <div className="assistant-typing">
            <div className="dot"></div>
            <div className="dot"></div>
            <div className="dot"></div>
          </div>
        )}
      </div>

      <div className="assistant-input">
        <input
          type="text"
          placeholder="Ask something..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button onClick={sendMessage}>
          <FaPaperPlane />
        </button>
      </div>
    </div>
  );
};

export default PlacementAssistant;

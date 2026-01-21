import React, { useState } from "react";
import "./PlacementAssistant.css";
import { FaPaperPlane, FaRobot } from "react-icons/fa";
import OpenAI from "openai";

// Initialize OpenAI client safely
let client = null;
try {
  if (process.env.REACT_APP_OPENAI_API_KEY) {
    client = new OpenAI({
      apiKey: process.env.REACT_APP_OPENAI_API_KEY,
      dangerouslyAllowBrowser: true
    });
  }
} catch (error) {
  console.warn("OpenAI client failed to initialize:", error);
}

const SUGGESTION_CHIPS = [
  "Top Companies", "Package Details", "Resume Tips", "Interview Process",
  "HR Questions", "Aptitude Topics", "Dress Code", "Internship", "Contact"
];

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
      return "Hello! 👋 I'm your Placement Assistant.\n\nI can help you with:\n• Company information\n• Package details\n• Resume tips\n• Interview preparation\n• CGPA requirements\n\nTry clicking a suggestion chip below!";
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
      return "📄 Resume Tips:\n\n• Keep it 1-2 pages\n• Use ATS-friendly format (no columns/graphics)\n• Highlight 2-3 key projects\n• Include technical skills (Java, React, SQL)\n• Quantify achievements (e.g., 'Improved speed by 20%')\n\nNeed a review? Visit the placement cell!";
    }

    // Interview - Process
    if (t.includes("process") || t.includes("rounds")) {
      return "🔄 Standard Placement Process:\n\n1. Resume Shortlisting\n2. Aptitude/Coding Test (Online)\n3. Technical Interview 1 (Core/DSA)\n4. Technical Interview 2 (System Design/Projects)\n5. HR Interview (Behavioral)\n\nEach company may vary slightly!";
    }

    // Interview - General
    if (t.includes("interview") || t.includes("preparation")) {
      return "🎯 Interview Tips:\n\n• Practice coding daily (LeetCode/HackerRank)\n• Know your resume inside out\n• Research the company beforehand\n• Be confident & honest\n• Prepare 'STAR' stories for behavioral questions";
    }

    // HR Questions
    if (t.includes("hr") || t.includes("behavioral")) {
      return "🤝 Common HR Questions:\n\n• Tell me about yourself.\n• Why should we hire you?\n• What are your strengths and weaknesses?\n• Where do you see yourself in 5 years?\n• Describe a challenge you overcame.\n\nTip: Be positive and authentic!";
    }

    // Aptitude
    if (t.includes("aptitude") || t.includes("test")) {
      return "🧠 Aptitude Topics to Prepare:\n\n• Quantitative: Time & Work, Speed & Distance, Percentages, Probability\n• Logical: Blood Relations, Seating Arrangement, Coding-Decoding\n• Verbal: Reading Comprehension, Grammar\n\nDaily practice is key!";
    }

    // Dress Code
    if (t.includes("dress") || t.includes("wear") || t.includes("attire")) {
      return "👔 Interview Dress Code:\n\n• Men: Formal shirt (light color), formal trousers, formal shoes (polished), tie (optional).\n• Women: Formal shirt/trousers or Salwar Kameez, formal shoes.\n\nLook neat, shaved/groomed, and professional!";
    }

    // CGPA
    if (t.includes("cgpa") || t.includes("marks") || t.includes("grade")) {
      return "📚 CGPA Requirements:\n\n• Most companies: 6.0+\n• Top companies: 7.0+\n• Dream companies: 8.0+\n\nRemember: Skills matter too, but a good CGPA opens doors!";
    }

    // Skills
    if (t.includes("skill") || t.includes("learn") || t.includes("technology")) {
      return "💻 Important Skills:\n\n• Programming: Java, Python\n• Web: React, Node.js\n• Database: SQL, MongoDB\n• Tools: Git, Docker\n\nFocus on depth over breadth!";
    }

    // Internship
    if (t.includes("internship") || t.includes("intern")) {
      return "🎓 Internship Information:\n\nThird-year students are encouraged to apply for summer internships. Check the 'Notifications' tab for active drives. Internships often convert to full-time offers (PPO)!";
    }

    // Contact
    if (t.includes("contact") || t.includes("support")) {
      return "📞 Placement Cell Contact:\n\nEmail: placement@college.edu\nPhone: +91-1234567890\nLocation: Admin Block, 2nd Floor\n\nOffice Hours: 9 AM - 5 PM";
    }

    // Default
    return "I'm here to help! 😊\n\nAsk me about:\n• Companies & packages\n• Resume & interview tips\n• HR & Aptitude prep\n• Placement process\n\nOr click a suggestion chip below!";
  };

  const handleChipClick = (text) => {
    setInput(text);
    // Optional: Auto-send on click
    // sendMessage(text); // Need to refactor sendMessage to accept arg
    // For now, let's just set input. Or we can refactor sendMessage.
    // Let's refactor sendMessage slightly to support direct calls.
    sendMessage(text);
  };

  const sendMessage = async (overrideInput = null) => {
    const textToSend = overrideInput || input;
    if (!textToSend.trim()) return;

    const userMsg = { sender: "me", text: textToSend };
    setMessages(prev => [...prev, userMsg]);
    setInput("");
    setTyping(true);

    let botReply = "";

    try {
      if (!useAI || !process.env.REACT_APP_OPENAI_API_KEY) {
        // Local mode (default)
        botReply = localResponse(textToSend);
      } else {
        // AI mode
        try {
          const res = await client.chat.completions.create({
            model: "gpt-4o-mini",
            messages: [
              { role: "system", content: "You are a helpful placement assistant for engineering students. Provide concise, practical advice." },
              { role: "user", content: textToSend }
            ],
            max_tokens: 200,
            temperature: 0.7
          });
          botReply = res.choices[0].message.content;
        } catch (error) {
          console.error("AI Error:", error);
          botReply = "⚠️ AI unavailable. Using local mode.\n\n" + localResponse(textToSend);
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
    }, 600);
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

      {/* Suggestion Chips */}
      <div className="suggestion-chips">
        {SUGGESTION_CHIPS.map((chip) => (
          <div key={chip} className="chip" onClick={() => handleChipClick(chip)}>
            {chip}
          </div>
        ))}
      </div>

      <div className="assistant-input">
        <input
          type="text"
          placeholder="Ask something..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button onClick={() => sendMessage()}>
          <FaPaperPlane />
        </button>
      </div>
    </div>
  );
};

export default PlacementAssistant;

import React, { useState, useRef } from "react";
import { DeepgramClient } from "@deepgram/sdk";

const VoiceAgent: React.FC = () => {
  const [status, setStatus] = useState<"idle" | "connecting" | "active">("idle");
  const dgConnectionRef = useRef<any>(null);

  const startConversation = async () => {
    try {
      setStatus("connecting");
      
      // 1. Initialize Client (Use your API Key)
      const deepgram = new DeepgramClient("YOUR_DEEPGRAM_API_KEY");

      // 2. Connect to the Voice Agent
      const connection = deepgram.agent.v("1").connect();
      dgConnectionRef.current = connection;

      connection.on("open", () => {
        setStatus("active");
        console.log("Connected to Deepgram");

        // 3. Send Settings to link your Backend
        connection.send(JSON.stringify({
          type: "Settings",
          agent: {
            think: {
              provider: { type: "open_ai" },
              endpoint: {
                // Change this to your public ngrok or production URL
                url: "https://your-backend-url.ngrok-free.app/v1/chat/completions"
              }
            },
            speak: {
              model: "aura-asteria-en"
            }
          }
        }));
      });

      connection.on("error", (err: any) => {
        console.error("Deepgram Error:", err);
        setStatus("idle");
      });

      connection.on("close", () => {
        setStatus("idle");
      });

    } catch (error) {
      console.error("Failed to start:", error);
      setStatus("idle");
    }
  };

  const stopConversation = () => {
    if (dgConnectionRef.current) {
      dgConnectionRef.current.finish();
      dgConnectionRef.current = null;
    }
    setStatus("idle");
  };

  return (
    <div style={containerStyle}>
      <h1>Agentic Voice Assistant</h1>
      <p>Status: <strong>{status.toUpperCase()}</strong></p>
      
      {status === "idle" ? (
        <button onClick={startConversation} style={startBtn}>Start Conversation</button>
      ) : (
        <button onClick={stopConversation} style={stopBtn}>End Call</button>
      )}
    </div>
  );
};

// Simple Styles
const containerStyle: React.CSSProperties = { padding: "40px", textAlign: "center", fontFamily: "sans-serif" };
const startBtn = { padding: "12px 24px", backgroundColor: "#00cc66", color: "#fff", border: "none", borderRadius: "8px", cursor: "pointer" };
const stopBtn = { padding: "12px 24px", backgroundColor: "#ff4d4d", color: "#fff", border: "none", borderRadius: "8px", cursor: "pointer" };

export default VoiceAgent;
import { useEffect, useRef, useState } from "react";

export interface Message {
  role: "user" | "agent";
  text: string;
}

export function useVoiceWebSocket() {
  const ws = useRef<WebSocket | null>(null);

  const [messages, setMessages] = useState<Message[]>([]);
  const [status, setStatus] = useState("disconnected");

  useEffect(() => {
    ws.current = new WebSocket("ws://localhost:8000/voice-agent");

    ws.current.onopen = () => {
      setStatus("listening");
    };

    ws.current.onmessage = async (event) => {
      const data = JSON.parse(event.data);

      if (data.text) {
        setMessages((prev) => [
          ...prev,
          { role: "agent", text: data.text },
        ]);

        const audio = new Audio(`http://localhost:8000/${data.audio}`);
        audio.play();

        setStatus("speaking");
        audio.onended = () => setStatus("listening");
      }
    };

    ws.current.onclose = () => {
      setStatus("disconnected");
    };

    return () => {
      ws.current?.close();
    };
  }, []);

  const sendAudio = (chunk: Blob) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(chunk);
    }
  };

  return { messages, status, sendAudio };
}
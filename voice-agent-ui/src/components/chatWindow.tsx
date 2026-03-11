import type { Message } from "../hooks/useVoiceWebsocket";

interface Props {
  messages: Message[];
}

export default function ChatWindow({ messages }: Props) {
  return (
    <div style={{ height: "400px", overflowY: "auto", border: "1px solid #ddd", padding: "10px" }}>
      {messages.map((m, i) => (
        <div key={i} style={{ marginBottom: "10px" }}>
          <b>{m.role === "user" ? "You" : "Agent"}:</b> {m.text}
        </div>
      ))}
    </div>
  );
}
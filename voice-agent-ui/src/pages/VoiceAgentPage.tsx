import { useState } from "react";
import ChatWindow from "../components/chatWindow";
import MicButton from "../components/MicButton";
import StatusIndicator from "../components/StatusIndicator";
import { useVoiceWebSocket } from "../hooks/useVoiceWebsocket";
import { useMicrophone } from "../hooks/useMicrophone";

export default function VoiceAgentPage() {
  const { messages, status, sendAudio } = useVoiceWebSocket();

  const { start, stop } = useMicrophone(sendAudio);

  const [recording, setRecording] = useState(false);

  const handleStart = () => {
    start();
    setRecording(true);
  };

  const handleStop = () => {
    stop();
    setRecording(false);
  };

  return (
    <div style={{ width: "500px", margin: "50px auto", textAlign: "center" }}>
      <h1>Voice Assistant</h1>

      <StatusIndicator status={status} />

      <ChatWindow messages={messages} />

      <MicButton
        recording={recording}
        onStart={handleStart}
        onStop={handleStop}
      />
    </div>
  );
}
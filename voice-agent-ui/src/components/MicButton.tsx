interface Props {
  onStart: () => void;
  onStop: () => void;
  recording: boolean;
}

export default function MicButton({ onStart, onStop, recording }: Props) {
  return (
    <button
      onClick={recording ? onStop : onStart}
      style={{
        padding: "10px 20px",
        fontSize: "18px",
        marginTop: "20px",
      }}
    >
      {recording ? "Stop Mic 🎤" : "Start Mic 🎤"}
    </button>
  );
}
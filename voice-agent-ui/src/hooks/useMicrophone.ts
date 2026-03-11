import { useRef } from "react";

export function useMicrophone(onChunk: (chunk: Blob) => void) {
  const mediaRecorder = useRef<MediaRecorder | null>(null);

  const start = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    mediaRecorder.current = new MediaRecorder(stream, {
      mimeType: "audio/webm"
    });

    mediaRecorder.current.ondataavailable = (e) => {
      if (e.data.size > 0) {
        onChunk(e.data);
      }
    };

    mediaRecorder.current.start(250);
  };

  const stop = () => {
    mediaRecorder.current?.stop();
  };

  return { start, stop };
}
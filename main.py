from fastapi import WebSocket, FastAPI
from workflows.graph_builder import graph
from services.speech_service import speech_service, tts_service

app = FastAPI()


import uuid

def create_thread():
    return str(uuid.uuid4())


@app.websocket("/voice-agent")
async def voice_agent(ws: WebSocket):

    await ws.accept()

    thread_id = None

    while True:

        audio_chunk = await ws.receive_bytes()

        text = speech_service.transcribe_chunk(audio_chunk)

        if speech_service.is_final():

            if thread_id is None:
                thread_id = create_thread()

            result = graph.invoke(
                {"user_input_text": text},
                config={"configurable": {"thread_id": thread_id}}
            )

            response_text = result["agent_response"]

            audio = tts_service.speak(response_text)

            await ws.send_json({
                "thread_id": thread_id,
                "text": response_text,
                "audio": audio,
                "status": result.get("status")
            })
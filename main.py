from fastapi import WebSocket, FastAPI, WebSocketDisconnect
from workflows.graph_builder import graph
from services.speech_service import speech_service, tts_service
import logging

logger = logging.getLogger(__name__)


app = FastAPI()


import uuid

def create_thread():
    return str(uuid.uuid4())


@app.websocket("/voice-agent")
async def voice_agent(ws: WebSocket):

    await ws.accept()

    thread_id = None

    try:

        # initialize streaming STT
        await speech_service.connect()

        while True:

            # receive audio from client
            audio_chunk = await ws.receive_bytes()

            # send audio to Deepgram
            await speech_service.send_audio(audio_chunk)

            # check if speech finished
            text = await speech_service.get_final_transcript()

            if not text:
                continue

            logger.info("User transcript: %s", text)

            # create session if first interaction
            if thread_id is None:
                thread_id = create_thread()

            # run agent graph
            result_state = graph.invoke(
                {"user_input_text": text},
                config={"configurable": {"thread_id": thread_id}}
            )

            response_text = result_state.get("agent_response")

            if not response_text:
                response_text = "I couldn't process that request."

            # generate voice response
            audio_path = tts_service.speak(response_text)

            # send response to client
            await ws.send_json({
                "thread_id": thread_id,
                "text": response_text,
                "audio": audio_path,
                "status": result_state.get("status")
            })

    except WebSocketDisconnect:
        logger.info("Client disconnected")

    except Exception as e:
        logger.exception("Voice agent error")

        await ws.send_json({
            "error": "Internal server error"
        })

    finally:
        await speech_service.close()
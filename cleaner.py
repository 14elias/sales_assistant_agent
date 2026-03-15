import os
import time


def cleanup_audio(folder='audio_responses', max_age=3600):
    now = time.time()
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if os.path.isfile(path) and now - os.path.getmtime(path) > max_age:
            os.remove(path)

def cleanup_logs(folder='logs', max_age=3600):
    now = time.time()
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if os.path.isfile(path) and now - os.path.getmtime(path) > max_age:
            os.remove(path)

if __name__ == '__main__':
    cleanup_logs()
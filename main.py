import time

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from IPython import embed
from playsound import playsound

from aws_lib import mood_detector, polly

if __name__ == "__main__":
    patterns = ["*.txt", "*.png", "*.jpg", "*.jpeg"]
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(
        patterns=patterns,
        ignore_patterns=ignore_patterns,
        ignore_directories=ignore_directories,
        case_sensitive=case_sensitive,
    )

    def on_created(event):
        resp = mood_detector.detect(event.src_path)
        emotions = resp["FaceDetails"][0]["Emotions"]
        most_accurate_emotion = max(emotions, key=lambda x: x["Confidence"])
        emotion = most_accurate_emotion["Type"]
        file = polly.create_speech(f"I detected a {emotion} person")
        playsound(file)

    my_event_handler.on_created = on_created

    path = "/Users/mrayco/Pictures/Photo Booth Library/Pictures/"
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join

import uuid

import boto3

polly_client = boto3.client("polly")


def create_speech(text: str) -> str:
    print("generating audio file")
    resp = polly_client.synthesize_speech(
        VoiceId="Joanna", OutputFormat="mp3", Text=text
    )
    audio_name = f"audio/{uuid.uuid4()}.mp3"
    file = open(audio_name, "wb")
    file.write(resp["AudioStream"].read())
    file.close()
    return audio_name

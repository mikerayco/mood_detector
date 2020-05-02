import io

from PIL import Image
import boto3

rekognition = boto3.client("rekognition")


def detect(image_dir: str) -> str:
    print("analyzing image")
    stream = io.BytesIO()
    image = Image.open(image_dir)
    image.save(stream, format="jpeg")
    image_binary = stream.getvalue()

    response = rekognition.detect_faces(
        Attributes=["ALL"], Image={"Bytes": image_binary}
    )
    return response

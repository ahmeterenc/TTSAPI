from flask import Flask, request, Response
from gtts import gTTS
import io
app = Flask(__name__)


@app.route("/tts", methods=["POST"])
def tts():
    text = request.json["text"]
    # gTTS kullanarak metni ses dosyasına dönüştürün
    tts = gTTS(text, lang="tr")

    # Ses dosyasını byte array'e dönüştürün
    wav_data = io.BytesIO()
    tts.write_to_fp(wav_data)
    wav_data.seek(0)

    # Byte array'i response body'de gönderin
    response = Response(wav_data.getvalue(), mimetype="audio/wav")
    response.headers["Content-Length"] = len(wav_data.getvalue())
    return response


if __name__ == "__main__":
    app.run()

import uuid

from flask import Flask, request, Response
from gtts import gTTS

app = Flask(__name__)


@app.route("/tts", methods=["POST"])
def tts():
    text = request.json["text"]

    tts = gTTS(text, lang="tr")

    filename = f"{uuid.uuid4()}.mp3"  # Benzersiz bir dosya adı oluşturuyoruz
    with open(f"static/{filename}", "wb") as f:
        tts.write_to_fp(f)

    return {"filename": filename}  # Oluşturulan dosya adını döndürüyoruz


@app.route("/get_tts", methods=["GET"])
def get_tts():
    filename = request.args["filename"]  # Dosya adını parametre olarak aldık

    try:
        with open(f"static/{filename}", "rb") as f:
            wav_data = f.read()
    except FileNotFoundError:
        return {"error": "Dosya bulunamadı."}, 404

    response = Response(wav_data, mimetype="audio/mp3")
    response.headers["Content-Length"] = len(wav_data)
    return response


if __name__ == "__main__":
    app.run()

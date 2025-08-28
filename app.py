from flask import Flask, render_template, request, jsonify
import requests
import os  # ✅ Import os for reading environment variables

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "en",   # source language
            "tl": "es",   # target language
            "dt": "t",
            "q": text,
        }

        response = requests.get(url, params=params, verify=False)
        result = response.json()

        # ✅ Safely join translated chunks with spaces
        translated_text = " ".join([item[0] for item in result[0] if item[0]])

        return jsonify({"translated_text": translated_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # ✅ Now supports local run + deployment
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)

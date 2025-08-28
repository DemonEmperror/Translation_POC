from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    texts = data.get("text", {})
    target_lang = data.get("target_lang", "es")

    if not texts:
        return jsonify({"error": "No text provided"}), 400

    translated = {}
    try:
        for key, text in texts.items():
            if not text:
                translated[key] = ""
                continue

            url = "https://translate.googleapis.com/translate_a/single"
            params = {
                "client": "gtx",
                "sl": "auto",   # detect source automatically
                "tl": target_lang,  # target language comes from frontend
                "dt": "t",
                "q": text,
            }

            response = requests.get(url, params=params, verify=False)
            result = response.json()

            # ✅ Join translated chunks
            translated_text = " ".join([item[0] for item in result[0] if item[0]])
            translated[key] = translated_text

        return jsonify({"translated_text": translated})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # ✅ Works locally and in deployment
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8081)), debug=True)

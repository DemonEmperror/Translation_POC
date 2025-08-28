from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json(force=True)
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
                "sl": "auto",     # auto detect
                "tl": target_lang,
                "dt": "t",
                "q": text,
            }

            response = requests.get(url, params=params, timeout=10)
            result = response.json()

            # ✅ Defensive parsing
            if result and isinstance(result, list) and len(result) > 0:
                chunks = []
                for item in result[0]:
                    if isinstance(item, list) and item[0]:
                        chunks.append(item[0])
                translated_text = " ".join(chunks)
            else:
                translated_text = text  # fallback = original text

            translated[key] = translated_text

        return jsonify({"translated_text": translated})

    except Exception as e:
        # ✅ Add debugging info in logs
        import traceback
        print("ERROR in /translate:", traceback.format_exc())
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # ✅ Works locally and in deployment
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8081)), debug=True)

from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


def normalizeTitle(s):
    if s == "library":
        return "libraries"
    elif s in {"file", "model"}:
        return s + "s"
    else:
        return s


@app.route("/extract", methods=["GET"])
def extract_data():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    try:
        # Fetch the HTML page
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        # Parse the HTML content
        soup = BeautifulSoup(html_content, "html.parser")
        parent = soup.find("h5", string="Stats").parent

        stats = {}
        for element in parent.find_all("li"):
            count, title = element.text.split()
            stats[normalizeTitle(title.lower())] = int(count)

        # Return the extracted data as JSON
        return jsonify({"url": url, "stats": stats})

    except requests.RequestException as e:
        return jsonify({"error": f"Failed to fetch the URL: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

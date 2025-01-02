from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/extract', methods=['GET'])
def extract_data():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL parameter is required'}), 400

    try:
        # Fetch the HTML page
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        stats = soup.find('h5', string = "Stats")
        ul = stats.next_sibling
        while ul and ul.name is None:
            ul = ul.next_sibling

        # Extract the stats
        stats = {}
        for li in ul.children:
            if li.name != 'li':
                continue
            li = li.text.split(' ')
            print(li)
            if li[1].lower().startswith('librar'):
                stats['libraries'] = li[0]
            elif li[1].lower().startswith('model'):
                stats['models'] = li[0]
            elif li[1].lower().startswith('file'):
                stats['files'] = li[0]
        
        # Return the extracted data as JSON
        return jsonify({'url': url, 'stats': stats})
    
    except requests.RequestException as e:
        return jsonify({'error': f'Failed to fetch the URL: {e}'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

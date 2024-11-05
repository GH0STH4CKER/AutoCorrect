from flask import Flask, request, jsonify
from requests import get
from bs4 import BeautifulSoup
import fake_useragent

app = Flask(__name__)

@app.route('/spellcheck', methods=['GET'])
def spell_check():
    word = request.args.get('word')

    if word:
        return jsonify({"message": "Missing parameter: word"})

    try:
        ua = fake_useragent.UserAgent()
        res = get(f'https://www.google.com/search?q={word}', headers={'User-Agent': ua.random})
    except Exception as e:
        return jsonify({"error": str(e)})
    
    if res.ok:
        soup = BeautifulSoup(res.text, 'html.parser')
        target_a = soup.find('a', id='fprsl')
        if target_a:
            suggestion = target_a.text
            return jsonify({"message": f"Do you mean {suggestion}?"})
        else:
            return jsonify({"message": "Word is correct"})
    else:
        return jsonify({"error": f"HTTP Error: {res.status_code}"})


if __name__ == '__main__':
    app.run(debug=True)

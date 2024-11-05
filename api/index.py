from flask import Flask, request, jsonify, render_template_string
from requests import get
from bs4 import BeautifulSoup
import fake_useragent

app = Flask(__name__)

# HTML template as a string with embedded CSS
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spell Checker</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: #333;
        }
        .container {
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            padding: 20px;
            width: 300px;
            text-align: center;
        }
        h1 {
            font-size: 24px;
            margin-bottom: 20px;
        }
        label {
            font-size: 14px;
            margin-bottom: 10px;
            display: block;
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            padding: 10px 15px;
            background-color: #007BFF;
            color: #fff;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #0056b3;
        }
        #result {
            margin-top: 20px;
            font-size: 16px;
            color: #007BFF;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Spell Checker</h1>
        <form action="/ACSC" method="get">
            <label for="word">Enter a word:</label>
            <input type="text" id="word" name="word" required>
            <button type="submit">Check Spelling</button>
        </form>
        <div id="result"></div>
    </div>
    <script>
        const form = document.querySelector('form');
        const resultDiv = document.getElementById('result');

        form.addEventListener('submit', async (event) => {
            event.preventDefault(); // Prevent form submission

            const formData = new FormData(form);
            const word = formData.get('word');

            const response = await fetch(`/ACSC?word=${word}`);
            const data = await response.json();

            if (response.ok) {
                resultDiv.textContent = data.message;
            } else {
                resultDiv.textContent = `Error: ${data.error}`;
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/ACSC', methods=['GET'])
def spell_check():
    word = request.args.get('word')

    if not word:  # Check if the word parameter is provided
        return jsonify({"error": "Missing parameter: word"}), 400

    try:
        ua = fake_useragent.UserAgent()
        res = get(f'https://www.google.com/search?q={word}', headers={'User-Agent': ua.random})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    if res.ok:
        soup = BeautifulSoup(res.text, 'html.parser')
        target_a = soup.find('a', id='fprsl')
        if target_a:
            suggestion = target_a.text
            return jsonify({"message": f"Do you mean {suggestion}?"})
        else:
            return jsonify({"message": "Word is correct"})
    else:
        return jsonify({"error": f"HTTP Error: {res.status_code}"}), res.status_code

if __name__ == '__main__':
    app.run(debug=True)

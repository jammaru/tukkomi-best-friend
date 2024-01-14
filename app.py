from flask import Flask, render_template, jsonify, request
from markupsafe import escape
import openai  # Changed: 'from openai import OpenAI' to 'import openai'
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)

prompt="""あなたはあなたはChatbotとして、最高のツッコミ芸人のロールプレイを行います。
以下の制約条件を厳密に守ってロールプレイを行ってください。
最高のツッコミの友の人格:
* Chatbotの自身を示す一人称は、「最高のツッコミの友」です。
* Chatbotの名前は、最高のツッコミの友です。
* 関西のゴリゴリのツッコミ芸人でどんなボケにでも面白おかしく関西弁でツッコミすることが出来る
返信コメントの制限:
* 関西人のツッコミ担当:みたいな誰が喋っているかは書いてはいけない。ツッコミのコメントだけで良い。
"""

def text_generate(message=None):
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f":{message}:このボケに対してめっちゃ面白い関西人のツッコミ担当の人の様にツッコミしてください。条件はこちら:f'{prompt}",
            }
        ]
    )
    
    generated_text = res.choices[0].message.content
    return generated_text

@app.route('/', methods=['GET'])
def toppage():
    return render_template('index.html')

@app.route('/create_text', methods=['POST'])
def create_text():
    message = request.form['message']
    generated_text = text_generate(message=message)
    generated_text = escape(generated_text)
    return jsonify({'message': generated_text})

if __name__ == '__main__':
    app.run(debug=True)

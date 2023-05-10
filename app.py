import openai
from flask import Flask, request
from backend import main

OPENAI_API_KEY = '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'
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

@app.route('/genNaiveAssert',  methods=['POST'])
def genNaiveAssert():
    code = request.json['code']
    codeExtension = request.json['code_extension']

    message = main(code, codeExtension)
    print(message)
    response = openai.ChatCompletion.create(
               model="gpt-3.5-turbo",
               messages=[{"role": "system", "content": ""},
                         {"role": "user", "content": message}],
               temperature=0,
               max_tokens=1023,
               presence_penalty=-0.5,
               n=1)
    op = response.choices[0].message.content
    return op

@app.route('/genFewShotAssert',  methods=['POST'])
def genFewShotAssert():
    code = request.json['code']
    codeExtension = request.json['code_extension']

    message = main(code, codeExtension, "yes")
    print(message)
    response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": ""},
                          {"role": "user", "content": message}],
                temperature=0,
                max_tokens=1023,
                presence_penalty=-0.5,
                n=1)
    op = response.choices[0].message.content
    return op

if __name__ == '__main__':
    app.run(debug=True)

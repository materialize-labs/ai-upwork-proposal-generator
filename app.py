from flask import Flask, request

app = Flask(__name__)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    print(f"Authorization Code: {code}")
    return "Authorization code received, please check the console."

if __name__ == '__main__':
    app.run(port=3000)
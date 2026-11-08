from helpers.aplication import app

@app.route("/")
def index():
    return {"version": "1.0.0"}, 200

@app.route("/health")
def health():
    return {"status": "OK"}, 200
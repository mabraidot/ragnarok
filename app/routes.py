from app import app

@app.route("/")
@app.route("/index")
def home():
    return "The Ragnarök is coming ..."
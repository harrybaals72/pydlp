from routes import app
from processes import start_loop

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5353)
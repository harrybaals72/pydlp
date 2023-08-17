import os
import sys
from routes import app

def main():
    port = os.environ.get('PORT')
    if port is None:
        print("Environment variable not set.")
        sys.exit(1)

    app.run(debug=True, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
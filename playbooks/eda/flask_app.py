from flask import Flask
import os
import time

app = Flask(__name__)

# Global state to control health (can be toggled via env var or signal)
HEALTH_FILE = '/tmp/flask_health.txt'

def get_health_state():
    try:
        with open(HEALTH_FILE, 'r') as f:
            return f.read().strip()
    except:
        return 'healthy'

@app.route('/health')
def health():
    state = get_health_state()
    if state == 'healthy':
        return {'status': 'healthy', 'timestamp': time.time()}, 200
    else:
        return {'status': 'unhealthy', 'timestamp': time.time()}, 500

@app.route('/metrics')
def metrics():
    # Simple metrics endpoint for Prometheus
    return '''# HELP flask_health Flask health status
# TYPE flask_health gauge
flask_health{status="''' + get_health_state() + '''"} 1
''', 200

if __name__ == '__main__':
    # Write initial health state
    with open(HEALTH_FILE, 'w') as f:
        f.write('healthy')
    
    print("Flask app starting on 0.0.0.0:5000")
    print(f"Health state: {get_health_state()}")
    app.run(host='0.0.0.0', port=5000, debug=False)
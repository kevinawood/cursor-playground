import os
import gc
from app import app

# Memory optimization settings
gc.set_threshold(700, 10, 10)  # More aggressive garbage collection

# Set environment variables for production
os.environ['FLASK_ENV'] = 'production'
os.environ['FLASK_DEBUG'] = '0'

# Configure for Railway
port = int(os.environ.get('PORT', 5001))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False) 
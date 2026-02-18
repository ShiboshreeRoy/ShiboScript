#!/usr/bin/env python3
"""
Simple test script for advanced ShiboScript features
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Test basic imports
    import psutil
    import bcrypt
    import qrcode
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from bs4 import BeautifulSoup
    import psycopg2
    import pymongo
    import redis
    
    print("✅ All required packages imported successfully!")
    
    # Test basic functionality
    print("Testing basic functionality...")
    
    # Test psutil
    cpu_percent = psutil.cpu_percent(interval=1)
    print(f"CPU Usage: {cpu_percent}%")
    
    # Test bcrypt
    password = b"test_password"
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    is_valid = bcrypt.checkpw(password, hashed)
    print(f"Password hashing works: {is_valid}")
    
    # Test UUID generation
    import uuid
    test_uuid = str(uuid.uuid4())
    print(f"Generated UUID: {test_uuid}")
    
    # Test system info
    import platform
    print(f"Platform: {platform.platform()}")
    
    print("✅ All tests passed!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install required packages:")
    print("pip3 install --break-system-packages psutil bcrypt qrcode matplotlib numpy pandas beautifulsoup4 psycopg2-binary pymongo redis")
except Exception as e:
    print(f"❌ Error: {e}")
"""
Test database connection with the correct password
"""
import os
import sys

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_connection():
    """Test database connection with the correct password"""
    try:
        from sqlalchemy import create_engine, text
        from sqlalchemy import URL
        
        url_object = URL.create(
            "postgresql+pg8000",
            username="postgres",
            password="omarkassem",
            host="localhost",
            database="app",
            port="5432"
        )
        
        engine = create_engine(url_object)
        with engine.begin() as conn:
            result = conn.execute(text("SELECT 1"))
            print("SUCCESS: Connected with password 'omarkassem'")
            return True
            
    except Exception as e:
        print(f"FAILED: {e}")
        return False

if __name__ == "__main__":
    test_connection()

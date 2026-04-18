"""
Test database connection with different credentials
"""
import os
import sys

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_connection(username="postgres", password="postgres"):
    """Test database connection with specific credentials"""
    try:
        from sqlalchemy import create_engine, text
        from sqlalchemy import URL
        
        url_object = URL.create(
            "postgresql+pg8000",
            username=username,
            password=password,
            host="localhost",
            database="app",
            port="5432"
        )
        
        engine = create_engine(url_object)
        with engine.begin() as conn:
            result = conn.execute(text("SELECT 1"))
            print(f"SUCCESS: Connected with username='{username}', password='{password}'")
            return True
            
    except Exception as e:
        print(f"FAILED: username='{username}', password='{password}' - {e}")
        return False

def main():
    """Test common PostgreSQL credentials"""
    print("Testing PostgreSQL connection with common credentials...")
    print("=" * 60)
    
    # Common default passwords
    test_credentials = [
        ("postgres", "postgres"),
        ("postgres", "password"),
        ("postgres", "admin"),
        ("postgres", ""),
        ("postgres", "123456"),
        ("postgres", "root"),
    ]
    
    for username, password in test_credentials:
        if test_connection(username, password):
            print(f"\nFound working credentials!")
            print(f"Create .env file with:")
            print(f"DB_USER={username}")
            print(f"DB_PASSWORD={password}")
            print(f"DB_HOST=localhost")
            print(f"DB_PORT=5432")
            print(f"DB_NAME=app")
            return True
    
    print("\nNo working credentials found.")
    print("You may need to:")
    print("1. Check your PostgreSQL installation password")
    print("2. Reset the PostgreSQL password")
    print("3. Create a new database user")
    return False

if __name__ == "__main__":
    main()

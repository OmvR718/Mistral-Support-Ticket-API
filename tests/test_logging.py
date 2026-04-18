"""
Test logging and error handling functionality
"""
import os
import sys

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_logging():
    """Test logging configuration"""
    print("Testing logging configuration...")
    try:
        from app.core.logging import setup_logging, get_logger
        
        # Setup logging
        logger = setup_logging()
        
        # Test different log levels
        logger.info("This is an info message")
        logger.warning("This is a warning message")
        logger.error("This is an error message")
        
        print("Logging test completed successfully!")
        print("Check the 'logs' directory for log files.")
        return True
        
    except Exception as e:
        print(f"Logging test failed: {e}")
        return False

def test_exception_handlers():
    """Test exception handling"""
    print("\nTesting exception handling...")
    try:
        from app.core.exceptions import (
            AppException, 
            DatabaseException, 
            AuthenticationException,
            ValidationException,
            AIServiceException
        )
        
        # Test creating different exceptions
        app_exc = AppException("General app error", 500, "APP_ERROR")
        db_exc = DatabaseException("Database connection failed")
        auth_exc = AuthenticationException("Invalid credentials")
        val_exc = ValidationException("Invalid input data")
        ai_exc = AIServiceException("AI service unavailable")
        
        print(f"AppException: {app_exc.status_code} - {app_exc.error_code}")
        print(f"DatabaseException: {db_exc.status_code} - {db_exc.error_code}")
        print(f"AuthenticationException: {auth_exc.status_code} - {auth_exc.error_code}")
        print(f"ValidationException: {val_exc.status_code} - {val_exc.error_code}")
        print(f"AIServiceException: {ai_exc.status_code} - {ai_exc.error_code}")
        
        print("Exception handling test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Exception handling test failed: {e}")
        return False

def main():
    """Run logging and error handling tests"""
    print("LOGGING AND ERROR HANDLING TEST")
    print("=" * 40)
    
    tests = [test_logging, test_exception_handlers]
    results = []
    
    for test in tests:
        results.append(test())
    
    print(f"\nResults: {sum(results)}/{len(results)} tests passed")
    
    if all(results):
        print("SUCCESS: Logging and error handling are working correctly!")
    else:
        print("Some tests failed - check the errors above.")
    
    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

"""
Debug test to isolate the issue
"""
import os
import sys

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_embedding_function():
    """Test the embedding function directly"""
    print("Testing embedding function...")
    try:
        from app.ai.embeddings.nomic_embedder import embed_query
        embedding = embed_query("test text")
        print(f"Embedding generated successfully: {len(embedding)} dimensions")
        return True
    except Exception as e:
        print(f"Embedding test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database_connection():
    """Test database connection"""
    print("\nTesting database connection...")
    try:
        from app.db.database import SessionLocal
        db = SessionLocal()
        try:
            result = db.execute("SELECT 1").fetchone()
            print(f"Database connection successful: {result}")
            return True
        finally:
            db.close()
    except Exception as e:
        print(f"Database connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_chunking_function():
    """Test chunking function directly"""
    print("\nTesting chunking function...")
    try:
        from app.ai.pipelines.index_document import chunk_text
        chunks = chunk_text("This is a test document for chunking. It has multiple sentences.")
        print(f"Chunking successful: {len(chunks)} chunks created")
        for i, chunk in enumerate(chunks):
            print(f"Chunk {i+1}: {chunk[:50]}...")
        return True
    except Exception as e:
        print(f"Chunking test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("DEBUG TEST - ISOLATING THE ISSUE")
    print("=" * 50)
    
    tests = [
        test_embedding_function,
        test_database_connection,
        test_chunking_function
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print(f"\nResults: {sum(results)}/{len(results)} tests passed")
    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

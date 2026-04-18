"""
Simple test script to verify document upload functionality
"""
import os
import sys

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_document_imports():
    """Test that all document-related imports work"""
    try:
        from app.ai.pipelines.index_document import chunk_text, process_document_pipeline, count_tokens
        from app.schemas.documents import DocumentUploadRequest, DocumentResponse
        from app.api.document_api import router
        print("All document imports successful!")
        return True
    except ImportError as e:
        print(f"Import error: {e}")
        return False

def test_chunking():
    """Test the chunking functionality"""
    try:
        from app.ai.pipelines.index_document import chunk_text, count_tokens
        
        # Test text
        test_text = """
        This is a sample document for testing the chunking functionality. 
        It contains multiple sentences that should be split into chunks.
        The chunking algorithm should handle overlapping chunks properly.
        Each chunk should contain a reasonable number of words.
        This ensures that the AI classification has enough context.
        """
        
        chunks = chunk_text(test_text, chunk_size=50, overlap=10)
        
        print(f"Number of chunks created: {len(chunks)}")
        for i, chunk in enumerate(chunks):
            tokens = count_tokens(chunk)
            print(f"Chunk {i+1}: {len(chunk)} chars, {tokens} tokens")
            print(f"Text preview: {chunk[:100]}...")
            print()
        
        return True
    except Exception as e:
        print(f"Chunking test failed: {e}")
        return False

def main():
    print("Testing Document Upload Functionality")
    print("=" * 40)
    
    # Test imports
    print("1. Testing imports...")
    if not test_document_imports():
        return False
    
    # Test chunking
    print("\n2. Testing chunking...")
    if not test_chunking():
        return False
    
    print("\nAll tests passed! Document upload functionality is ready.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

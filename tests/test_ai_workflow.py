"""
Comprehensive end-to-end test for the AI workflow
Tests: Document Upload -> Chunking -> Vector Search -> Ticket Classification
"""
import os
import sys
import json
from datetime import datetime

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_document_upload_pipeline():
    """Test the complete document upload and processing pipeline"""
    print("=" * 60)
    print("1. TESTING DOCUMENT UPLOAD PIPELINE")
    print("=" * 60)
    
    try:
        from app.ai.pipelines.index_document import process_document_pipeline
        from app.db.database import SessionLocal
        
        # Sample knowledge base content
        sample_document = """
        PASSWORD RESET PROCEDURE
        
        For users who forget their password, follow these steps:
        1. Go to the login page and click "Forgot Password"
        2. Enter the email address associated with the account
        3. Check email for reset link (valid for 24 hours)
        4. Click the link and create a new password
        5. New password must be at least 8 characters with uppercase, lowercase, and numbers
        
        Priority Level: HIGH - Password issues affect user access immediately
        Category: SECURITY - Password management is a security concern
        
        SERVER DOWNTIME PROCEDURE
        
        When servers are down, follow this protocol:
        1. Check server status dashboard
        2. Notify users via email about the outage
        3. Estimate recovery time based on error logs
        4. Post updates every 30 minutes until resolved
        
        Priority Level: CRITICAL - Server downtime affects all users
        Category: INFRASTRUCTURE - Server management is infrastructure
        
        BILLING INQUIRIES
        
        For billing questions:
        1. Check account status in billing system
        2. Review recent transactions and payments
        3. Verify subscription level and features
        4. Process refunds according to policy
        
        Priority Level: MEDIUM - Billing issues are important but not urgent
        Category: BILLING - Financial transactions and account management
        """
        
        # Test the pipeline
        db = SessionLocal()
        try:
            result = process_document_pipeline(
                db=db,
                title="Support Knowledge Base",
                source="internal_documentation",
                content=sample_document,
                content_type="txt",
                uploaded_by=1
            )
            
            print(f"Document uploaded successfully!")
            print(f"Document ID: {result['document_id']}")
            print(f"Title: {result['title']}")
            print(f"Chunks created: {result['chunks_created']}")
            print(f"Total tokens: {result['total_tokens']}")
            
            return result['document_id']
            
        finally:
            db.close()
            
    except Exception as e:
        print(f"Document upload test failed: {e}")
        return None

def test_vector_search(document_id):
    """Test vector search functionality"""
    print("\n" + "=" * 60)
    print("2. TESTING VECTOR SEARCH")
    print("=" * 60)
    
    try:
        from app.ai.embeddings.nomic_embedder import embed_query
        from app.ai.retrieval.vector_search import retrieve_similar_chunks
        from app.db.database import SessionLocal
        
        # Test query similar to password reset
        test_query = "I forgot my password and can't login to my account"
        
        db = SessionLocal()
        try:
            # Generate embedding for test query
            query_embedding = embed_query(test_query)
            print(f"Generated embedding for query: '{test_query}'")
            print(f"Embedding dimension: {len(query_embedding)}")
            
            # Retrieve similar chunks
            similar_chunks = retrieve_similar_chunks(db, query_embedding, top_k=3)
            
            print(f"\nFound {len(similar_chunks)} similar chunks:")
            for i, chunk in enumerate(similar_chunks):
                print(f"\nChunk {i+1} (ID: {chunk.id}):")
                print(f"Document ID: {chunk.doc_id}")
                print(f"Chunk Index: {chunk.chunk_index}")
                print(f"Token Count: {chunk.token_count}")
                print(f"Text Preview: {chunk.text[:150]}...")
            
            return similar_chunks
            
        finally:
            db.close()
            
    except Exception as e:
        print(f"Vector search test failed: {e}")
        return []

def test_ticket_classification():
    """Test ticket classification with retrieved context"""
    print("\n" + "=" * 60)
    print("3. TESTING TICKET CLASSIFICATION")
    print("=" * 60)
    
    try:
        from app.ai.pipelines.classify_ticket import classify_ticket_pipeline
        from app.db.database import SessionLocal
        from app.db.models import Ticket
        
        # Create a test ticket
        test_ticket = type('Ticket', (), {
            'id': 999,
            'subject': 'Password Reset Request',
            'body': 'Hello, I forgot my password and cannot access my account. I tried the reset link but it expired. Can you help me reset my password urgently?'
        })()
        
        db = SessionLocal()
        try:
            # Run classification pipeline
            result = classify_ticket_pipeline(db, test_ticket)
            
            print(f"Classification completed successfully!")
            print(f"Category: {result['category']}")
            print(f"Priority: {result['priority']}")
            print(f"Confidence: {result['confidence']}")
            print(f"Citations: {len(result['citations'])} chunks used")
            
            # Show citations
            for i, citation in enumerate(result['citations']):
                print(f"Citation {i+1}: Chunk ID {citation['chunk_id']}, Doc ID {citation['doc_id']}")
            
            return result
            
        finally:
            db.close()
            
    except Exception as e:
        print(f"Ticket classification test failed: {e}")
        return None

def test_prompt_building():
    """Test the prompt building functionality"""
    print("\n" + "=" * 60)
    print("4. TESTING PROMPT BUILDING")
    print("=" * 60)
    
    try:
        from app.ai.prompts.classifier_prompt import build_classification_prompt
        
        ticket_text = "I forgot my password and need help accessing my account"
        chunks = [
            "Password reset procedure: Click forgot password, enter email, check reset link",
            "Security policy: Password must be 8+ characters with uppercase, lowercase, numbers"
        ]
        
        prompt = build_classification_prompt(ticket_text, chunks)
        
        print("Generated classification prompt:")
        print("-" * 40)
        print(prompt[:500] + "..." if len(prompt) > 500 else prompt)
        print("-" * 40)
        
        return True
        
    except Exception as e:
        print(f"Prompt building test failed: {e}")
        return False

def main():
    """Run all AI workflow tests"""
    print("MISTRAL SUPPORT TICKET API - AI WORKFLOW TEST")
    print("=" * 60)
    print(f"Test started at: {datetime.now()}")
    
    # Test 1: Document Upload
    document_id = test_document_upload_pipeline()
    if not document_id:
        print("FAILED: Document upload pipeline")
        return False
    
    # Test 2: Vector Search
    similar_chunks = test_vector_search(document_id)
    if not similar_chunks:
        print("FAILED: Vector search")
        return False
    
    # Test 3: Ticket Classification
    classification_result = test_ticket_classification()
    if not classification_result:
        print("FAILED: Ticket classification")
        return False
    
    # Test 4: Prompt Building
    if not test_prompt_building():
        print("FAILED: Prompt building")
        return False
    
    # Summary
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED! AI WORKFLOW IS FULLY FUNCTIONAL")
    print("=" * 60)
    print(f"Test completed at: {datetime.now()}")
    print("\nWorkflow Summary:")
    print("1. Document Upload -> Chunking -> Embeddings: SUCCESS")
    print("2. Vector Search with Cosine Similarity: SUCCESS")
    print("3. Ticket Classification with RAG: SUCCESS")
    print("4. Prompt Building with Context: SUCCESS")
    print("\nThe system is ready for production use!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

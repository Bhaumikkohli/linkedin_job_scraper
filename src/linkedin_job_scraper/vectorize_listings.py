from llama_index import Document, VectorStoreIndex
from llama_index.node_parser import SimpleNodeParser
from llama_index.embeddings import HuggingFaceEmbeddings
import os
import json
from typing import List, Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JobListingVectorizer:
    """Process job listings text files and convert them to vector embeddings."""
    
    def __init__(self, input_dir: str, output_dir: str, batch_size: int = 100):
        """
        Initialize the vectorizer with directories and settings.
        
        Args:
            input_dir (str): Directory containing job listing text files
            output_dir (str): Directory to save vectorized outputs
            batch_size (int): Number of listings to process in each batch
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.batch_size = batch_size
        
        # Initialize embedding model
        self.embed_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Initialize node parser
        self.parser = SimpleNodeParser.from_defaults()
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
    
    def load_job_listings(self) -> List[Dict]:
        """Load all job listing files from the input directory."""
        job_listings = []
        
        for filename in os.listdir(self.input_dir):
            if filename.endswith('.txt'):
                file_path = os.path.join(self.input_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        job_listings.append({
                            'id': filename.replace('.txt', ''),
                            'content': content
                        })
                except Exception as e:
                    logger.error(f"Error reading file {filename}: {str(e)}")
                    continue
        
        return job_listings
    
    def vectorize_listings(self, listings: List[Dict]) -> List[Dict]:
        """Convert job listings to vector embeddings."""
        vectorized_listings = []
        
        for i in range(0, len(listings), self.batch_size):
            batch = listings[i:i + self.batch_size]
            
            try:
                # Create documents for the batch
                documents = [
                    Document(text=listing['content'], doc_id=listing['id'])
                    for listing in batch
                ]
                
                # Parse into nodes
                nodes = self.parser.get_nodes_from_documents(documents)
                
                # Create vector store index
                index = VectorStoreIndex(
                    nodes,
                    embed_model=self.embed_model,
                    show_progress=True
                )
                
                # Get vector store data
                vector_store = index.vector_store
                
                # Store embeddings and metadata
                for node in nodes:
                    vectorized_listings.append({
                        'id': node.doc_id,
                        'embedding': vector_store.embeddings[node.node_id].tolist(),
                        'metadata': node.metadata
                    })
                
                logger.info(f"Processed batch of {len(batch)} listings")
                
            except Exception as e:
                logger.error(f"Error processing batch: {str(e)}")
                continue
        
        return vectorized_listings
    
    def save_vectors(self, vectors: List[Dict]):
        """Save vectorized listings to output directory."""
        output_file = os.path.join(self.output_dir, 'vectorized_listings.json')
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(vectors, f)
            logger.info(f"Saved vectorized listings to {output_file}")
        except Exception as e:
            logger.error(f"Error saving vectors: {str(e)}")
    
    def process(self):
        """Run the complete vectorization pipeline."""
        logger.info("Starting job listing vectorization process")
        
        # Load listings
        listings = self.load_job_listings()
        logger.info(f"Loaded {len(listings)} job listings")
        
        # Vectorize
        vectors = self.vectorize_listings(listings)
        logger.info(f"Vectorized {len(vectors)} listings")
        
        # Save results
        self.save_vectors(vectors)
        logger.info("Process completed")

if __name__ == "__main__":
    # Example usage
    vectorizer = JobListingVectorizer(
        input_dir="data/raw_listings",
        output_dir="data/vectorized_listings"
    )
    vectorizer.process()

import os
import json
import time  
from volcenginesdkarkruntime import Ark

def generate_and_save_embeddings(file_path="embedding_text.txt", output_path="embeddings.json", 
                                 batch_size=256, max_retries=3, initial_delay=1):
    """
    Generate embedding vectors from a text file (in batches) and save to a JSON file
    
    Parameters:
        file_path: Path to the input file containing text content
        output_path: Path to the output file for saving embedding vectors
        batch_size: Maximum number of texts per batch (model limit is 256)
        max_retries: Maximum number of retries when server is overloaded
        initial_delay: Initial delay (in seconds) for retry, will increase exponentially
        
    Returns:
        List containing texts and their corresponding embedding vectors
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file not found: {file_path}")
    
    try:
        
        with open(file_path, "r", encoding="utf-8") as f:
            texts = [line.strip() for line in f if line.strip()]
        
        if not texts:
            print("Warning: No valid text content in the input file")
            return []
            
        total = len(texts)
        print(f"Successfully read {total} text entries")
        print(f"Will process in {((total + batch_size - 1) // batch_size)} batches (batch size: {batch_size})")
        
        
        client = Ark(
            api_key=os.environ.get("ARK_API_KEY"),
            base_url="https://ark.cn-beijing.volces.com/api/v3"
        )
        
        results = []
        
        for i in range(0, total, batch_size):
            batch_texts = texts[i:i+batch_size]
            batch_num = (i // batch_size) + 1
            print(f"Processing batch {batch_num} ({len(batch_texts)} texts)...")
            
            
            retries = 0
            while retries < max_retries:
                try:
                    response = client.embeddings.create(
                        model="ep-20250818160550-v84jg",
                        input=batch_texts,
                        encoding_format="float"
                    )
                    break  
                except Exception as e:
                    if e.status_code == 429 or (hasattr(e, 'code') and e.code == 'ServerOverloaded'):
                        retries += 1
                        if retries >= max_retries:
                            raise Exception(f"Failed to process batch {batch_num} after {max_retries} retries")
                        delay = initial_delay * (2 ** (retries - 1))
                        print(f"Server overloaded, retrying batch {batch_num} in {delay}s (retry {retries}/{max_retries})...")
                        time.sleep(delay)
                    else:
                        raise e
            
            batch_results = [
                {"text": text, "embedding": data.embedding}
                for text, data in zip(batch_texts, response.data)
            ]
            results.extend(batch_results)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"Successfully generated and saved {len(results)} vectors to {output_path}")
        return results
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    generate_and_save_embeddings()

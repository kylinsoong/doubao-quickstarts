import json
import os
import uuid
import urllib.parse

def knowledge_service_add_file(file_url):
    """Add file to knowledge base service"""
    AK = os.environ.get("VOLCENGINE_ACCESS_KEY")  
    SK = os.environ.get("VOLCENGINE_SECRET_KEY")  
    REGION = "cn-beijing"  
    KB_NAME = "images"  
    
    # Extract filename from FILE_URL
    parsed_url = urllib.parse.urlparse(file_url)
    filename = os.path.basename(parsed_url.path)
    # Remove query parameters if any
    if '?' in filename:
        filename = filename.split('?')[0]
    # Get doc name (without extension)
    if '.' in filename:
        DOC_NAME = filename.rsplit('.', 1)[0]
    else:
        DOC_NAME = filename
    # Get file extension and map to doc_type
    if '.' in filename:
        ext = filename.rsplit('.', 1)[1].lower()
        # Map extensions to doc_type (only support image and video)
        if ext in ['jpg', 'jpeg']:
            DOC_TYPE = 'jpeg'
        elif ext in ['png']:
            DOC_TYPE = 'png'
        elif ext in ['webp']:
            DOC_TYPE = 'webp'
        elif ext in ['bmp']:
            DOC_TYPE = 'bmp'
        elif ext in ['mp4']:
            DOC_TYPE = 'mp4'
        else:
            raise ValueError(f"Unsupported file extension: {ext}. Only support image (jpg, jpeg, png, webp, bmp) and video (mp4) types.")
    else:
        raise ValueError("No file extension found in URL. Please provide a URL with a valid file extension.")
    
    # Generate DOC_ID with UUID and prefix
    DOC_ID = f"_agent_add_{str(uuid.uuid4()).replace('-', '')}"
    # Print values
    print(f"FILE_URL: {file_url}")
    print(f"DOC_NAME: {DOC_NAME}")
    print(f"DOC_TYPE: {DOC_TYPE}")
    print(f"DOC_ID: {DOC_ID}")
    
    if not AK:
        raise ValueError("Please set the environment variable VOLCENGINE_ACCESS_KEY")
    if not SK:
        raise ValueError("Please set the environment variable VOLCENGINE_SECRET_KEY")
    
    try:
        from volcengine.viking_knowledgebase.VikingKnowledgeBaseService import VikingKnowledgeBaseService
        
        # Create service instance
        service = VikingKnowledgeBaseService(
            host="api-knowledgebase.mlp.cn-beijing.volces.com",
            region=REGION,
            ak=AK,
            sk=SK,
            scheme="https"
        )
        
        # Build request parameters
        params = {
            "collection_name": KB_NAME,
            "add_type": "url",
            "doc_id": DOC_ID,
            "doc_name": DOC_NAME,
            "doc_type": DOC_TYPE,
            "url": file_url
        }
        
        # Send request using json method, api parameter is "AddDoc"
        # Convert params to JSON string
        import json as json_module
        response = service.json("AddDoc", {}, json_module.dumps(params))
        
        print("\nResponse using viking_knowledgebase module:")
        print(f"Response content: {json.dumps(response, indent=2, ensure_ascii=False)}")
        
    except ImportError as e:
        print(f"\nModule import error: {str(e)}")
        print("Please make sure volcengine library is installed: pip install volcengine")
    
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        import traceback
        traceback.print_exc()

def main():
    """Main function to read file URL and add to knowledge base"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    url_file = os.path.join(script_dir, "image_url.txt")
    try:
        with open(url_file, 'r') as f:
            for line in f:
                stripped_line = line.strip()
                if stripped_line and not stripped_line.startswith('#'):
                    FILE_URL = stripped_line
                    break
            else:
                raise ValueError(f"Please set the image URL in {url_file} file (non-comment line)")
    except FileNotFoundError:
        raise ValueError(f"Please create {url_file} file with the image URL")
    
    knowledge_service_add_file(FILE_URL)

if __name__ == "__main__":
    main()
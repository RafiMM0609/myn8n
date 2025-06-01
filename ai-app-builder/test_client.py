import requests
import json

def test_app_generation():
    """Test the app generation service with Gemini"""
    
    # Test prompt dalam bahasa Indonesia
    prompt = "Buatkan backend service dengan FastAPI untuk sistem e-commerce dengan authentication JWT, PostgreSQL database, dan fitur CRUD untuk products, users, dan orders. Sertakan juga Redis untuk caching."
    
    print("🚀 Testing AI App Builder with Gemini...")
    print(f"📝 Prompt: {prompt}")
    
    # Send request
    try:
        response = requests.post("http://localhost:8000/generate", json={
            "prompt": prompt,
            "project_name": "ecommerce_gemini"
        }, timeout=120)  # Increased timeout for Gemini
        
        if response.status_code == 200:
            result = response.json()
            print("✅ App generated successfully!")
            print(f"📁 Project path: {result['project_path']}")
            print(f"📄 Files generated: {result['files_generated']}")
            print(f"🔍 Analysis: {json.dumps(result['analysis'], indent=2)}")
            
            # List generated files
            import os
            project_path = result['project_path']
            if os.path.exists(project_path):
                print(f"\n📂 Generated files in {project_path}:")
                for root, dirs, files in os.walk(project_path):
                    level = root.replace(project_path, '').count(os.sep)
                    indent = ' ' * 2 * level
                    print(f"{indent}📁 {os.path.basename(root)}/")
                    subindent = ' ' * 2 * (level + 1)
                    for file in files:
                        print(f"{subindent}📄 {file}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📝 Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        print("💡 Make sure the service is running with: python start.py")

def test_analysis_only():
    """Test just the analysis feature"""
    
    prompt = "Buat REST API untuk blog dengan authentication dan comment system"
    
    print("\n🔍 Testing analysis only...")
    
    try:
        response = requests.post("http://localhost:8000/analyze", json={
            "prompt": prompt
        })
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Analysis completed!")
            print(f"🔍 Analysis: {json.dumps(result['analysis'], indent=2)}")
        else:
            print(f"❌ Error: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    test_analysis_only()
    test_app_generation()
import subprocess
import sys
import os
from pathlib import Path

def setup_environment():
    """Setup the development environment for WSL"""
    print("🚀 Setting up AI App Builder with Gemini (WSL)...")
    
    # Install dependencies using python3
    print("📦 Installing dependencies...")
    try:
        subprocess.run(["python3", "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    except subprocess.CalledProcessError:
        print("⚠️  Trying with pip3...")
        subprocess.run(["pip3", "install", "-r", "requirements.txt"], check=True)
    
    # Create directories
    Path("generated_apps").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    
    print("✅ Environment setup complete!")
    print("🔑 Don't forget to add your Gemini API key to .env file!")

def start_service():
    """Start the AI App Builder service"""
    print("🔥 Starting AI App Builder service with Gemini (WSL)...")
    
    # Check if .env exists
    if not Path(".env").exists():
        print("⚠️  Creating .env file - please add your Gemini API key!")
        with open(".env", "w") as f:
            f.write("GEMINI_API_KEY=your_gemini_api_key_here\n")
            f.write("DATABASE_URL=sqlite:///./test.db\n")
            f.write("SECRET_KEY=your_secret_key_here\n")
            f.write("GEMINI_MODEL=gemini-1.5-pro\n")
        
        print("📝 Please edit .env file and add your Gemini API key from https://makersuite.google.com/app/apikey")
        return
    
    # Check if Gemini API key is set
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY") == "your_gemini_api_key_here":
        print("❌ Please set your GEMINI_API_KEY in .env file")
        print("🔗 Get your API key from: https://makersuite.google.com/app/apikey")
        return
    
    # Start the service using python3
    os.chdir("services")
    try:
        subprocess.run(["python3", "main.py"])
    except KeyboardInterrupt:
        print("\n👋 Service stopped.")
    except Exception as e:
        print(f"❌ Error starting service: {e}")
        print("💡 Try running: python3 services/main.py")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "setup":
        setup_environment()
    else:
        start_service()
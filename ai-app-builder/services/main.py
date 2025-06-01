from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import google.generativeai as genai
import os
import platform
import json
import asyncio
from pathlib import Path
import subprocess
from datetime import datetime

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="AI App Builder Service with Gemini", version="1.0.0")

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-1.5-pro"))

class AppRequest(BaseModel):
    prompt: str
    project_name: Optional[str] = None
    output_dir: Optional[str] = "./generated_apps"

class ProjectAnalysis(BaseModel):
    framework: str
    database: str
    features: List[str]
    endpoints: List[str]
    auth_type: str
    external_services: List[str]

class AppBuilderService:
    def __init__(self):
        self.output_base = Path("./generated_apps")
        self.output_base.mkdir(exist_ok=True)
        
    async def analyze_prompt(self, prompt: str) -> ProjectAnalysis:
        """Analyze user prompt using Gemini AI"""
        
        analysis_prompt = f"""
        Analisis permintaan pengembangan berikut dan ekstrak informasi terstruktur:
        
        Permintaan User: "{prompt}"
        
        Harap kembalikan objek JSON dengan field berikut:
        {{
            "framework": "fastapi|django|flask|express|nestjs",
            "database": "postgresql|mysql|sqlite|mongodb", 
            "features": ["authentication", "crud", "api", "admin", "cache"],
            "endpoints": ["users", "products", "orders"],
            "auth_type": "jwt|session|oauth2|none",
            "external_services": ["redis", "elasticsearch", "s3"]
        }}
        
        Hanya kembalikan JSON murni tanpa penjelasan tambahan.
        Pastikan respons valid JSON format.
        """
        
        try:
            response = model.generate_content(analysis_prompt)
            
            # Clean response text
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:-3]
            elif response_text.startswith("```"):
                response_text = response_text[3:-3]
            
            result = json.loads(response_text)
            return ProjectAnalysis(**result)
            
        except Exception as e:
            print(f"Error analyzing prompt: {e}")
            # Fallback analysis
            return ProjectAnalysis(
                framework="fastapi",
                database="sqlite", 
                features=["crud", "api"],
                endpoints=["items"],
                auth_type="none",
                external_services=[]
            )
    
    async def generate_project_structure(self, analysis: ProjectAnalysis, project_name: str) -> Dict[str, str]:
        """Generate complete project structure and code"""
        
        if analysis.framework == "fastapi":
            return await self.generate_fastapi_project(analysis, project_name)
        elif analysis.framework == "flask":
            return await self.generate_flask_project(analysis, project_name)
        else:
            raise HTTPException(status_code=400, detail=f"Framework {analysis.framework} belum didukung")
    
    async def generate_fastapi_project(self, analysis: ProjectAnalysis, project_name: str) -> Dict[str, str]:
        """Generate FastAPI project structure"""
        
        files = {}
        
        # Generate main application
        files["main.py"] = await self.generate_fastapi_main(analysis, project_name)
        
        # Generate models
        files["models.py"] = await self.generate_models(analysis)
        
        # Generate database configuration
        files["database.py"] = await self.generate_database_config(analysis)
        
        # Generate schemas
        files["schemas.py"] = await self.generate_schemas(analysis)
        
        # Generate CRUD operations
        files["crud.py"] = await self.generate_crud(analysis)
        
        # Generate requirements
        files["requirements.txt"] = self.generate_requirements(analysis)
        
        # Generate Docker files
        files["Dockerfile"] = self.generate_dockerfile(analysis)
        files["docker-compose.yml"] = self.generate_docker_compose(analysis, project_name)
        
        # Generate environment file
        files[".env.example"] = self.generate_env_template(analysis)
        
        # Generate README
        files["README.md"] = await self.generate_readme(analysis, project_name)
        
        return files
    
    async def generate_fastapi_main(self, analysis: ProjectAnalysis, project_name: str) -> str:
        """Generate main FastAPI application file using Gemini"""
        
        prompt = f"""
        Buatkan file main.py lengkap untuk aplikasi FastAPI dengan requirements berikut:
        
        - Nama project: {project_name}
        - Database: {analysis.database}
        - Authentication: {analysis.auth_type}
        - Fitur: {', '.join(analysis.features)}
        - Endpoints yang dibutuhkan: {', '.join(analysis.endpoints)}
        - External services: {', '.join(analysis.external_services)}
        
        Sertakan:
        - Import yang tepat
        - CORS middleware
        - Error handling
        - Health check endpoint
        - Semua CRUD endpoints untuk entitas yang disebutkan
        - Authentication middleware jika diperlukan
        - Startup dan shutdown events yang tepat
        - Documentation yang baik
        
        Kembalikan hanya kode Python, tanpa penjelasan.
        Pastikan kode dapat langsung dijalankan.
        """
        
        response = model.generate_content(prompt)
        
        # Clean code blocks
        code = response.text.strip()
        if code.startswith("```python"):
            code = code[9:-3]
        elif code.startswith("```"):
            code = code[3:-3]
        
        return code
    
    async def generate_models(self, analysis: ProjectAnalysis) -> str:
        """Generate SQLAlchemy models using Gemini"""
        
        prompt = f"""
        Buatkan SQLAlchemy models untuk endpoints berikut: {', '.join(analysis.endpoints)}
        Database: {analysis.database}
        
        Sertakan:
        - Import yang tepat
        - Base model class
        - Semua relationship yang diperlukan
        - Field types yang tepat
        - Created/updated timestamps
        - Primary keys dan foreign keys
        
        Kembalikan hanya kode Python.
        """
        
        response = model.generate_content(prompt)
        code = response.text.strip()
        if code.startswith("```python"):
            code = code[9:-3]
        elif code.startswith("```"):
            code = code[3:-3]
        
        return code
    
    async def generate_database_config(self, analysis: ProjectAnalysis) -> str:
        """Generate database configuration"""
        
        prompt = f"""
        Buatkan konfigurasi database SQLAlchemy untuk {analysis.database}.
        
        Sertakan:
        - Database URL configuration
        - SessionLocal setup
        - Engine configuration
        - Base class untuk models
        - Connection pooling yang optimal
        
        Kembalikan hanya kode Python.
        """
        
        response = model.generate_content(prompt)
        code = response.text.strip()
        if code.startswith("```python"):
            code = code[9:-3]
        elif code.startswith("```"):
            code = code[3:-3]
        
        return code
    
    async def generate_schemas(self, analysis: ProjectAnalysis) -> str:
        """Generate Pydantic schemas"""
        
        prompt = f"""
        Buatkan Pydantic schemas untuk endpoints: {', '.join(analysis.endpoints)}
        
        Sertakan:
        - Base schemas
        - Create schemas
        - Update schemas
        - Response schemas
        - Validation yang tepat
        
        Kembalikan hanya kode Python.
        """
        
        response = model.generate_content(prompt)
        code = response.text.strip()
        if code.startswith("```python"):
            code = code[9:-3]
        elif code.startswith("```"):
            code = code[3:-3]
        
        return code
    
    async def generate_crud(self, analysis: ProjectAnalysis) -> str:
        """Generate CRUD operations"""
        
        prompt = f"""
        Buatkan operasi CRUD lengkap untuk endpoints: {', '.join(analysis.endpoints)}
        Database: {analysis.database}
        
        Sertakan:
        - Create, Read, Update, Delete functions
        - Query optimizations
        - Error handling
        - Pagination untuk list operations
        
        Kembalikan hanya kode Python.
        """
        
        response = model.generate_content(prompt)
        code = response.text.strip()
        if code.startswith("```python"):
            code = code[9:-3]
        elif code.startswith("```"):
            code = code[3:-3]
        
        return code
    
    async def generate_readme(self, analysis: ProjectAnalysis, project_name: str) -> str:
        """Generate README.md"""
        
        prompt = f"""
        Buatkan README.md lengkap untuk project {project_name} dengan:
        - Framework: {analysis.framework}
        - Database: {analysis.database}
        - Features: {', '.join(analysis.features)}
        
        Sertakan:
        - Deskripsi project
        - Installation instructions
        - Usage examples
        - API documentation
        - Environment setup
        
        Format dalam Markdown.
        """
        
        response = model.generate_content(prompt)
        return response.text.strip()
    
    def generate_requirements(self, analysis: ProjectAnalysis) -> str:
        """Generate requirements.txt based on analysis"""
        
        base_requirements = [
            "fastapi==0.104.1",
            "uvicorn[standard]==0.24.0",
            "sqlalchemy==2.0.23",
            "alembic==1.12.1",
            "pydantic==2.5.0",
            "python-dotenv==1.0.0"
        ]
        
        # Add database drivers
        if analysis.database == "postgresql":
            base_requirements.append("psycopg2-binary==2.9.9")
        elif analysis.database == "mysql":
            base_requirements.append("pymysql==1.1.0")
        
        # Add auth dependencies
        if analysis.auth_type == "jwt":
            base_requirements.extend([
                "python-jose[cryptography]==3.3.0",
                "passlib[bcrypt]==1.7.4",
                "python-multipart==0.0.6"
            ])
        
        # Add external services
        if "redis" in analysis.external_services:
            base_requirements.append("redis==5.0.1")
        
        return "\n".join(base_requirements)
    
    def generate_dockerfile(self, analysis: ProjectAnalysis) -> str:
        """Generate Dockerfile"""
        
        return """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
    
    def generate_docker_compose(self, analysis: ProjectAnalysis, project_name: str) -> str:
        """Generate docker-compose.yml"""
        
        if analysis.database == "postgresql":
            return f"""version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/{project_name}
    depends_on:
      - db
    
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB={project_name}
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
"""
        else:
            return f"""version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
"""
    
    def generate_env_template(self, analysis: ProjectAnalysis) -> str:
        """Generate .env template"""
        
        env_vars = [
            "SECRET_KEY=your_secret_key_here",
            f"DATABASE_URL=sqlite:///./{analysis.database}.db"
        ]
        
        if analysis.auth_type == "jwt":
            env_vars.append("JWT_SECRET_KEY=your_jwt_secret_here")
        
        if "redis" in analysis.external_services:
            env_vars.append("REDIS_URL=redis://localhost:6379")
        
        return "\n".join(env_vars)

# Initialize service
builder_service = AppBuilderService()

@app.post("/analyze")
async def analyze_request(request: AppRequest):
    """Analyze user prompt and return project analysis"""
    try:
        analysis = await builder_service.analyze_prompt(request.prompt)
        return {"status": "success", "analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate")
async def generate_app(request: AppRequest, background_tasks: BackgroundTasks):
    """Generate complete application"""
    try:
        # Analyze prompt
        analysis = await builder_service.analyze_prompt(request.prompt)
        
        # Generate project name if not provided
        project_name = request.project_name or f"generated_app_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Generate project structure
        files = await builder_service.generate_project_structure(analysis, project_name)
        
        # Create project directory
        project_path = builder_service.output_base / project_name
        project_path.mkdir(exist_ok=True)
        
        # Write all files
        for file_path, content in files.items():
            full_path = project_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding='utf-8')
        
        # Add background task to setup environment
        background_tasks.add_task(setup_project_environment, str(project_path))
        
        return {
            "status": "success",
            "project_name": project_name,
            "project_path": str(project_path),
            "files_generated": len(files),
            "analysis": analysis
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def setup_project_environment(project_path: str):
    """Setup virtual environment and install dependencies"""
    try:
        print(f"🔧 Setting up environment for {project_path}")
        
        # Create virtual environment
        venv_path = f"{project_path}/venv"
        print(f"📦 Creating virtual environment at {venv_path}")
        
        result = subprocess.run([
            "python", "-m", "venv", venv_path
        ], capture_output=True, text=True, check=True)
        
        # Determine correct pip path for Windows
        import platform
        if platform.system() == "Windows":
            pip_path = f"{venv_path}/Scripts/pip.exe"
            python_path = f"{venv_path}/Scripts/python.exe"
        else:
            pip_path = f"{venv_path}/bin/pip"
            python_path = f"{venv_path}/bin/python"
        
        # Check if pip exists
        if not os.path.exists(pip_path):
            print(f"❌ Pip not found at {pip_path}")
            print("🔄 Trying alternative setup...")
            
            # Alternative: use the main Python to install in venv
            result = subprocess.run([
                "python", "-m", "pip", "install", "-r", f"{project_path}/requirements.txt",
                "--target", f"{venv_path}/Lib/site-packages"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Dependencies installed successfully (alternative method)")
            else:
                print(f"❌ Failed to install dependencies: {result.stderr}")
            return
        
        # Install dependencies using venv pip
        print(f"📥 Installing dependencies using {pip_path}")
        result = subprocess.run([
            pip_path, "install", "-r", f"{project_path}/requirements.txt"
        ], capture_output=True, text=True, check=True)
        
        print(f"✅ Environment setup completed for {project_path}")
        print(f"🚀 To run the project:")
        print(f"   cd {project_path}")
        print(f"   {python_path} main.py")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error setting up environment: {e}")
        print(f"📝 Error output: {e.stderr if hasattr(e, 'stderr') else 'No error details'}")
    except Exception as e:
        print(f"❌ Error setting up environment: {e}")
        
        # Fallback: create a simple run script
        try:
            run_script_content = f"""@echo off
echo Starting {project_path}
cd /d "{project_path}"
python -m pip install -r requirements.txt
python main.py
pause
"""
            with open(f"{project_path}/run.bat", "w") as f:
                f.write(run_script_content)
            
            print(f"📝 Created run.bat script. You can run the project with: {project_path}/run.bat")
        except:
            pass

@app.get("/projects")
async def list_projects():
    """List all generated projects"""
    projects = []
    for project_dir in builder_service.output_base.iterdir():
        if project_dir.is_dir():
            projects.append({
                "name": project_dir.name,
                "path": str(project_dir),
                "created": datetime.fromtimestamp(project_dir.stat().st_ctime).isoformat()
            })
    
    return {"projects": projects}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AI App Builder with Gemini"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
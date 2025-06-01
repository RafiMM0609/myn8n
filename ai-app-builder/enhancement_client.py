import requests
import json
import os
from pathlib import Path

class AppEnhancer:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def analyze_project(self, project_path: str):
        """Analyze existing project"""
        print(f"🔍 Analyzing project: {project_path}")
        
        try:
            response = requests.post(f"{self.base_url}/analyze-existing", json={
                "project_path": project_path,
                "enhancement_request": "analyze",
                "enhancement_type": "analysis"
            }, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Analysis completed!")
                
                analysis = result["analysis"]
                print(f"\n📊 Current Structure:")
                print(f"   Files: {analysis['current_structure']['files_count']}")
                print(f"   Components: {', '.join(analysis['current_structure']['main_components'])}")
                print(f"   Architecture: {analysis['current_structure']['architecture_pattern']}")
                print(f"   Database: {analysis['current_structure']['database_used']}")
                print(f"   Complexity: {analysis['complexity_score']}/10")
                
                print(f"\n⚠️  Issues Found:")
                for issue in analysis['identified_issues']:
                    print(f"   - {issue}")
                
                print(f"\n💡 Suggestions:")
                for suggestion in analysis['improvement_suggestions']:
                    print(f"   - {suggestion}")
                
                return result
            else:
                print(f"❌ Analysis failed: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def enhance_project(self, project_path: str, enhancement_request: str, enhancement_type: str = "feature"):
        """Enhance existing project"""
        print(f"\n🔧 Enhancing project: {project_path}")
        print(f"📝 Request: {enhancement_request}")
        print(f"🎯 Type: {enhancement_type}")
        
        try:
            response = requests.post(f"{self.base_url}/enhance-app", json={
                "project_path": project_path,
                "enhancement_request": enhancement_request,
                "enhancement_type": enhancement_type
            }, timeout=180)
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Enhancement completed!")
                
                if "enhancements" in result and "changes_summary" in result["enhancements"]:
                    print(f"\n📝 Changes Made:")
                    print(f"   {result['enhancements']['changes_summary']}")
                
                # Show modified files
                if "enhancements" in result:
                    enhancements = result["enhancements"]
                    if "modifications" in enhancements:
                        print(f"\n🔧 Modified Files:")
                        for file_path in enhancements["modifications"].keys():
                            print(f"   - {file_path}")
                    
                    if "new_files" in enhancements:
                        print(f"\n📄 New Files:")
                        for file_path in enhancements["new_files"].keys():
                            print(f"   - {file_path}")
                
                return result
            else:
                print(f"❌ Enhancement failed: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def list_projects(self):
        """List available projects"""
        try:
            response = requests.get(f"{self.base_url}/projects")
            if response.status_code == 200:
                projects = response.json()["projects"]
                print("📁 Available Projects:")
                for i, project in enumerate(projects, 1):
                    print(f"   {i}. {project['name']} ({project['path']})")
                return projects
            else:
                print("❌ Failed to list projects")
                return []
        except Exception as e:
            print(f"❌ Error: {e}")
            return []

def main():
    enhancer = AppEnhancer()
    
    print("🚀 AI App Enhancer")
    print("=" * 50)
    
    # List available projects
    projects = enhancer.list_projects()
    
    if not projects:
        print("❌ No projects found. Generate a project first!")
        return
    
    # Let user select project
    try:
        choice = int(input(f"\nSelect project (1-{len(projects)}): ")) - 1
        if choice < 0 or choice >= len(projects):
            print("❌ Invalid choice")
            return
        
        selected_project = projects[choice]
        project_path = selected_project["path"]
        
        print(f"\n✅ Selected: {selected_project['name']}")
        
        # Analyze first
        print("\n" + "="*50)
        enhancer.analyze_project(project_path)
        
        # Ask for enhancement
        print("\n" + "="*50)
        print("Enhancement Options:")
        print("1. Add new feature")
        print("2. Optimize performance") 
        print("3. Add security features")
        print("4. Fix bugs")
        print("5. Custom enhancement")
        
        enhancement_choice = input("\nSelect enhancement type (1-5): ")
        
        enhancement_requests = {
            "1": ("Add user authentication with JWT tokens and login/logout endpoints", "feature"),
            "2": ("Optimize database queries, add caching with Redis, and improve response times", "optimization"),
            "3": ("Add input validation, rate limiting, CORS security, and data encryption", "security"),
            # "4": ("Fix any bugs, improve error handling, and add proper logging", "bug_fix"),
            "4": ("Fix ModuleNotFoundError: No module named databases", "bug_fix"),
            "5": (input("Describe your enhancement request: "), "feature")
        }
        
        if enhancement_choice in enhancement_requests:
            request, req_type = enhancement_requests[enhancement_choice]
            enhancer.enhance_project(project_path, request, req_type)
        else:
            print("❌ Invalid choice")
    
    except ValueError:
        print("❌ Invalid input")
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()
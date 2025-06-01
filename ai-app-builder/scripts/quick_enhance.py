import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enhancement_client import AppEnhancer

def quick_add_auth(project_path):
    """Quick add authentication"""
    enhancer = AppEnhancer()
    return enhancer.enhance_project(
        project_path,
        "Add JWT authentication with login, register, and protected routes",
        "feature"
    )

def quick_add_tests(project_path):
    """Quick add tests"""
    enhancer = AppEnhancer()
    return enhancer.enhance_project(
        project_path,
        "Add comprehensive unit tests and integration tests for all endpoints",
        "feature"
    )

def quick_optimize(project_path):
    """Quick performance optimization"""
    enhancer = AppEnhancer()
    return enhancer.enhance_project(
        project_path,
        "Optimize performance with caching, async operations, and database improvements",
        "optimization"
    )

def quick_secure(project_path):
    """Quick security enhancements"""
    enhancer = AppEnhancer()
    return enhancer.enhance_project(
        project_path,
        "Add security features: input validation, rate limiting, and HTTPS support",
        "security"
    )

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python quick_enhance.py <project_path> <enhancement_type>")
        print("Enhancement types: auth, tests, optimize, secure")
        sys.exit(1)
    
    project_path = sys.argv[1]
    enhancement_type = sys.argv[2]
    
    functions = {
        "auth": quick_add_auth,
        "tests": quick_add_tests,
        "optimize": quick_optimize,
        "secure": quick_secure
    }
    
    if enhancement_type in functions:
        functions[enhancement_type](project_path)
    else:
        print(f"❌ Unknown enhancement type: {enhancement_type}")
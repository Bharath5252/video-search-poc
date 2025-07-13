#!/usr/bin/env python3
"""
Setup script for Video Search PoC

This script helps set up the environment and install dependencies.
"""

import os
import sys
import subprocess
import venv
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def create_virtual_environment():
    """Create a virtual environment if it doesn't exist."""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    print("📦 Creating virtual environment...")
    try:
        venv.create("venv", with_pip=True)
        print("✅ Virtual environment created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def install_dependencies():
    """Install required dependencies."""
    print("📥 Installing dependencies...")
    
    # Determine the pip command based on the platform
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        pip_cmd = "venv/bin/pip"
    
    try:
        # Install requirements
        result = subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def test_installation():
    """Test if the installation works correctly."""
    print("🧪 Testing installation...")
    
    # Determine the python command based on the platform
    if os.name == 'nt':  # Windows
        python_cmd = "venv\\Scripts\\python"
    else:  # Unix/Linux/macOS
        python_cmd = "venv/bin/python"
    
    try:
        # Test import
        result = subprocess.run([python_cmd, "-c", 
                               "from transcript_processor import generate_mock_transcripts; "
                               "from search_engine import VideoSearchEngine; "
                               "print('✅ All modules imported successfully')"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print(result.stdout.strip())
            return True
        else:
            print(f"❌ Import test failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error testing installation: {e}")
        return False

def print_usage_instructions():
    """Print usage instructions."""
    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")
    print("=" * 60)
    
    print("\n📖 Usage Instructions:")
    print("1. Activate the virtual environment:")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # Unix/Linux/macOS
        print("   source venv/bin/activate")
    
    print("\n2. Run the demo:")
    print("   python main.py demo")
    
    print("\n3. Run interactive mode:")
    print("   python main.py")
    
    print("\n4. Run examples:")
    print("   python example_usage.py")
    
    print("\n5. Run tests:")
    print("   python test_search.py")
    
    print("\n📚 For more information, see README.md")

def main():
    """Main setup function."""
    print("🚀 Video Search PoC - Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        sys.exit(1)
    
    # Print usage instructions
    print_usage_instructions()

if __name__ == "__main__":
    main() 
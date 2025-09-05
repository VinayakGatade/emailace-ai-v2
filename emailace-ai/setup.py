#!/usr/bin/env python3
"""
Setup script for EmailAce AI
Installs dependencies and sets up the environment
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up EmailAce AI...")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Install Python dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("❌ Failed to install Python dependencies")
        sys.exit(1)
    
    # Install Node.js dependencies
    if not run_command("npm install", "Installing Node.js dependencies"):
        print("❌ Failed to install Node.js dependencies")
        sys.exit(1)
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating .env file...")
        env_content = """# EmailAce AI Configuration
# Email Service Configuration
GMAIL_USERNAME=your-email@gmail.com
GMAIL_PASSWORD=your-app-password
OUTLOOK_USERNAME=your-email@outlook.com
OUTLOOK_PASSWORD=your-password
REPLY_EMAIL=your-reply-email@company.com

# Database Configuration
DATABASE_URL=sqlite:///./emailace.db

# AI Configuration
OPENAI_API_KEY=your-openai-api-key
HUGGINGFACE_API_KEY=your-huggingface-api-key
"""
        with open(env_file, "w") as f:
            f.write(env_content)
        print("✅ .env file created. Please update with your credentials.")
    
    # Create necessary directories
    directories = ["logs", "data", "knowledge_base"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Update .env file with your email credentials")
    print("2. Run backend: cd backend && python run.py")
    print("3. Run frontend: npm run dev")
    print("4. Visit http://localhost:3000 to see the application")
    print("\nFor Gmail setup:")
    print("- Enable 2-factor authentication")
    print("- Generate an App Password")
    print("- Use the App Password in GMAIL_PASSWORD")

if __name__ == "__main__":
    main()




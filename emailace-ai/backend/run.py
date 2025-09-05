#!/usr/bin/env python3
"""
Simple script to run the EmailAce AI Backend
"""

import uvicorn
import sys
import os

def main():
    """Main function to run the backend"""
    print("🚀 Starting EmailAce AI Backend...")
    print("📚 API Documentation: http://127.0.0.1:8000/docs")
    print("🔗 Health Check: http://127.0.0.1:8000/api/v1/")
    print("⏹️  Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        uvicorn.run(
            "main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Backend stopped by user")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()



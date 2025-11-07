#!/usr/bin/env python3
"""
Run the APOS web server.
"""

import os
import sys

def check_environment():
    """Check if environment is properly configured."""
    issues = []
    
    # Check for API key
    if not os.getenv("GOOGLE_API_KEY"):
        issues.append(
            "⚠️  GOOGLE_API_KEY not set. LLM features will not work.\n"
            "   Set it in .env file or environment variable."
        )
    
    return issues


def main():
    """Main entry point."""
    print("="*60)
    print("Advanced Prompt Optimization System (APOS)")
    print("="*60)
    
    # Check environment
    issues = check_environment()
    if issues:
        print("\nEnvironment Check:")
        for issue in issues:
            print(issue)
        print()
    
    # Try to import required modules
    try:
        from src.web.backend import main as run_server
    except ImportError as e:
        print(f"\n❌ Failed to import required modules: {e}")
        print("\nPlease install dependencies:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    
    # Run the server
    print("\nStarting web server...")
    print("Web interface will be available at: http://localhost:8000")
    print("API documentation at: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop\n")
    
    try:
        run_server()
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        sys.exit(0)


if __name__ == "__main__":
    main()

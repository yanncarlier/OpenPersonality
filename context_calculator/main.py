#!/usr/bin/env python3
"""
AI Personality System with Progressive Disclosure
Main entry point for the personality engine.
"""

import sys
from pathlib import Path
from personality_engine import PersonalityEngine


def main():
    """Main entry point for the AI personality system."""
    print("=" * 60)
    print("AI Personality System - Loading all contexts")
    print("=" * 60)
    # print()
    
    # Initialize the personality engine
    config_dir = Path("context_files")
    
    if not config_dir.exists():
        print(f"Error: Configuration directory '{config_dir}' not found.")
        print("Please create the directory and add the required files:")
        print("  - AGENT.md")
        print("  - IDENTITY.md")
        print("  - TOOLS.md")
        print("  - SOUL.md")
        print("  - HEARTBEAT.md")
        sys.exit(1)
    
    try:
        # Create personality engine
        engine = PersonalityEngine(config_dir)
        
        # Load all contexts
        engine.load_all_contexts()
        
        # Display status
        # print("\n" + "=" * 60)
        # print("FINAL STATUS")
        # print("=" * 60)
        engine.print_status()
        
        print("\n✓ All contexts loaded and processed successfully.")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please ensure all required configuration files exist.")
        sys.exit(1)
    except Exception as e:
        print(f"Error initializing personality engine: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
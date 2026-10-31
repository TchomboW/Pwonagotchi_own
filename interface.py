#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pwonagotchi_own root entrypoint. Delegates to src/interface.py."""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.interface import main_test

async def main():
    print("Pwonagotchi_own — Intelligence Engine Starting...")
    await main_test()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nEmergency shutdown initiated.")

from dotenv import load_dotenv
import os
from utils import *

def init():
    load_dotenv()
    init_log()

def main():
    log("starting main script")
    pass

if __name__ == "__main__":
    init()
    log("main init complete")
    main()
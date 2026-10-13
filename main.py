import os
import sys

from dotenv import load_dotenv

from github_api import get_profile


def main():
    load_dotenv()
    if len(sys.argv) != 2:
        print("Использование: python main.py <логин>")
        sys.exit(1)
    profile = get_profile(sys.argv[1], os.environ["GITHUB_TOKEN"])
    print(profile)


if __name__ == "__main__":
    main()

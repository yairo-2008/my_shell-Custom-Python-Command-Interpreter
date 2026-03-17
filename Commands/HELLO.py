import os

def print_user_name():
    print(f'Hello {os.environ.get("USERNAME")}')

def main():
    print_user_name()

if __name__ == "__main__":
    main()
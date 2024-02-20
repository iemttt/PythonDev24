from cowsay import cowsay

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("message", type=str)
    args = parser.parse_args()
    message = args.message
    print(cowsay(message, preset="l"))

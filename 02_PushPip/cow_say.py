from cowsay import cowsay

import argparse

PRESET_OPTIONS = {
    "b", "d"
}

def get_preset(args):
    return "".join(opt for opt in PRESET_OPTIONS if getattr(args, opt, False))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("message", type=str)
    parser.add_argument("-b", help="Borg mode", action="store_true")
    parser.add_argument("-d", help="Dead mode", action="store_true")
    args = parser.parse_args()
    preset = get_preset(args)
    message = args.message

    print(cowsay(message, preset=preset))

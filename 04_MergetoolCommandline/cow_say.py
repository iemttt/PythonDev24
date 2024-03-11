from cowsay import cowsay, cowthink, Option, list_cows, make_bubble, THOUGHT_OPTIONS

import cmd
import shlex


def parseCowOptions(arg):
    args = shlex.split(arg)
    next_is_arg = False
    opt = {
        "message": arg[0],
        "eyes": Option.eyes,
        "tongue": Option.tongue,
        "cow": "default",
    }
    for i, a in enumerate(args):
        if a == "-e":
            opt["eyes"] = args[i+1]
            next_is_arg = True
        elif a == "-t":
            opt["tongue"] = args[i+1]
            next_is_arg = True
        elif a == "-c":
            opt["cow"] = args[i+1]
            next_is_arg = True
        else:
            if not next_is_arg:
                opt["message"] = a
            next_is_arg = False
    return opt


def opt_completer(text, line, begidx, endidx):
    EYES = [Option.eyes, "@@", "aa", "TT"]
    TONGUE = [Option.tongue, "vv", "u", "U"]
    COWS = list_cows()
    cowsay_opts = {
        "-e": EYES,
        "-t": TONGUE,
        "-c": COWS
    }
    cowthink_opts = cowsay_opts
    make_bubble_opts = {
        "-b": ["cowsay", "cowthink"],
    }
    all_opts = {
        "cowsay": cowsay_opts,
        "cowthink": cowthink_opts,
        "make_bubble": make_bubble_opts
    }
    args = shlex.split(line)
    command = args[0]
    if begidx == endidx:
        opt = args[-1]
    else:
        opt = args[-2]
    return [s for s in all_opts[command][opt] if s.startswith(text)]


class CowSay(cmd.Cmd):
    '''
    Cowsay in command line
    '''
    prompt = "CowSay>"

    def do_cowsay(self, arg):
        '''
        cowsay message [-e eye_string] [-t tongue_string] [-c cow]
        
        Print cow says your message
        '''
        opt = parseCowOptions(arg)
        print(
            cowsay(
                message=opt["message"],
                eyes=opt["eyes"],
                tongue=opt["tongue"],
                cow=opt["cow"],
            )
        )
    
    def complete_cowsay(self, text, line, begidx, endidx):
        return opt_completer(text, line, begidx, endidx)

    def do_cowthink(self, arg):
        '''
        cowthink message [-e eye_string] [-t tongue_string] [-c cow]
        
        Print cow thinking about your message
        '''
        opt = parseCowOptions(arg)
        print(
            cowthink(
                message=opt["message"],
                eyes=opt["eyes"],
                tongue=opt["tongue"],
                cow=opt["cow"],
            )
        )
    
    def complete_cowthink(self, text, line, begidx, endidx):
        return opt_completer(text, line, begidx, endidx)


    def do_list_cows(self, _):
        '''
        list_cows prints all cow options
        '''
        print(*list_cows())
    
    def do_make_bubble(self, arg):
        '''
        make_bubble message [-b <brackets>] [-w width] [-n]
        
        Print message in bubble
        
        -b can be only "cowsay" or "cowthink
        -w needs integer value
        -n flag to not wrap text
        '''
        args = shlex.split(arg)
        brackets_options = ["cowsay", "cowthink"]
        brackets = "cowsay"
        width = 40
        wrap_text = True
        message = arg[0]
        next_is_arg = False
        for i, a in enumerate(args):
            if a == "-b":
                if args[i+1] in brackets_options:
                    brackets = args[i+1]
                else:
                    print(f"-b options: {shlex.quote(shlex.join(brackets_options))}")
                    return
                next_is_arg = True
            elif a == "-w":
                try:
                    width = int(args[i+1])
                except ValueError:
                    print("-w needs integer value")
                    return
                next_is_arg = True
            elif a == "-n":
                wrap_text == False
            else:
                if not next_is_arg:
                    message = a
                next_is_arg = False
        print(
            make_bubble(
                message,
                brackets=THOUGHT_OPTIONS[brackets],
                width=width,
                wrap_text=wrap_text
            )
        )
    
    def complete_make_bubble(self, text, line, begidx, endidx):
        return opt_completer(text, line, begidx, endidx)


if __name__ == '__main__':
    CowSay().cmdloop()

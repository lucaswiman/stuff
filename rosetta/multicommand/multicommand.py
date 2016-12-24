#!/usr/bin/env python3
import sys
import subprocess


def main(cmd_file):
    with open(cmd_file, 'r') as f:
        commands = [line.strip() for line in f if line.strip()]
    processes = []
    for command in commands:
        processes.append(subprocess.Popen(command.split(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT))
    fail = False
    for p in processes:
        retcode = p.wait()
        if retcode != 0:
            fail = True
            sys.stdout.buffer.write(p.stdout.read())
    return int(fail)
        
    


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))

#! ./bin/python3
import sys
import command

"""
run with the following syntax
command <app_name> <task_type> <args>
"""


def main():
    if len(sys.argv) == 1:
        command.Command('summary', '', '', build=True).dispatch()
    if sys.argv[1] in command.cmds:
        parsed_args = command.parse_argv(sys.argv)
        cmd = command.Command(*parsed_args)
        cmd.build()
        cmd.dispatch()
    else:
        raise ValueError('{} is not a supported command'.format(sys.argv[1]))

if __name__ == '__main__':
    main()
    sys.exit(0)

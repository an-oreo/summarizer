#! ./bin/python3
import sys

import apis

import command

"""
run with the following syntax
command <app_name> <task_type> <args>
"""


def main():
    if len(sys.argv) == 1:
        command.cmd_funcs.print_summary()
    elif sys.argv[1] in command.cmds:
        parsed_args = command.parse_argv(sys.argv)
        cmd = command.Command(*parsed_args)
        cmd.build()
        cmd.dispatch()
    else:
        raise ValueError('{} is not a supported command'.format(sys.argv[1]))

    # elif sys.argv[1] == 'task':
    #     todoist = apis.Todoist()
    #     if sys.argv[2] == 'add':
    #         todoist.quick_add(sys.argv[3])
    #     elif sys.argv[2] == 'finish':
    #         todoist.complete_task(sys.argv[3])
    #     elif sys.argv[2] == 'list':
    #         command._list_todoist_tasks(todoist)
    #
    # elif sys.argv[1] == 'time':
    #     timer = apis.Timer()
    #     if sys.argv[2] == 'start':
    #         timer.start(sys.argv[3])
    #     if sys.argv[2] == 'stop':
    #         timer.stop()
    #
    # elif sys.argv[1] == 'mail':
    #     print('Not implemented!')
    #
    # elif sys.argv[1] == 'cal':
    #     calendar = apis.Calendar()
    #     if sys.argv[2] == 'add':
    #         calendar.add(sys.argv[3])
    #     elif sys.argv[2] == 'list':
    #         command._list_calender(calendar)
    #
    # elif sys.argv[1] == 'help':
    #     command._print_help()

if __name__ == '__main__':
    main()

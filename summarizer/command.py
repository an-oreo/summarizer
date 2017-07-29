#! /usr/bin/env python
# vim:fileencoding=utf-8
# -*- coding: utf-8 -*-
"""
summarizer
command.py
Author: Danyal Ahsanullah
Date: 7/28/2017
License: N/A
Description:
    Module that handles generic handling of tasks for cli tool.
    built off the use syntax of:
        <app_name> <task_type> <args>
"""

import apis as _apis
import cmd_funcs as _cmd_funcs
from itertools import repeat as _repeat
from argparse import ArgumentParser as _ArgumentParser


# Exceptions
class ApiImportError(Exception):
    """raised when api is improperly imported"""


class TaskError(Exception):
    """raised when task is not found"""


class ParseError(Exception):
    """raised when parse_argv fails"""

# util stuff

# _parser to separate parts of command. outside func to prevent recreation of _parser
_parser = _ArgumentParser()
_parser.add_argument('app_name', type=str, action='store', default='', nargs=1)
_parser.add_argument('task_type', type=str, action='store', default='', nargs=1)
# _parser.add_argument('args', type=str, action='store', nargs='*')


def parse_argv(argv):
    args = argv
    args.pop(0)  # remove path from local temp copy of sys.argv
    # print(args)
    if len(args) >= 1:
        # pad to be at least 3 long
        args.extend(_repeat('', 3 - len(args)))
        # print(args)
        try:
            parsed, args = _parser.parse_known_args(args)
            return parsed.app_name[0], parsed.task_type[0], args
        except Exception as e:
            print(e)
            raise ParseError('failed to parse args:{}'.format(args))
    else:
        raise ParseError('failed to parse args:{}'.format(args))


# set of acceptable command strings
# used primarily for preliminary input validation
# todo: maybe a frozenset?
cmds = {'summary',
        'task',
        'time',
        'cal',
        'mail',
        'help',
        }

# mapping for commands to appropriate command functions
# command functions are left in the cmd_funcs module
_cmd_dict = {'summary': 'print_summary',
             'help': 'print_help',
             'mail': 'not_implemented',
             }

# mapping for commands to appropriate api objects
# used with _task_dict to accomplish api object instantiation and function call
_api_dict = {'task': 'Todoist',
             'time': 'Timer',
             'cal': 'Calendar',
             'mail': 'Gmail',
             }

# mapping for task function calls
# are mapped to either the name of api functions or command actions
# command actions are foudn in the cmd_funcs module
_task_dict = {'task_add': 'quick_add',
              'task_finish': 'complete_task',
              'task_list': 'list_tasks',  # command action
              'time_start': 'start',
              'time_stop': 'stop',
              'time_current_timer': 'current_timer',
              'cal_add': 'add',
              'cal_list': 'list_calander',  # command action
              }


class Command:
    """
    Command object to prepare and execute commands
    """
    def __init__(self, app_name, task_type, args, build=False):
        self.app_name = app_name
        self.task_type = task_type
        self.args = list(filter(None, args))
        self._api = None
        self._task = lambda vals: print(vals)
        if build:
            self.build()

    def build(self):
        if self.app_name in _cmd_dict:
            self._task = self._get_task()
        elif self.app_name in _api_dict:
            # ALWAYS call 'self._get_api()' BEFORE 'self._get_task()'
            # this is due to get_tasks checking if an api object exists before searching  to the cmd task list
            self._api = self._get_api()
            self._task = self._get_task()
        else:
            raise ValueError('command: {} is not recognised.'.format(self.app_name))

    def dispatch(self):
        if self.args:
            self._task(*self.args)
        else:
            # noinspection PyArgumentList
            self._task()

    def _get_api(self):
        try:
            return getattr(_apis, _api_dict[self.app_name])()
        except AttributeError:
            raise ApiImportError('Failed to get API: {}'.format(_api_dict[self.app_name]))
        except KeyError:
            raise ApiImportError('No API mapping exists for App Name: {}'.format(self.app_name))

    def _get_task(self):
        if self._api:
            try:
                return getattr(self._api, _task_dict[self._name_hash()])
            except AttributeError:
                raise TaskError('failed to get api function')
        elif self.app_name in _cmd_dict:
            try:
                return getattr(_cmd_funcs, _cmd_dict[self.app_name])
            except AttributeError:
                raise TaskError('failed to get task function')
        else:
            raise TaskError('failed to get task.')

    def _name_hash(self):
        return '{}_{}'.format(self.app_name, self.task_type)


if __name__ == '__main__':
    import sys
    # _print_help()
    sys.exit(0)

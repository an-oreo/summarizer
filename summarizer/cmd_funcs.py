#! /usr/bin/env python
# vim:fileencoding=utf-8
# -*- coding: utf-8 -*-
"""
summarizer
cmd_funcs.py
Author: Danyal Ahsanullah
Date: 7/28/2017
License: N/A
Description:
    here the actions that require more than a simple api call are put.
    actions that don't require an api call are als put here.
"""
import apis as _apis
import itertools as _itertools

'''
util funcs not needed outside module
'''


def _pairwise(iterable):
    """"s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = _itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


'''
modify below to support desired functionality
'''


def not_implemented():
    raise NotImplementedError('Feature is not yet implemented!')


def print_help(task=None):
    help_dict = {'task': 'add finish list',
                 'time': 'start stop',
                 'cal': 'add list',
                 }
    if task is None:
        for key in help_dict:
            print('{} {{{}}}'.format(key, help_dict[key]))
    else:
        print('{} {{{}}}'.format(task, help_dict[task]))


def print_summary():
    list_todoist_tasks(_apis.Todoist())
    timer_summary(_apis.Timer())
    list_unread_email(_apis.Gmail())
    list_calender(_apis.Calendar())


def timer_summary(timer):
    current_timer = timer.current_timer()
    if current_timer:
        print('Current timer is: ' + current_timer)


def list_unread_email(mail):
    num_unread = mail.get_num_unread()
    for email, num in num_unread.items():
        print(num + ' unread messages in email ' + email)


def list_calender(calendar):
    for event in calendar.get_today_schedule():
        calendar.print_event(event)


def list_todoist_tasks(todoist):
    for task in todoist.get_all_tasks():
        todoist.print_task(task)

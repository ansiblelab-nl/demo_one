#!/usr/bin/python
# Make coding more python3-ish, this is required for contributions to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.callback import CallbackBase

DOCUMENTATION = '''
    callback: status
    description: show status of playbook run.
'''


class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_NAME = 'status'
    CALLBACK_NEEDS_WHITELIST = True

    def __init__(self):
        super(CallbackModule, self).__init__()

    def v2_playbook_on_start(self, playbook):
        self.playbook = playbook
        print(dir(playbook))

    def v2_playbook_on_play_start(self, play):
        print(dir(play))

    def v2_runner_on_ok(self, result):
        print(dir(result))
        print('On a succesfull task:\nTask name: %s\nTask result: %s\n' %
              (result.task_name, result._result))

    def v2_runner_on_failed(self, taskresult):
        print(dir(taskresult))

    def v2_runner_on_unreachable(self, taskresult):
        print(dir(taskresult))

    def v2_playbook_on_stats(self, stats):
        hosts = sorted(stats.processed.keys())
        print(dir(stats))
        print(stats.__dict__)
        for host in hosts:
            print(stats.summarize(host))

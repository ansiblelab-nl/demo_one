#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, Ton Kersten
# GNU General Public License v3.0
# see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt
#
"""Let the Cow Say it.

Lookup plugin that does Cowsay without installing the Cowsay executable.
"""

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
import re
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '0.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
  lookup: cowsay
  short_description: Return cowsay
  author:
    - Ton Kersten <tonk@smartowl.nl>
  version_added: "2.7"
  description:
    - Return a Cowsay formatted text
  options:
    text:
      description: String to convert to cowsay
      type: str
      required: True
  variables:
    sysinfo:
      description: System information to display behind the cow
      type: list
      required: False

'''

EXAMPLES = r'''
- name: Generate the motd
  copy:
    dest: /etc/motd
    owner: root
    group: root
    mode: '0644'
    content: "{{ lookup('cowsay', 'Say: Hello World', sysinfo=sysinfo) }}"
  vars:
    sysinfo:
      - Hostname    = {{ ansible_facts['hostname'] }}
      - Host alias  = Hammerboy
      - Function    = Test lab
      - Location    = Local machine
      - IP address  = {{ ansible_facts['default_ipv4']['address'] }}
      - VMware name = ansilan01

- name: Just let the Cow say Mhoow!
  copy:
    dest: /etc/motd
    owner: root
    group: root
    mode: '0644'
    content: "{{ lookup('cowsay', 'Mhoow!') }}"
'''

RETURN = r'''
message:
    description: The output message from the Cow
    type: str
    returned: always
'''

cow = r'''
\   ^__^
 \  (oo)\_______
    (__)\       )\/\
        ||----w |
        ||     ||
'''


def wrap_lines(lines, max_width=49):
    """Wrap bubble lines if they are longer than max_width."""
    new_lines = []
    for line in lines:
        for line_part in [
            line[i:i+max_width] for i in range(0, len(line), max_width)
        ]:
            new_lines.append(line_part)
    return new_lines


def generate_bubble(text):
    """Generate the bubble text."""
    lines = [line.strip() for line in str(text).split("\n")]
    lines = wrap_lines([line for line in lines if line])
    text_width = max([len(line) for line in lines])
    output = []
    output.append(" _" + "_" * (text_width+1))
    if len(lines) > 1:
        output.append(" /" + " " * text_width + "\\")
    for line in lines:
        output.append("< " + line + " " * (text_width - len(line) + 1) + ">")
    if len(lines) > 1:
        output.append(" \\" + " " * text_width + "/")
    output.append(" -" + "-" * (text_width+1))
    return output


def generate_char(text_width):
    """Generate the cow without the bubble."""
    output = []
    char_lines = cow.split('\n')
    char_lines = [i for i in char_lines if len(i) != 0]
    for line in char_lines:
        output.append(' ' * max(int(text_width/2), 2) + line)
    return output


def draw(text):
    """Put the bubble and the cow together."""
    if len(re.sub('\s', '', text)) == 0:
        raise Exception('Pass something meaningful to cowsay')
    output = generate_bubble(text)
    text_width = max([len(line) for line in output]) - 4  # 4 is the frame
    output += generate_char(text_width)
    cow_width = max([len(line) for line in output]) + 1 # One extra space
    return cow_width, output


display = Display()

class LookupModule(LookupBase):
    def run(self, terms, variables, **kwargs):
        ret = ""

        # Get the system information list
        try:
            sysinfo = kwargs['sysinfo']
        except (NameError, KeyError):
            sysinfo = []

        # Check if it is a list
        if not isinstance(sysinfo, list):
            raise AnsibleError("sysinfo should be a list")

        # Get the width and the cow
        width, cow = draw(terms[0])
        for i, line in enumerate(cow):
            if i == 0 or i == len(cow)-1:
                # Skip the first and lastline of the cow
                ret += line + '\n'
            else:
                try:
                    info = sysinfo[i-1]
                except IndexError:
                    info = ""
                if info:
                    ret += "{1:{0}} | {2}\n".format(width, line, info)
                else:
                    ret += "{0}\n".format(line)

        return [ret]

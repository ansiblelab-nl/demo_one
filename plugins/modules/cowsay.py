#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, Ton Kersten
# GNU General Public License v3.0
# see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt
#
"""Let the Cow Say it.

Module that does Cowsay without installing the Cowsay executable.
"""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

# All imports
import re
from ansible.errors import AnsibleError
from ansible.module_utils.basic import AnsibleModule

ANSIBLE_METADATA = {'metadata_version': '0.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
  module: cowsay
  short_description: Return cowsay
  author:
    - Ton Kersten <tonk@smartowl.nl>
  version_added: "2.7"
  description:
    - Return a Cowsay formatted text
  notes:
    - When in check mode, this module pretends to have done things
      and returns C(changed = True).
  options:
    text:
      description: String to convert to cowsay
      type: str
      required: True
'''

EXAMPLES = r'''
- name: Do the Cow
  cowsay:
    text: The Cow says Mhoow
  register: cowsaid
  delegate_to: localhost
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
    new_lines = []
    for line in lines:
        for line_part in [
            line[i:i+max_width] for i in range(0, len(line), max_width)
        ]:
            new_lines.append(line_part)
    return new_lines


def generate_bubble(text):
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
    output = []
    char_lines = cow.split('\n')
    char_lines = [i for i in char_lines if len(i) != 0]
    for line in char_lines:
        output.append(' ' * max(int(text_width/2), 2) + line)
    return output


def draw(text):
    if len(re.sub('\s', '', text)) == 0:
        raise Exception('Pass something meaningful to cowsay')
    output = generate_bubble(text)
    text_width = max([len(line) for line in output]) - 4  # 4 is the frame
    output += generate_char(text_width)
    return output


def run_module():
    """Run Ansible module."""
    # Define module options
    module_args = dict(text=dict(type='str', required=True))

    # Start with an empty result
    result = {
        'changed': False,
        'message': ''
    }

    # Init the module
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # In check_mode pretend it did something
    if module.check_mode:
        module.exit_json(**result)

    # Get all module options
    text = module.params['text']

    # Execute "cow" function
    result['message'] = draw(text)

    # return collected results
    result['changed'] = False

    # Return the beast
    module.exit_json(**result)


def main():
    """Start here."""
    run_module()


if __name__ == '__main__':
    main()

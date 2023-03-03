from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = """
    module: welcome
    description: Ansible demo module
"""


def run_module():

    module_args = dict(
        # day=dict(type='str', required=True),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    result = dict(changed=False, msg="Bienvenue")
    module.exit_json(**result)


if __name__ == "__main__":
    run_module()

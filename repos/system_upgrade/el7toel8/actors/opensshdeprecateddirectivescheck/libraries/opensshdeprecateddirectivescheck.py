from leapp import reporting


LIST_SEPARATOR_FMT = '\n    - '


def inhibit_if_deprecated_directives_used(ssh_config_msg):
    """ Inhibits the upgrade if any deprecated directives were found in the sshd configuration. """

    if ssh_config_msg.deprecated_directives:
        # Prepare the output of the deprecated directives for the user
        deprecated_directives_report_text = ''
        for deprecated_directive in ssh_config_msg.deprecated_directives:
            deprecated_directives_report_text += '{0}{1}'.format(LIST_SEPARATOR_FMT, deprecated_directive)

        reporting.create_report([
            reporting.Title('A deprecated directive in the sshd configuration'),
            reporting.Summary(
                'The following deprecated directives were found in the sshd configuration:{0}'
                .format(deprecated_directives_report_text)
            ),
            reporting.Severity(reporting.Severity.HIGH),
            reporting.Tags([reporting.Tags.SERVICES]),
            reporting.Flags([reporting.Flags.INHIBITOR]),
            reporting.Remediation(hint='Remove the deprecated directives from the sshd configuration.')
        ])

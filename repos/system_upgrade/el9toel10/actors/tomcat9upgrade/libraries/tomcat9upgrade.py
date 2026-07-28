from leapp.libraries.common.config.version import matches_target_version
from leapp.libraries.common.rpms import has_package
from leapp.libraries.stdlib import api
from leapp.models import DistributionSignedRPM, RpmTransactionTasks

# Pairs of (rhel9_package, rhel10_replacement)
TOMCAT_PACKAGE_MAP = [
    ('tomcat', 'tomcat9'),
    ('tomcat-el-3.0-api', 'tomcat9-el-3.0-api'),
    ('tomcat-jsp-2.3-api', 'tomcat9-jsp-2.3-api'),
    ('tomcat-lib', 'tomcat9-lib'),
    ('tomcat-servlet-4.0-api', 'tomcat9-servlet-4.0-api'),
    ('tomcat-webapps', 'tomcat9-webapps'),
    ('tomcat-docs-webapp', 'tomcat9-docs-webapp'),
    ('tomcat-admin-webapps', 'tomcat9-admin-webapps'),
]


def _get_transaction_tasks():
    """
    Return (to_install, to_remove) for each installed RHEL 9 tomcat package.
    """
    to_install = []
    to_remove = []
    for old_pkg, new_pkg in TOMCAT_PACKAGE_MAP:
        if has_package(DistributionSignedRPM, old_pkg):
            to_remove.append(old_pkg)
            to_install.append(new_pkg)
    return to_install, to_remove


def process():
    if not matches_target_version('<= 10.2'):
        api.current_logger().debug('Target version is greater than 10.2 - tomcat will not be replaced with tomcat9.')
        return
    to_install, to_remove = _get_transaction_tasks()
    if not to_install:
        api.current_logger().debug('No installed tomcat RHEL 9 packages found; skipping.')
        return
    api.current_logger().info(
        'Scheduling tomcat package replacement: removing {} and installing {}.'.format(to_remove, to_install)
    )
    api.produce(RpmTransactionTasks(to_install=to_install, to_remove=to_remove))

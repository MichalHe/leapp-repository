import pytest

from leapp.libraries.actor import tomcat9upgrade
from leapp.libraries.common.testutils import CurrentActorMocked, produce_mocked
from leapp.libraries.stdlib import api
from leapp.models import DistributionSignedRPM, RPM, RpmTransactionTasks


def _make_rpm(name):
    return RPM(
        name=name,
        version='0.1',
        release='1.el9',
        epoch='0',
        pgpsig='RSA/SHA256, Mon 01 Jan 1970 00:00:00 AM -03, Key ID 199e2f91fd431d51',
        packager='Red Hat, Inc. <http://bugzilla.redhat.com/bugzilla>',
        arch='noarch',
    )


@pytest.mark.parametrize('installed,expected_install,expected_remove', [
    (
        [
            'tomcat',
            'tomcat-el-3.0-api',
            'tomcat-jsp-2.3-api',
            'tomcat-lib',
            'tomcat-servlet-4.0-api',
            'tomcat-webapps',
            'tomcat-docs-webapp',
            'tomcat-admin-webapps'
        ],
        [
            'tomcat9',
            'tomcat9-el-3.0-api',
            'tomcat9-jsp-2.3-api',
            'tomcat9-lib',
            'tomcat9-servlet-4.0-api',
            'tomcat9-webapps',
            'tomcat9-docs-webapp',
            'tomcat9-admin-webapps'
        ],
        [
            'tomcat',
            'tomcat-el-3.0-api',
            'tomcat-jsp-2.3-api',
            'tomcat-lib',
            'tomcat-servlet-4.0-api',
            'tomcat-webapps',
            'tomcat-docs-webapp',
            'tomcat-admin-webapps'
        ],
    ),
    (
        ['tomcat'],
        ['tomcat9'],
        ['tomcat'],
    ),
    (
        ['tomcat-el-3.0-api', 'tomcat-lib'],
        ['tomcat9-el-3.0-api', 'tomcat9-lib'],
        ['tomcat-el-3.0-api', 'tomcat-lib'],
    ),
    (
        [],
        [],
        [],
    ),
])
def test_get_transaction_tasks(monkeypatch, installed, expected_install, expected_remove):
    rpms = [_make_rpm(name) for name in installed] + [_make_rpm('httpd')]
    monkeypatch.setattr(api, 'current_actor', CurrentActorMocked(
        src_ver='9.6',
        dst_ver='10.2',
        msgs=[DistributionSignedRPM(items=rpms)],
    ))

    to_install, to_remove = tomcat9upgrade._get_transaction_tasks()

    assert to_install == expected_install
    assert to_remove == expected_remove


def test_process_skips_when_target_version_above_10_2(monkeypatch):
    rpms = [_make_rpm('tomcat')]
    monkeypatch.setattr(api, 'current_actor', CurrentActorMocked(
        src_ver='9.6',
        dst_ver='10.3',
        msgs=[DistributionSignedRPM(items=rpms)],
    ))
    monkeypatch.setattr(api, 'produce', produce_mocked())

    tomcat9upgrade.process()

    assert not api.produce.called

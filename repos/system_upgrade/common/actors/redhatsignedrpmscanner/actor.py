from leapp.actors import Actor
from leapp.libraries.common import rhui
from leapp.models import InstalledRedHatSignedRPM, InstalledRPM, InstalledUnsignedRPM
from leapp.tags import FactsPhaseTag, IPUWorkflowTag


class RedHatSignedRpmScanner(Actor):
    """Provide data about installed RPM Packages signed by Red Hat.

    After filtering the list of installed RPM packages by signature, a message
    with relevant data will be produced.
    """

    name = 'red_hat_signed_rpm_scanner'
    consumes = (InstalledRPM,)
    produces = (InstalledRedHatSignedRPM, InstalledUnsignedRPM,)
    tags = (IPUWorkflowTag, FactsPhaseTag)

    def process(self):
        RH_SIGS = ['199e2f91fd431d51',
                   '5326810137017186',
                   '938a80caf21541eb',
                   'fd372689897da07a',
                   '45689c882fa658e0']

        signed_pkgs = InstalledRedHatSignedRPM()
        unsigned_pkgs = InstalledUnsignedRPM()

        env_vars = self.configuration.leapp_env_vars
        # if we start upgrade with LEAPP_DEVEL_RPMS_ALL_SIGNED=1, we consider
        # all packages to be signed
        all_signed = [
            env
            for env in env_vars
            if env.name == 'LEAPP_DEVEL_RPMS_ALL_SIGNED' and env.value == '1'
        ]

        def has_rhsig(pkg):
            return any(key in pkg.pgpsig for key in RH_SIGS)

        def is_gpg_pubkey(pkg):
            """Check if gpg-pubkey pkg exists or LEAPP_DEVEL_RPMS_ALL_SIGNED=1

            gpg-pubkey is not signed as it would require another package
            to verify its signature
            """
            return (    # pylint: disable-msg=consider-using-ternary
                    pkg.name == 'gpg-pubkey'
                    and pkg.packager.startswith('Red Hat, Inc.')
                    or all_signed
            )

        def has_katello_prefix(pkg):
            """Whitelist the katello package."""
            return pkg.name.startswith('katello-ca-consumer')

        upg_path = rhui.get_upg_path()
        # AWS RHUI packages do not have to be whitelisted because they are signed by RedHat
        whitelisted_cloud_flavours = ('azure', 'azure-eus', 'azure-sap-ha', 'azure-sap-apps', 'google', 'google-sap')
        whitelisted_cloud_pkgs = {
            rhui.RHUI_CLOUD_MAP[upg_path].get(flavour, {}).get('src_pkg') for flavour in whitelisted_cloud_flavours
        }
        whitelisted_cloud_pkgs.update(
            rhui.RHUI_CLOUD_MAP[upg_path].get(flavour, {}).get('target_pkg') for flavour in whitelisted_cloud_flavours
        )
        whitelisted_cloud_pkgs.update(
            rhui.RHUI_CLOUD_MAP[upg_path].get(flavour, {}).get('leapp_pkg') for flavour in whitelisted_cloud_flavours
        )

        for rpm_pkgs in self.consume(InstalledRPM):
            for pkg in rpm_pkgs.items:
                if any(
                    [
                        has_rhsig(pkg),
                        is_gpg_pubkey(pkg),
                        has_katello_prefix(pkg),
                        pkg.name in whitelisted_cloud_pkgs,
                    ]
                ):
                    signed_pkgs.items.append(pkg)
                    continue

                unsigned_pkgs.items.append(pkg)

        self.produce(signed_pkgs)
        self.produce(unsigned_pkgs)

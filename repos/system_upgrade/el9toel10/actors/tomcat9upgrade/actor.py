from leapp.actors import Actor
from leapp.libraries.actor import tomcat9upgrade
from leapp.models import DistributionSignedRPM, RpmTransactionTasks
from leapp.tags import FactsPhaseTag, IPUWorkflowTag


class Tomcat9Upgrade(Actor):
    """
    Replace RHEL 9 tomcat packages with their RHEL 10 equivalents in the upgrade transaction.

    For each RHEL 9 tomcat package that is installed (tomcat, tomcat-lib,
    tomcat-el-3.0-api, tomcat-jsp-2.3-api, tomcat-servlet-4.0-api), schedules
    the corresponding RHEL 10 package (tomcat9, tomcat9-lib, etc.) for
    installation and the RHEL 9 package for removal.
    """

    name = 'tomcat9_upgrade'
    consumes = (DistributionSignedRPM,)
    produces = (RpmTransactionTasks,)
    tags = (FactsPhaseTag, IPUWorkflowTag)

    def process(self):
        tomcat9upgrade.process()

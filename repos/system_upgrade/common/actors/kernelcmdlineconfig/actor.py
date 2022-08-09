import os

from leapp.actors import Actor
from leapp.exceptions import StopActorExecutionError
from leapp.libraries.actor import kernelcmdlineconfig
from leapp.models import FirmwareFacts, InstalledTargetKernelVersion, KernelCmdlineArg, TargetKernelCmdlineArgTasks
from leapp.tags import FinalizationPhaseTag, IPUWorkflowTag


class KernelCmdlineConfig(Actor):
    """
    Append extra arguments to the target RHEL kernel command line
    """

    name = 'kernelcmdlineconfig'
    consumes = (KernelCmdlineArg, InstalledTargetKernelVersion, FirmwareFacts, TargetKernelCmdlineArgTasks)
    produces = ()
    tags = (FinalizationPhaseTag, IPUWorkflowTag)

    def process(self):

        configs = None
        ff = next(self.consume(FirmwareFacts), None)
        if not ff:
            raise StopActorExecutionError(
                'Could not identify system firmware',
                details={'details': 'Actor did not receive FirmwareFacts message.'}
            )

        if ff.firmware == 'bios' and os.path.ismount('/boot/efi'):
            configs = ['/boot/grub2/grub.cfg', '/boot/efi/EFI/redhat/grub.cfg']
        kernelcmdlineconfig.modify_kernel_args_in_boot_configs(configs)

# Libraries and API
Leapp-repository includes several libraries providing common useful
functionality available to all actors. These libraries cover key areas crucial
to the upgrade process such as (safely) creating various system mounts,
determining kernel version and its flavour (e.g., realtime), parsing reporfiles,
etc. Naturally, one could always introduce his/hers own solution, however,
the repository's bundled libraries are maintained by leapp, and, Leapp's maintainers
provide fixes when a bug is found, or something critical changes (e.g., kernel
naming scheme) in the underlying system, breaking the implementation. This
section provides an overview of the most useful libraries leapp-repository
provides.


## An exhaustive list of useful libraries
Note that some internal libraries have been excluded as they are unlikely to be useful for developers
other than maintainers. 

| File                    | Summary                                                                                                                                                |
|---------------------    |--------                                                                                                                                                |
|`config/__init__.py`     | reading leapp's environmental vars, getting product type                                                                                               |
|`config/architecture.py` | providing constants abstracting concrete arch names, allows querying source system arch                                                                |
|`config/version.py`      | accessing source/target system major/minor versions                                                                                                    |
|`dnfplugin.py`           | allows installing packages into initramfs                                                                                                              |
|`grub.py`                | identifying block device path containing /boot, checking whether disk has grub                                                                         |
|`guards.py`              | ensuring that the system has enough disk space and can make a connection                                                                               |
|`kernel.py`              | extracting uname provided by kernel RPM, identifying kernel's RPM from uname                                                                           |
|`mdraid.py`              | checking whether device is mdraid, listing component devices for multiple device array                                                                 |
|`module.py`              |  listing DNF modulestream modules, enabled_modulues, mapping RPMs to module+streams                                                                    |
|`mounting.py`            |  providing context managers creating and safely removing various mount types                                                                           |
|`overlaygen.py`          |  implementing source system overlay                                                                                                                    |
|`persistentnetnames.py`  | listing physical network devices with their `udev` attributes                                                                                          |
|`repofileutils.py`       | listing what repo files are present, parsing their content                                                                                             |
|`rhsm.py`                | listing attached SKUs; reading RHSM status, available repos, setting and unsetting release                                                             |
|`rhui.py`                | leapp knowledge supported RHUI setups found on various cloud systems                                                                                   |
|`rpms.py`                | checking whether a package is installed, check whether a file owned by an RPM has been modified                                                        |
|`systemd.py`             | enabling/disabling units, listing service files, listing service preset files                                                                          |
|`testutils.py`           | various unilities solving common problems when developing unit tests for an actor                                                                      |
|`utils.py`               | various utilities, e.g., INI config parser that is indepented of python version, or calling commands with OSError converted to StopActorExecutionError |

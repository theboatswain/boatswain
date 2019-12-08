from boatswain.common.models.audit import Audit
from boatswain.common.models.audit_update import AuditUpdate
from boatswain.common.models.group import Group
from boatswain.common.models.workspace import Workspace

from boatswain.common.models.preference import Preference

from boatswain.common.models.configurations import Configuration
from boatswain.common.models.preferences_shortcut import PreferencesShortcut

from boatswain.common.models.tag import Tag

from boatswain.common.models.container import Container
from boatswain.common.models.environment import Environment
from boatswain.common.models.port_mapping import PortMapping
from boatswain.common.models.volume_mount import VolumeMount

db_tables = [Container, Environment, PortMapping, VolumeMount, Tag, Configuration, PreferencesShortcut,
             Preference, Workspace, Group, Audit, AuditUpdate]

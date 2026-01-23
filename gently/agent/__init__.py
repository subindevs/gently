"""
Conversational Microscopy Copilot

AI agent for microscopy experiment orchestration. Backend-agnostic —
works with any hardware that implements the MicroscopeBackend protocol.
"""

from .copilot import MicroscopyCopilot
from .state import EmbryoState, ExperimentState, ImageRecord
from .plan_synthesis import PlanSynthesizer, PlanValidator
from .image_manager import ImageManager
from .perception import PerceptionManager, PerceptionResult, PerceptionSession
from .rich_cli import run_rich_cli, RichCopilotCLI
from .autocomplete import create_completer, CopilotCompleter
from .tool_registry import ToolRegistry, get_tool_registry, tool, ToolCategory

# Temporary: keep client imports until agent is fully refactored to use MicroscopeBackend
from .microscope_client import MicroscopeClient
from .queue_server_client import QueueServerClient

# Import tools package to register all tools
from . import tools

__all__ = [
    'MicroscopyCopilot',
    'EmbryoState',
    'ExperimentState',
    'ImageRecord',
    'PlanSynthesizer',
    'PlanValidator',
    'ImageManager',
    # Perception system
    'PerceptionManager',
    'PerceptionResult',
    'PerceptionSession',
    'run_rich_cli',
    'RichCopilotCLI',
    'create_completer',
    'CopilotCompleter',
    # Tool registry
    'ToolRegistry',
    'get_tool_registry',
    'tool',
    'ToolCategory',
    # Temporary: will be replaced by MicroscopeBackend
    'MicroscopeClient',
    'QueueServerClient',
]

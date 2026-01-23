"""
Gently - AI Agent for Microscopy
=================================

A backend-agnostic AI agent for microscopy experiment orchestration.
Works with any hardware backend that implements the MicroscopeBackend protocol.

Key Components:
    - interface: MicroscopeBackend protocol for hardware abstraction
    - agent: Copilot AI for experiment orchestration and decision-making
    - analysis: Focus scoring and image analysis utilities
    - coordinates: Coordinate transformations for pixel/stage conversions
    - core: Event bus, data store, and service infrastructure
    - visualization: Web-based experiment visualization
"""

# The abstract hardware interface
from .interface import MicroscopeBackend

# Core infrastructure
from .core import (
    TiledStore,
    DatabrokerStore,
    EventBus,
    EventType,
    get_event_bus,
    get_data_store,
)

# Coordinate utilities
try:
    from .coordinates import (
        pixel_to_stage_position,
        stage_to_pixel_position,
        pixel_displacement_to_stage_movement,
        get_um_per_pixel,
        DEFAULT_PIXEL_SIZE_UM,
        DEFAULT_OBJECTIVE_MAG,
    )
    _COORDINATES_AVAILABLE = True
except ImportError:
    _COORDINATES_AVAILABLE = False

# Analysis utilities
try:
    from .analysis.core import (
        FocusAnalysisConfig,
        FocusResult,
        FocusAlgorithm,
        FitFunction,
        calculate_focus_score,
        analyze_focus_stack,
        fit_focus_curve,
    )
    _ANALYSIS_AVAILABLE = True
except ImportError:
    _ANALYSIS_AVAILABLE = False

# Main entry point
from .gently import Gently, create_gently

__version__ = "0.4.0"
__all__ = [
    # Interface
    "MicroscopeBackend",

    # Main entry point
    "Gently",
    "create_gently",

    # Core infrastructure
    "TiledStore",
    "DatabrokerStore",
    "EventBus",
    "EventType",
    "get_event_bus",
    "get_data_store",

    # Analysis
    "FocusAnalysisConfig",
    "FocusResult",
    "FocusAlgorithm",
    "FitFunction",
    "calculate_focus_score",
    "analyze_focus_stack",
    "fit_focus_curve",

    # Coordinates
    "pixel_to_stage_position",
    "stage_to_pixel_position",
    "pixel_displacement_to_stage_movement",
    "get_um_per_pixel",
    "DEFAULT_PIXEL_SIZE_UM",
    "DEFAULT_OBJECTIVE_MAG",
]

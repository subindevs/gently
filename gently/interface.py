"""
Microscope Backend Interface

Defines the abstract protocol that any microscope hardware backend must implement
to work with the gently AI agent. This is the contract between the AI layer and
the hardware control layer.

Backends implement this protocol to provide hardware-specific functionality:
- dispim-control: DiSPIM with ASI Tiger controller
- pymmcore-plus: Generic Micro-Manager backend
- EPICS/Bluesky: Synchrotron-style control systems

Example
-------
>>> from gently.interface import MicroscopeBackend
>>> from dispim_control import DiSPIMBackend
>>>
>>> backend: MicroscopeBackend = DiSPIMBackend(config="dispim.yml")
>>> await backend.connect()
>>> uid = await backend.acquire_volume(num_slices=100)
"""

from typing import Dict, Protocol, Tuple, Optional, runtime_checkable
import numpy as np


@runtime_checkable
class MicroscopeBackend(Protocol):
    """
    Abstract interface for microscope hardware backends.

    All methods are async to support both local and remote hardware.
    Backends must implement all methods in this protocol.
    """

    # =========================================================================
    # Connection
    # =========================================================================

    async def connect(self) -> bool:
        """
        Connect to the hardware backend.

        Returns
        -------
        bool
            True if connection successful
        """
        ...

    async def disconnect(self) -> None:
        """Disconnect from the hardware backend."""
        ...

    @property
    def is_connected(self) -> bool:
        """Check if connected to hardware."""
        ...

    # =========================================================================
    # Stage
    # =========================================================================

    async def move_to_position(self, x: float, y: float) -> Dict:
        """
        Move XY stage to position.

        Parameters
        ----------
        x : float
            X position in micrometers
        y : float
            Y position in micrometers

        Returns
        -------
        dict
            Result with new position and success status
        """
        ...

    async def get_stage_position(self) -> Tuple[float, float]:
        """
        Get current XY stage position.

        Returns
        -------
        tuple of (float, float)
            (x, y) position in micrometers
        """
        ...

    async def get_piezo_position(self) -> float:
        """
        Get current piezo/focus position.

        Returns
        -------
        float
            Position in micrometers
        """
        ...

    # =========================================================================
    # Acquisition
    # =========================================================================

    async def acquire_volume(
        self,
        num_slices: int = 50,
        exposure_ms: float = 10.0,
        **kwargs,
    ) -> Dict:
        """
        Acquire a 3D volume stack.

        Parameters
        ----------
        num_slices : int
            Number of Z slices
        exposure_ms : float
            Camera exposure time in milliseconds
        **kwargs
            Backend-specific parameters (e.g., galvo_amplitude, piezo_center)

        Returns
        -------
        dict
            Must contain:
            - 'volume': np.ndarray with shape (Z, Y, X)
            - 'shape': tuple of volume dimensions
            - 'success': bool
            May contain backend-specific metadata.
        """
        ...

    async def capture_image(self, exposure_ms: Optional[float] = None) -> np.ndarray:
        """
        Capture a single 2D image.

        Parameters
        ----------
        exposure_ms : float, optional
            Exposure time in milliseconds. If None, uses current setting.

        Returns
        -------
        np.ndarray
            2D image array (Y, X), typically uint16
        """
        ...

    async def capture_lightsheet_image(
        self,
        piezo_position: float = 50.0,
        galvo_position: float = 0.0,
    ) -> Dict:
        """
        Capture a single lightsheet/SPIM image at specified positions.

        Parameters
        ----------
        piezo_position : float
            Piezo/focus position in micrometers
        galvo_position : float
            Galvo/scanner position in volts or degrees

        Returns
        -------
        dict
            Must contain:
            - 'image': np.ndarray (Y, X)
            - 'success': bool
            May contain position metadata.
        """
        ...

    # =========================================================================
    # Illumination
    # =========================================================================

    async def set_led(self, state: str) -> Dict:
        """
        Set LED illumination state.

        Parameters
        ----------
        state : str
            LED state (e.g., 'on'/'off', 'Open'/'Closed')

        Returns
        -------
        dict
            Result with success status
        """
        ...

    async def get_led_status(self) -> Dict:
        """
        Get current LED status.

        Returns
        -------
        dict
            Contains current state and available configurations
        """
        ...

    # =========================================================================
    # Camera
    # =========================================================================

    async def set_exposure(self, exposure_ms: float) -> Dict:
        """
        Set camera exposure time.

        Parameters
        ----------
        exposure_ms : float
            Exposure time in milliseconds

        Returns
        -------
        dict
            Result with success status
        """
        ...

    async def get_exposure(self) -> Dict:
        """
        Get current camera exposure time.

        Returns
        -------
        dict
            Contains current exposure_ms value
        """
        ...

    # =========================================================================
    # Calibration
    # =========================================================================

    async def calibrate(self, **kwargs) -> Dict:
        """
        Run hardware calibration.

        Parameters are backend-specific (e.g., piezo positions for diSPIM,
        z-stack range for widefield).

        Returns
        -------
        dict
            Calibration results with success status and backend-specific data
        """
        ...

    # =========================================================================
    # Acquisition Control
    # =========================================================================

    async def pause(self) -> Dict:
        """
        Pause running acquisition.

        Returns
        -------
        dict
            Result with success status
        """
        ...

    async def resume(self) -> Dict:
        """
        Resume paused acquisition.

        Returns
        -------
        dict
            Result with success status
        """
        ...

    async def abort(self) -> Dict:
        """
        Abort running acquisition.

        Returns
        -------
        dict
            Result with success status
        """
        ...

    # =========================================================================
    # Status
    # =========================================================================

    async def get_status(self) -> Dict:
        """
        Get hardware backend status.

        Returns
        -------
        dict
            Status information including device states, connection info, etc.
        """
        ...

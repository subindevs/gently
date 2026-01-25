#!/usr/bin/env python
"""
Test script for gently + dispim-control integration.

This script verifies that:
1. Both packages import correctly
2. DiSPIMBackend implements MicroscopeBackend protocol
3. MicroscopyCopilot accepts the backend

Run with: python examples/test_backend_integration.py
"""

import asyncio


def test_imports():
    """Test that all imports work."""
    print("Testing imports...")

    # Test gently
    from gently import MicroscopeBackend
    from gently.agent import MicroscopyCopilot
    print("  ✓ gently imports OK")

    # Test dispim-control
    try:
        from dispim_control import DiSPIMBackend
        print("  ✓ dispim-control imports OK")
        return True
    except ImportError as e:
        print(f"  ✗ dispim-control not installed: {e}")
        print("    Run: pip install -e /path/to/dispim-control")
        return False


def test_protocol_compliance():
    """Test that DiSPIMBackend implements MicroscopeBackend."""
    print("\nTesting protocol compliance...")

    from gently import MicroscopeBackend
    from dispim_control import DiSPIMBackend

    # Check if DiSPIMBackend is a subclass/implements the protocol
    backend = DiSPIMBackend(http_url="http://localhost:60610")

    # Check required methods exist
    required_methods = [
        'connect', 'disconnect', 'is_connected',
        'move_to_position', 'get_stage_position', 'get_piezo_position',
        'acquire_volume', 'capture_image', 'capture_lightsheet_image',
        'set_led', 'get_led_status',
        'set_exposure', 'get_exposure',
        'calibrate',
        'pause', 'resume', 'abort',
        'get_status',
    ]

    missing = []
    for method in required_methods:
        if not hasattr(backend, method):
            missing.append(method)

    if missing:
        print(f"  ✗ Missing methods: {missing}")
        return False
    else:
        print("  ✓ DiSPIMBackend implements all MicroscopeBackend methods")
        return True


def test_copilot_creation():
    """Test creating a copilot with the backend."""
    print("\nTesting copilot creation...")

    from gently.agent import MicroscopyCopilot
    from dispim_control import DiSPIMBackend

    # Create backend (won't connect without server)
    backend = DiSPIMBackend(http_url="http://localhost:60610")

    # Create copilot with backend
    copilot = MicroscopyCopilot(
        backend=backend,
        # No API key needed for this test
    )

    if copilot.backend is backend:
        print("  ✓ Copilot created with backend")
        return True
    else:
        print("  ✗ Backend not properly attached to copilot")
        return False


async def test_mock_operations():
    """Test operations with a mock backend (no hardware needed)."""
    print("\nTesting mock operations...")

    from gently import MicroscopeBackend

    class MockBackend:
        """Mock backend for testing without hardware."""

        def __init__(self):
            self._connected = False
            self._position = (0.0, 0.0)

        async def connect(self):
            self._connected = True
            return True

        async def disconnect(self):
            self._connected = False

        @property
        def is_connected(self):
            return self._connected

        async def move_to_position(self, x, y):
            self._position = (x, y)
            return {"success": True, "x": x, "y": y}

        async def get_stage_position(self):
            return self._position

        async def get_piezo_position(self):
            return 50.0

        async def acquire_volume(self, num_slices=50, exposure_ms=10.0, **kwargs):
            import numpy as np
            volume = np.zeros((num_slices, 100, 100), dtype=np.uint16)
            return {"volume": volume, "shape": volume.shape, "success": True}

        async def capture_image(self, exposure_ms=None):
            import numpy as np
            return np.zeros((100, 100), dtype=np.uint16)

        async def capture_lightsheet_image(self, piezo_position=50.0, galvo_position=0.0):
            import numpy as np
            return {"image": np.zeros((100, 100), dtype=np.uint16), "success": True}

        async def set_led(self, state):
            return {"success": True}

        async def get_led_status(self):
            return {"state": "off"}

        async def set_exposure(self, exposure_ms):
            return {"success": True}

        async def get_exposure(self):
            return {"exposure_ms": 10.0}

        async def calibrate(self, **kwargs):
            return {"success": True, "calibration": {}}

        async def pause(self):
            return {"success": True}

        async def resume(self):
            return {"success": True}

        async def abort(self):
            return {"success": True}

        async def get_status(self):
            return {"connected": self._connected}

    # Test with mock backend
    backend = MockBackend()

    await backend.connect()
    assert backend.is_connected, "Connect failed"
    print("  ✓ connect()")

    await backend.move_to_position(100.0, 200.0)
    pos = await backend.get_stage_position()
    assert pos == (100.0, 200.0), f"Position mismatch: {pos}"
    print("  ✓ move_to_position() / get_stage_position()")

    result = await backend.acquire_volume(num_slices=10)
    assert result["success"], "Acquire failed"
    assert result["shape"] == (10, 100, 100), f"Shape mismatch: {result['shape']}"
    print("  ✓ acquire_volume()")

    image = await backend.capture_image()
    assert image.shape == (100, 100), f"Image shape mismatch: {image.shape}"
    print("  ✓ capture_image()")

    await backend.disconnect()
    assert not backend.is_connected, "Disconnect failed"
    print("  ✓ disconnect()")

    return True


def main():
    print("=" * 50)
    print("Gently + DiSPIM-Control Integration Test")
    print("=" * 50)

    results = []

    # Test imports
    if not test_imports():
        print("\n⚠ Install dispim-control first to run full tests")
        return

    results.append(("Protocol compliance", test_protocol_compliance()))
    results.append(("Copilot creation", test_copilot_creation()))
    results.append(("Mock operations", asyncio.run(test_mock_operations())))

    # Summary
    print("\n" + "=" * 50)
    print("Results:")
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: {name}")

    all_passed = all(r[1] for r in results)
    print("=" * 50)
    print("All tests passed!" if all_passed else "Some tests failed.")


if __name__ == "__main__":
    main()

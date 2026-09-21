import unittest
from session_manager import SessionManager


class LifecycleTests(unittest.IsolatedAsyncioTestCase):
    async def test_cleanup_can_stop_and_restart(self):
        manager = SessionManager()
        await manager.start()
        task = manager._cleanup_handle
        await manager.start()
        self.assertIs(manager._cleanup_handle, task)
        await manager.stop()
        self.assertTrue(task.cancelled())
        await manager.start()
        self.assertIsNot(manager._cleanup_handle, task)
        await manager.stop()
        await manager.stop()

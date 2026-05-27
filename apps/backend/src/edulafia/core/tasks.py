"""Global background tasks registry to prevent garbage collection."""
import asyncio

# A set to hold strong references to running background tasks
background_tasks = set()

def create_tracked_task(coro):
    """Create an asyncio task and store a strong reference to it."""
    task = asyncio.create_task(coro)
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)
    return task

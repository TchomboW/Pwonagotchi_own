import asyncio
import logging
from typing import Callable, Dict, List, Any


class EventBus:
    """
    A high-performance, asynchronous event bus for decoupling 
    system components and facilitating reactivity.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._subscribers: Dict[str, List[Callable[[Any], Any]]] = {}

    def subscribe(self, event_type: str, callback: Callable[[Any], Any]):
        """Registers a subscriber for a specific event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)
        self.logger.debug(f"Subscribed to event type: {event_type}")

    async def publish(self, event_type: str, data: Any = None):
        """Publishes an event to all registered subscribers."""
        self.logger.info(f"Publishing Event: [{event_type}] with data: {data}")
        if event_type in self._subscribers:
            tasks = []
            for callback in self._subscribers[event_type]:
                # Check if it's a coroutine or regular function
                if asyncio.iscoroutinefunction(callback):
                    tasks.append(callback(data))
                else:
                    # Run sync functions in executor to not block the loop
                    loop = asyncio.get_event_loop()
                    tasks.append(loop.run_in_executor(None, callback, data))
            
            if tasks:
                await asyncio.gather(*tasks)

    def get_subscribers(self, event_type: str) -> List[Callable]:
        """Returns the list of callbacks for a specific event type."""
        return self._subscribers.get(event_type, [])

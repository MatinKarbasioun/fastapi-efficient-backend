import ray
from uuid import uuid4

from application.actors.image_processor import ImageProcessorActor



@ray.remote
class ManagerActor:
    def __init__(self):
        self._actors = {}
        
    def create_actor(self, actor_name):
        if actor_name not in self._actors:
            actor_name = uuid4().hex
            self._actors.update({actor_name: ImageProcessorActor.option(
                name=actor_name,
                get_if_exists=True
            ).remote()})
        return self._actors[actor_name]
    
    async def add_task(self)
        

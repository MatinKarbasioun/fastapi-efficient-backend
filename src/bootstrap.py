from application.actors.actor_sys import ActorSystem
from settings import get_settings
from pathlib import Path
import ray

from application.actors.image_processor import ImageProcessorActor


class Bootstrap:
    def __init__(self):
        self._settings = get_settings()
    
    def init(self):
        """ bootstrap function to init system before run""" 
        ray.init()
        ActorSystem()
        ActorSystem.Manager.create_actor.remote()
        upload_path = Path("local_uploads") / Path(self._settings.UPLOAD_DIR)
        self._initialize_path(upload_path)

    def _initialize_path(self, path: str):
        try:
            path.mkdir(parents=True, exist_ok=True)
        except FileExistsError:
            pass
        
    

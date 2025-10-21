from application.actors.actor_sys import ActorSystem
from settings import get_settings
import ray

from application.actors.image_processor import ImageProcessorActor


def bootstrap():
    """ bootstrap function to init system before run"""
    get_settings()
    ray.init()
    ActorSystem()
    ActorSystem.Manager.create_actor.remote()

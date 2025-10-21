from application.actors.manager import ManagerActor


class ActorSystem:
    Manager = None
    
    def __init__(self):
        ActorSystem.Manager = ManagerActor.options(name="manager").remote()
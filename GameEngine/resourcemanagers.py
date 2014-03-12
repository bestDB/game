from gamehelpers import ResourceHelper
import pygame

class ResourceManager :

    instance = None

    def __init__(self):
        self.rPid = 0
        self.resourcesPaths = []
        self.loadedResources = []
        ResourceManager.instance = self

    @staticmethod
    def allocate_resource(path):
        ResourceManager.instance.resourcesPaths.insert(ResourceManager.instance.rPid, path)
        ResourceManager.instance.rPid += 1
        return ResourceManager.instance.rPid - 1

    @staticmethod
    def get_resource_id(loadedResource):
        if loadedResource in ResourceManager.instance.loadedResources :
            return ResourceManager.instance.loadedResources.index(loadedResource)

    @staticmethod
    def prepare_resources(resourcesIds):
        for id_ in resourcesIds :
            loaded = ResourceHelper.load_resource(ResourceManager.instance.resourcesPaths[id_])
            if loaded != None :
                ResourceManager.instance.loadedResources.insert(id_, loaded)

    @staticmethod
    def prepare_all_resources():
        for index in range(0, ResourceManager.instance.resourcesPaths.__len__()):
            path = ResourceManager.instance.resourcesPaths[index]
            loaded = ResourceHelper.load_resource(path)
            if loaded != None :
                ResourceManager.instance.loadedResources.insert(index, loaded)

    @staticmethod
    def clear():
        ResourceManager.instance.loadedResources = []

import os

from direct.showbase import Loader
from panda3d.core import Filename


class AssetFactory:
    loader = None
    assetRoot = ''

    @staticmethod
    def setLoader(loader: Loader):
        AssetFactory.loader = loader

    @staticmethod
    def setAssetRoot(path: str):
        if not os.path.exists(path):
            raise ValueError(f"Asset path does not exist: '{path}'")
        AssetFactory.assetRoot = path

    @staticmethod
    def loadModel(filename):
        path = Filename.fromOsSpecific(os.path.join(AssetFactory.assetRoot, filename))
        try:
            return AssetFactory.loader.loadModel(path)
        except Exception as e:
            print(e)

    @staticmethod
    def loadTexture(filename):
        path = Filename.fromOsSpecific(os.path.join(AssetFactory.assetRoot, filename))
        return AssetFactory.loader.loadTexture(path)

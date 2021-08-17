import os

from direct.showbase import Loader
from panda3d.core import Filename, Texture


# Static accessor for loading panda assets
class AssetFactory:
    loader = None
    assetRoot = ''

    # Panda app sets the loader on startup
    @staticmethod
    def setLoader(loader: Loader):
        AssetFactory.loader = loader

    # Panda app sets the base directory where assets are stored on startup
    @staticmethod
    def setAssetRoot(path: str):
        # Confirm the path exists on the system
        if not os.path.exists(path):
            raise ValueError(f"Asset path does not exist: '{path}'")
        AssetFactory.assetRoot = path

    # Load a model for panda, returning a new nodepath
    @staticmethod
    def loadModel(filename):
        # Build the absolute path
        path = Filename.fromOsSpecific(os.path.join(AssetFactory.assetRoot, filename))
        try:
            return AssetFactory.loader.loadModel(path)
        except Exception as e:      # Catches if the path doesn't exist
            print(e)

    # Load the texture from disk
    @staticmethod
    def loadTexture(filename):
        # Get the absolute path
        path = Filename.fromOsSpecific(os.path.join(AssetFactory.assetRoot, filename))
        # Panda's texture loader normally caches textures, so subsequent loads just return the same object
        # We need to be able to set different visual properties on different models using the same base texture
        # Because of that, we have to force load the texture from disk every time
        newTex = Texture()
        newTex.setup2dTexture()
        newTex.read(path)
        # Return the texture
        return newTex

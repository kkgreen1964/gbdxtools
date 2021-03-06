from gbdxtools.images.base import RDABaseImage
from gbdxtools.images.drivers import RDADaskImageDriver
from gbdxtools.images.util import reproject_params
from gbdxtools.ipe.interface import Ipe
ipe = Ipe()

class Sentinel2Driver(RDADaskImageDriver):
    image_option_support = ["spec", "product", "proj"]
    __image_option_defaults__ = {"spec": "10m", "product": "sentinel", "proj": None}

class Sentinel2(RDABaseImage):
    """
      Dask based access to sentinel2 images backed by IPE Graphs.
    """
    __Driver__ = Sentinel2Driver

    @property
    def _id(self):
        return self.__rda_id__

    @property
    def _spec(self):
        return self.options["spec"]

    @property
    def _rgb_bands(self):
        return [2,1,0]

    @property
    def _ndvi_bands(self):
        return [6,3]

    @classmethod
    def _build_standard_products(cls, prefix, spec="10m", proj=None, **kwargs):
        sentinel = ipe.SentinelRead(SentinelId=prefix, sentinelProductSpec=spec)
        if proj is not None:
            sentinel = ipe.Reproject(sentinel, **reproject_params(proj))
        return {
            "sentinel": sentinel
        }

from gbdxtools.images.base import RDABaseImage
from gbdxtools.images.drivers import RDADaskImageDriver
from gbdxtools.images.util.image import reproject_params
from gbdxtools.ipe.interface import Ipe
ipe = Ipe()

class LandsatDriver(RDADaskImageDriver):
    __default_options__ = {}
    image_option_support = ["spec", "product", "proj"]
    __image_option_defaults__ = {"spec": "multispectral", "product": "landsat", "proj": None}

class LandsatImage(RDABaseImage):
    """
      Dask based access to landsat image backed by IPE Graphs.
    """
    __Driver__ = LandsatDriver

    @property
    def _id(self):
        return self.__rda_id__

    @property
    def _spec(self):
        return self.options["spec"]

    @property
    def _rgb_bands(self):
        return [3,2,1]

    @property
    def _ndvi_bands(self):
        return [4,3]

    @classmethod
    def _build_standard_products(cls, _id, spec="multispectral", proj=None, **kwargs):
        landsat = ipe.LandsatRead(landsatId=_id, productSpec=spec)
        if proj is not None:
            landsat = ipe.Reproject(landsat, **reproject_params(proj))
        return {
            "landsat": landsat
        }

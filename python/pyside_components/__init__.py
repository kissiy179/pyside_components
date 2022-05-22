try:
    from importlib import reload

except:
    pass

from . import layouts; reload(layouts)
from . import models; reload(models)
from . import views; reload(views)
from . import widgets; reload(widgets)
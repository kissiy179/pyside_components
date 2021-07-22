try:
    from importlib import reload

except:
    pass

from . import double_clickable_button; reload(double_clickable_button)
from . import text_editable_button; reload(text_editable_button)
from . import double_actions_button; reload(double_actions_button)
from . import removable_button; reload(removable_button)
from . import tag_item_button; reload(tag_item_button)
from . import tag_edit; reload(tag_edit)
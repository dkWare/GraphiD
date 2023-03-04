from .utils import Vector2D as _Vector2D
from .utils import MousePointer as _MousePointer
from .debugger import logger as dbg
from .debugger import Tag as _debugger_tags

try:
    from .fields import UIField as _UIField
except ImportError:
    dbg.critical("importing _UIField skipped", extra={'classname': "", "tags": [_debugger_tags.M_MANAGE]})
import arcade

class UIManager:
    def __init__(self, mouse_pointer: _MousePointer, *fields):
        """
        This class is a shortcut to not have to use these methods on every single element.
        And for example to shorten 80 lines in 4 for 20 elements.

        ## register
        use the register method to regress single elements. You can also pass an instance of
        this manager either directly when creating the element from a predefined class or also
        pass an instance at super.__init__ for your own classes that inherit from one of the predefined
        classes. if you do one of the two above you don't have to use this method on the named object
        or on all created objects of this class.

        ## draw
        this method calls the function with the same name for all regressed elements

        ## update
        with this method the function with the same name is called for all regressed elements

        ## raise_click_event_press
        with this method the function with the same name is called for all regressed elements

        ## raise_click_event_release
        this method calls the function with the same name for all regressed elements

        ## getitem
        You can access individual elements by accessing them with their ID:
        gui_manager_object[element_id]
        """
        self.field_list:list[_UIField] = []
        self.field_dict = {}
        for field in fields:
            self.field_list.append(field)
            self.field_dict[field.ID] = field
        self._mouse_pointer = mouse_pointer

    def register(self, field):
        """
        use the register method to regress single elements. You can also pass an instance of
        this manager either directly when creating the element from a predefined class or also
        pass an instance at super.__init__ for your own classes that inherit from one of the predefined
        classes. if you do one of the two above you don't have to use this method on the named object
        or on all created objects of this class.
        """
        if type(field) is not UIGroup:
            field.register_mouse(self._mouse_pointer)
        self.field_list.append(field)
        self.field_dict[field.ID] = field
        dbg.debug(f"REGISTERED field: <\"{field.ID}\">", extra={'classname': self.__class__.__name__})

    def draw(self):
        """
        Draw all the elements
        For more details please refer to the same method in the respective element
        """
        for field in self.field_list:
            field.draw()

    def update(self):
        """
        Update all elements
        For more details please refer to the same method in the respective element
        """
        for field in self.field_list:
            if type(field) is UIGroup:
                field.update()
                continue
            field.update_field()

    def raise_click_event_press(self, button: int):
        """
        Trigger a mouse press event at each element
        For more details please refer to the same method in the respective element

        button: int the pressed button
        """
        dbg.info("MOUSE PRESS EVENT start iterating all fields", extra={"tags": [_debugger_tags.EVENTS, _debugger_tags.M_MANAGE, _debugger_tags.MOUSE], 'classname': self.__class__.__name__})
        for field in self.field_list:
            field.raise_click_event_press(button)

    def raise_click_event_release(self, button: int):
        """
        Trigger a mouse release event on each element
        For more details please refer to the same method in the respective element

        button: int the released button
        """
        dbg.info("MOUSE RELEASE EVENT start iterating all fields", extra={"tags": [_debugger_tags.EVENTS, _debugger_tags.M_MANAGE, _debugger_tags.MOUSE], 'classname': self.__class__.__name__})
        for field in self.field_list:
            field.raise_click_event_release(button)

    def __getitem__(self, name):
        dbg.warning(f"USED GETITEM TO GET \"{name}\". THIS WILL BE REMOVED", extra={"tags": [_debugger_tags.M_MANAGE], 'classname': self.__class__.__name__})
        if name in self.field_dict:
            return self.field_dict[name]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")


class UIGroup(UIManager):
    def __init__(self, group_id:str, mouse_pointer: _MousePointer, *fields):
        super().__init__(mouse_pointer, *fields)
        self.__group_id = group_id

    @property
    def ID(self):
        return self.__group_id

    def deactivate(self):
        for field in self.field_list:
            field.deactivate()

    def activate(self):
        for field in self.field_list:
            field.activate()

    def set_visible(self, x: bool):
        for field in self.field_list:
            field.set_visible(x)

    def set_active(self, x: bool):
        for field in self.field_list:
            field.set_active(x)

    def set_locked(self, x: bool):
        for field in self.field_list:
            field.set_locked(x)

    def set_color_unmasked(self, c: arcade.Color):
        for field in self.field_list:
            field.set_color_unmasked(c)

    def set_color_masked(self, c: arcade.Color):
        for field in self.field_list:
            field.set_color_masked(c)

    def set_color_pressed(self, c: arcade.Color):
        for field in self.field_list:
            field.set_color_pressed(c)

    def set_color_locked(self, c: arcade.Color):
        for field in self.field_list:
            field.set_color_locked(c)

    def change_position(self, x: float, y:float):
        for field in self.field_list:
            field.change_position(x, y)

    def change_position_rel(self, dx: float, dy:float):
        for field in self.field_list:
            field.change_position_rel(dx, dy)


class EventTemplate:
    def on_draw(self):
        arcade.start_render()
        self.gui_manager.draw()

    def on_update(self, delta_time):
        self.gui_manager.update()

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_pointer.change(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        self.gui_manager.raise_click_event_press(button)

    def on_mouse_release(self, x, y, button, modifiers):
        self.gui_manager.raise_click_event_release(button)

    def on_mouse_leave(self, x: int, y: int):
        dbg.warning(f"MOUSE LEFT ON POSITION {_Vector2D(x, y, 'left')}", extra={"tags": [_debugger_tags.EVENTS, _debugger_tags.M_MANAGE, _debugger_tags.MOUSE], "classname": self.__class__.__name__})
        self.mouse_pointer.change(-100, -100)

    def on_mouse_enter(self, x: int, y: int):
        dbg.warning(f"MOUSE ENTERED ON POSITION {_Vector2D(x, y, 'entered')}", extra={"tags": [_debugger_tags.EVENTS, _debugger_tags.M_MANAGE, _debugger_tags.MOUSE], "classname": self.__class__.__name__})
        self.mouse_pointer.change(x, y)

dbg.debug("MANAGE MODULE LOADED", extra={"classname": ""})

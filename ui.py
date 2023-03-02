from math import isclose, sqrt
from typing import overload
from numpy import clip
import arcade
import debuger

dbg = debuger.log


class Vector2D:
    def __init__(self, a: float, b: float):
        """
        This Class represents a simple two dimensional Vector
        It has two values:

        - a: float | int
        - b: float | int

        ## properties
        you can get the values separate by using:
        - @valA for the content of a
        - @valB for the content of b
        or both in a tuple by using:
        - @values
        """
        self._a = a
        self._b = b

    def __add__(self, other: tuple):
        self._a += other[0]
        self._b += other[1]
        return self

    @property
    def valA(self):
        return self._a

    @property
    def valB(self):
        return self._b

    @property
    def values(self):
        return self._a, self._b


class MousePointer(Vector2D):
    """
    This Class represents the position off the Mouse
    It has two values:

     - a: float | int
     - b: float | int

    ## properties
    you can get the values separate by using:
     - @valA for the content of a
     - @valB for the content of b
    or both in a tuple by using:
     - @values
    ## methods
    you can use the change method to change a and b:
     - @change(new_a: float|int, new_b: float|int)
    """
    def __init__(self, a: float, b: float):
        super().__init__(a, b)

    def change(self, a, b):
        self._a = a
        self._b = b


class UIManager:
    def __init__(self, mouse_pointer: MousePointer, *fields):
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
        self.field_list = []
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
        field.register_mouse(self._mouse_pointer)
        self.field_list.append(field)
        self.field_dict[field.ID] = field
        dbg.debug(f"REGISTERED field: <\"{field.ID}\">")

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
            field.update_field()

    def raise_click_event_press(self, button: int):
        """
        Trigger a mouse press event at each element
        For more details please refer to the same method in the respective element

        button: int the pressed button
        """
        dbg.info("MOUSE PRESS EVENT start iterating all fields")
        for field in self.field_list:
            field.raise_click_event_press(button)

    def raise_click_event_release(self, button: int):
        """
        Trigger a mouse release event on each element
        For more details please refer to the same method in the respective element

        button: int the released button
        """
        dbg.info("MOUSE RELEASE EVENT start iterating all fields")
        for field in self.field_list:
            field.raise_click_event_release(button)

    def __getitem__(self, name):
        dbg.warning(f"USED GETITEM TO GET \"{name}\". THIS WILL BE REMOVED")
        if name in self.field_dict:
            return self.field_dict[name]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

class UIField:
    def _find_center(self, pointA: Vector2D, pointC: Vector2D):
        """
        Calculates the following values:
         - width (float) the width of this field
         - height (float) the height of this field
         - size (Vector2D) it contains the width and height

         - center_x (float) the center position on x
         - center_y (float) the center position on y
         - centerPos (Vector2D) it contains the center position

        Args:
            pointA (Vector2D): The point from the fields upper left
            pointC (Vector2D): The point from the fields lower right
        """
        self._width = pointA.valA - pointC.valA
        self._height = pointA.valB - pointC.valB
        self._half_width = self._width / 2
        self._half_height = self._height / 2
        self._size = Vector2D(self._width, self._height)

        self._center_x = pointA.valA + self._half_width
        self._center_y = pointA.valB - self._half_height
        self._centerPos = Vector2D(self._center_x, self._center_y)
        dbg.info(f"FOUND CENTER: x: {self._center_x} y: {self._center_y}")

    def _create_point_list(self, pointA: Vector2D, pointB: Vector2D, pointC: Vector2D, pointD: Vector2D):
        """
        method to create the required point_list and point_list_raw

        Args:
            pointA (Vector2D): The point from the fields upper left
            pointB (Vector2D): The point from the fields upper right
            pointC (Vector2D): The point from the fields lower right
            pointD (Vector2D): The point from the fields lower left

        Returns:
            None
        """
        point_list = [pointA, pointB, pointC, pointD]
        if None in point_list:
            return
        self._point_list_raw = [point.values for point in point_list]
        self._point_list = point_list
        dbg.info("successfully built point list")
        self._find_center(pointA, pointC)

    def _init_values(self, id: str):
        """
        In this method all flags and the required data for the button
        are set to default for later use. They can always be changed after creation

        Args:
            id (str): The ID of this field for debug uses

        Returns:
            None
        """
        #for debug uses
        self._id = id
        self.debug = True

        #Mouse Event flags
        self._mouse_press_on_field = False
        self._mouse_pointer_in_field = False
        self.release_event_outside_field = True
        self._mouse_click_logic_overwrite = False

        #Visual Flags and colors
        self._mouse_click_visual_overwrite = False
        self._color_masked = arcade.color.DARK_GREEN
        self._color_unmasked = arcade.color.RED
        self._color_pressed = arcade.color.GREEN
        self._color_field_locked = arcade.color.DARK_RED

        #Control flags Events, Logic and Visual
        self._field_active = True
        self._field_visible = True
        self._field_locked = False
        self._listen_for_mouse_enter_event = True
        self._listen_for_mouse_leave_event = True

        #Create Mouse Pointer Var for IDE
        #Check if its not already exists
        #so that it wont overwrite in future cases
        if not hasattr(self, "_mouse_pointer"):
            dbg.warning("MOUSE POINTER MAY BE OVERWRITTEN")
            self._mouse_pointer = None

    def register_mouse(self, mouse: MousePointer):
        """
        Register a mouse for all events that need mouse position.
        for example entering or leaving the field with it.

        Args:
            mouse (MousePointer): An instance off the MousePointer class
        """
        self._mouse_pointer = mouse

    def _try_register(self, ui_manager: UIManager):
        if ui_manager:
            ui_manager.register(self)

    def __init__(self, id: str=None, *, pointA: Vector2D=None, pointB: Vector2D=None, pointC: Vector2D=None, pointD: Vector2D=None, ui_manager: UIManager=None, other_form:bool=False):
        """
        Create the default UIField. Its shape is a Rectangle, to create it you need to give four points and ab id for debugging.
        If you want that the Field registers automatically you can also give an instance from the class UIManager.

        Args:
            id (str): The ID of this field for debug uses
            pointA (Vector2D): The point from the fields upper left
            pointB (Vector2D): The point from the fields upper right
            pointC (Vector2D): The point from the fields lower right
            pointD (Vector2D): The point from the fields lower left
            ui_manager (UIManager, optional): If you want to register it automatically. Defaults to None.
            other_form (bool, optional): This is used internal. Defaults to False.
        """
        if other_form: #used the alternative constructor
            return

        self._init_values(id)
        self._create_point_list(pointA, pointB, pointC, pointD)
        self._try_register(ui_manager)

    def __init_other__(self, id: str, *, ui_manager: UIManager=None):
        """
        Use this if you want to create a UIField thats
        shaped differently then a Rectangle.
        Here you only need the id. You can also give an instance of
        the UIManager class to register it.

        Args:
            id (str): The ID of this field for debug uses
            ui_manager (UIManager, optional): If you want to register it automatically. Defaults to None.
        """
        self._init_values(id)
        self._try_register(ui_manager)

    def _position_over_field(self, position: Vector2D, *, pointA: Vector2D, pointC: Vector2D):
        """
        This method detects if the given position is in the given area/field

        Args:
            position (Vector2D): The given position given as Vector2D or MousePointer
            pointA (Vector2D): _description_
            pointC (Vector2D): _description_

        Returns:
            bool True if the mouse is in the field
        """
        if not pointA.valA <= position.valA <= pointC.valA:
            return False

        if not pointC.valB <= position.valB <= pointA.valB:
            return False

        return True

    def _get_flag_change(self, oldFlagState: bool, newFlagState: bool):
        """
        Shows the change from an old state to the new state of an given Flag

        Args:
            oldFlagState (bool): The old value off the Flag
            newFlagState (bool): The new value off the Flag

        Returns:
            tuple[bool, bool]
            False, False: Nothing has changed
            False, True: The value has gone from False to True
            True, False: The value has gone from True to False
        """
        if oldFlagState == 0 and newFlagState == 1:
            return False, True
        if oldFlagState == 1 and newFlagState == 0:
            return True, False
        return False, False

    def change_position(self, x: float, y: float):
        point = self._point_list[0]
        dx = point.valA - x
        dy = point.valB - y
        self.change_position_rel(dx, dy)

    def change_position_rel(self, dx: float=0, dy: float=0):
        self._point_list_raw.clear()
        for point in self._point_list:
            point: Vector2D
            point += dx, dy
            self._point_list_raw.append(point.values)
        self._find_center(self._point_list[0], self._point_list[2])
        self.on_position_change(Vector2D(dx, dy))
        dbg.info(f"CHANGED POS BY dx: {dx} dy: {dy} to x: {self._center_x} y: {self._center_y}")

    def update_field(self):
        """
        Update the UIField, check if active and not locked.
        If both is correct call the on_update method then checks if
        the mouse has entered or left the field.
        if it has entered call the on_mouse_enters and if the mouse has left call
        the on_mouse_leaves method
        """
        if not self._field_active: #field is not active
            return

        if self._field_locked: #field is locked
            return


        #check if mouse is in field and use it to get the action if muse has entered left to call the representing event
        new_mouse_pointer_in_field = self._position_over_field(self._mouse_pointer, pointA=self._point_list[0], pointC=self._point_list[2])
        mouse_leaves_field, mouse_enters_field = self._get_flag_change(self._mouse_pointer_in_field, new_mouse_pointer_in_field)

        if mouse_enters_field and self._listen_for_mouse_enter_event: #mouse has entered the field
            dbg.info(f"[{self._id} mouse has entered the field]")
            self.on_mouse_enters()

        if mouse_leaves_field and self._listen_for_mouse_leave_event: #mouse has left the field
            dbg.info(f"[{self._id} mouse has left the field]")
            self.on_mouse_leaves()

        #if none of the if statements above then the mouse is outside or is still in the field

        #call the update event
        self.on_update()

        #save the current mouse flag to detect changes in an later try
        self._mouse_pointer_in_field = new_mouse_pointer_in_field

    def draw(self):
        """
        Draws the Field only if the field is visible.
        The field can have 3 states:
        (event, default color)
         - mouse in field: arcade.color.DARK_GREEN
         - mouse not in field: arcade.color.RED
         - mouse pressed field: arcade.color.GREEN
         - field locked: arcade.color.DARK_RED

        for every state you can change the color:
         - set_color_masked
         - set_color_unmasked
         - set_color_pressed
         - set_color_locked
        """
        if not self._field_visible: #the field is not visible
            return

        if self._field_locked: #field is locked
            color = self._color_field_locked
        elif self._mouse_press_on_field: #field is being pressed
            color = self._color_pressed
        else: #mark field so that its unmarked or marked
            color = self._color_unmasked if not self._mouse_pointer_in_field and not self._mouse_click_visual_overwrite else self._color_masked
        arcade.draw_polygon_filled(self._point_list_raw, color)

        if not self.debug:
            return

        for index, point in enumerate(self._point_list):
            arcade.draw_text(index, *point.values)

    def raise_click_event_press(self, button: int):
        """
        Call this method to raise an click event.
        It checks if the mouse is in the field and
        raises an button_press event.

        Args:
            button (int): The button that is being used to press the Mouse
        """
        if not self._field_active: #field is not active
            return

        if self._field_locked: #field is locked
            return

        if self._mouse_pointer_in_field: #mouse is in field
            dbg.info(f"[{self._id} mouse has press on field]")
            #set to true to detect later the release event even if mouse leaves the field
            self._mouse_press_on_field = True
            self.on_button_press(button)

    def raise_click_event_release(self, button: int):
        """
        Call this method to raise an click event.
        It checks if the mouse is in the field and
        raises an button_release event.

        Args:
            button (int): The button that is being used to press the Mouse
        """
        if not self._field_active: #field is not active
            return

        if self._field_locked: #field is locked
            return

        #if this is true the event can be raised even outside the field
        #it is False so that the user can set it so it can or it can not
        #be raised outside the field
        release_event_overwrite = False

        if self.release_event_outside_field and self._mouse_press_on_field:
            #button was pressed, the mouse button got released and the user lets
            #raise the event outside the field
            release_event_overwrite = True

        if self._mouse_pointer_in_field or release_event_overwrite:
            #the mouse button gets released in or outside the field
            #with self._mouse_pointer_in_field we check if the mouse is in the field
            #bzw if release_event_overwrite is True we realest the button outside the field
            dbg.info(f"[{self._id} mouse has released the field]")
            self.on_button_release(button)
            self._mouse_press_on_field = False

    def on_mouse_enters(self):
        """
        This event gets called when the mouse enters this field
        """

    def on_mouse_leaves(self):
        """
        This event gets called when the mouse leaves this field
        """

    def on_button_press(self, button: int):
        """
        This event gets called when the mouse button is over this field.
        And pressed on the field, you get witch button is being pressed
        in form of an int:
         - arcade.MOUSE_BUTTON_LEFT: 1
         - arcade.MOUSE_BUTTON_MIDDLE: 2
         - arcade.MOUSE_BUTTON_RIGHT: 4

        Args:
            button (int): the button that was used by the user
        """

    def on_button_release(self, button: int):
        """
        This event gets called when the mouse button is over this field.
        And the button gets released on the field or nearby, you get witch
        button is being pressed in form of an int:
         - arcade.MOUSE_BUTTON_LEFT: 1
         - arcade.MOUSE_BUTTON_MIDDLE: 2
         - arcade.MOUSE_BUTTON_RIGHT: 4

        Args:
            button (int): the button that was used by the user
        """

    def on_unlock(self):
        """
        This event gets called when this field gets unlocked
        """

    def on_lock(self):
        """
        This event gets called when this field gets locked
        """

    def on_activate(self):
        """
        This event gets called when this field gets activated
        """

    def on_deactivate(self):
        """
        This event gets called when this field gets deactivated
        """

    def on_hide(self):
        """
        This event gets called when this field gets hidden
        """

    def on_visible(self):
        """
        This event gets called when this field gets shown
        """

    def on_update(self):
        """
        This event gets called after this field gets updated
        """

    def on_position_change(self, delta_position: Vector2D):
        """
        This event gets called after the position of this field changes

        Args:
            delta_position (Vector2D): The change in Position Vector2D(dx, dy)
        """

    def activate(self):
        """
        a short cut to set the field visible and active. it also raises both events:
         - on_activate
         - on_visible
        """
        self._field_visible = True
        self._field_active = True
        self.on_activate()
        self.on_visible()
        dbg.warning(f"[{self._id}] got activated")

    def deactivate(self):
        """
        a short cut to set the field visible and active. it also raises both events:
         - on_deactivate
         - on_hide
        """
        self._field_visible = False
        self._field_active = False
        self.on_deactivate()
        self.on_hide()
        dbg.warning(f"[{self._id}] got deactivated")

    def set_visible(self, x: bool):
        """
        This method sets the visibility of this field:
        it also calls on_hide or on_visible when you set it invisible
        or visible
        """
        show, hide = self._get_flag_change(self._field_visible, x)
        if hide:
            dbg.warning.info(f"[{self._id}] invisible")
            self.on_hide()
        else:
            dbg.warning.info(f"[{self._id}] visible")
            self.on_visible()
        self._field_visible = x

    def set_active(self, x: bool):
        """
        This method sets the active or deactivate.
        it also calls:
         - on_activate
         - on_deactivate
        """
        deactivate, activate = self._get_flag_change(self._field_active, x)
        if activate:
            dbg.warning.info(f"[{self._id}] activate")
            self.on_activate()
        else:
            dbg.warning(f"[{self._id}] deactivate")
            self.on_deactivate()
        self._field_active = x

    def set_locked(self, x: bool):
        unlock, lock = self._get_flag_change(self._field_locked, x)
        if lock:
            dbg.warning(f"[{self._id}] locked")
            self.on_lock()
        else:
            dbg.warning(f"[{self._id}] unlocked")
            self.on_unlock()
        self._field_locked = x
        if x:
            self._mouse_pointer_in_field = False
            self._mouse_press_on_field = False

    def set_color_unmasked(self, color: arcade.color):
        self._color_unmasked = color

    def set_color_masked(self, color: arcade.color):
        self._color_masked = color

    def set_color_pressed(self, color: arcade.color):
        self._color_pressed = color

    def set_color_locked(self, color: arcade.color):
        self._color_field_locked = color

    def overwrite_visual_mouse_click(self, x: bool):
        self._mouse_click_visual_overwrite = x

    def listen_for_mouse_enter(self, x: bool):
        self._listen_for_mouse_enter_event = x

    def listen_for_mouse_leaving(self, x: bool):
        self._listen_for_mouse_leave_event = x

    def raise_mouse_move_events(self, x: bool):
        self._listen_for_mouse_enter_event = x
        self._listen_for_mouse_leave_event = x

    @property
    def IS_ACTIVE(self):
        return self._field_active and self._field_visible

    @property
    def IS_VISIBLE(self):
        return self._field_visible

    @property
    def IS_LOCKED(self):
        return self._field_locked

    @property
    def ID(self):
        return self._id

    @property
    def MOUSE(self):
        return self._mouse_pointer

    def __str__(self) -> str:
        if not self.debug:
            return ""
        points = ""
        for point in self._point_list_raw:
            points += " " + str(point)
        return f"{self._id}: {self._point_list_raw[1][0] - self._point_list_raw[0][0]} : {self._point_list_raw[3][1] - self._point_list_raw[0][1]}\n{points}"


class RectButton(UIField):
    def set_field(self, *, width: float=None, height: float=None, center_x: float=None, center_y: float=None, text_dx: float=None, text_dy: float=None):
        old_x = self._centerPos.valA
        old_y = self._centerPos.valB

        if width is None:
            width = self._width
        if height is None:
            height = self._height
        if center_x is None:
            center_x = self._center_x
        if center_y is None:
            center_y = self._center_y
        if text_dx is None:
            text_dx = self._text_dx
        if text_dy is None:
            text_dy = self._text_dy

        self._half_width = width/2
        self._half_height = height/2

        point_a = Vector2D(center_x-self._half_width, center_y)
        point_b = Vector2D(center_x+self._half_width, center_y)
        point_c = Vector2D(center_x+self._half_width, center_y-self._half_height)
        point_d = Vector2D(center_x-self._half_width, center_y-self._half_height)
        self._create_point_list(point_a, point_b, point_c, point_d)

        self._text_x = center_x-self._half_width+text_dx
        self._text_y = center_y-self._half_height+text_dy

        self._centerPos = Vector2D(center_x, center_y)

        dx = old_x - center_x
        dy = old_y - center_y

        if dx != 0 or dy != 0:
            self.on_position_change(self._centerPos)

    def _set_text_pos(self):
        self._text_x = self._center_x-self._half_width+self._text_dx
        self._text_y = self._center_y-self._half_height+self._text_dy

    def __init__(self, id: str, *, center_x: float, center_y: float, width: float, height: float, text: str, text_size: int, text_dx: float, text_dy: float, ui_manager: UIManager=None, release_event_outside_field:bool=False):
        half_width = width / 2
        half_height = height / 2

        point_a = Vector2D(center_x-half_width, center_y)
        point_b = Vector2D(center_x+half_width, center_y)
        point_c = Vector2D(center_x+half_width, center_y-half_height)
        point_d = Vector2D(center_x-half_width, center_y-half_height)
        super().__init__(id, pointA=point_a, pointB=point_b, pointC=point_c, pointD=point_d)

        self.text = text
        self._text_size = text_size

        self._text_dx = text_dx
        self._text_dy = text_dy
        self._set_text_pos()

        if ui_manager:
            ui_manager.register(self)

    def change_position(self, dx: float=0, dy: float=0):
        super().change_position_rel(dx, dy)
        self._set_text_pos()

    def draw(self):
        if not self._field_visible:
            return

        super().draw()
        arcade.draw_text(self.text, self._text_x, self._text_y, font_size=self._text_size)

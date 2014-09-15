"""
**dungeon** module

Provides an engine for simple text adventure games.
"""

import locale
import types
import re
import gettext

import dsent.lists

from src import settings


__author__ = 'dsent'
__version__ = '2.0'
__email__ = 'info@dsent.ru'


def lang_init():
    """
    Initialize a translation framework (gettext).
    Typical use::
        _ = lang_init()

    :return: A string translation function.
    :rtype: (str) -> str
    """
    _locale, _encoding = locale.getdefaultlocale()  # Default system values
    if settings.SETTINGS['locale'] is not None:
        _locale = settings.SETTINGS['locale']
    lang = gettext.translation('dungeon', 'l10n/', [_locale])
    return lang.gettext

_ = lang_init()

# TODO: Implement scene locking for multiplayer (with timeouts)
# TODO: Figure out how to OS-independently add colors to the strings
# TODO: I feel that the base classes aren't basic enough (should be no text output at all)
# TODO: Unit tests and integration tests (think sample game runs)
# TODO: cx_Freeze build via Python script (not .cmd)


class Player(object):
    """Encapsulates the properties of a player — a brave journeyman in the unfriendly lands."""

    # Only getter for this property: you can't delete it or change after creation
    @property
    def name(self):
        """
        The player's name. Read-only. Can't be set after creation.

        :rtype: str
        """
        return self._name

    def __init__(self, name=None, game_map=None, scene_ref=None):
        """
        Create a player and place him/her to the scene.

        :param name: The new player's name. If None or empty string, then "Nameless" is assumed
        :type name: str
        :param game_map: An instance of `Map` where the new player spawns.
            If set to None, then you'll have to call `enter_map` by yourself before really doing anything!
        :type game_map: Map
        :param scene_ref: A starting scene's name or Scene object itself (must be present in the game_map).
            If set to None, then default starting scene of the map is used.
        :type scene_ref: str | Scene
        """
        if (name is None) or (name == ""):
            self._name = _("Nameless")
        else:
            self._name = name

        self._inv = {}
        self._state = {}
        self._messages = dsent.lists.Queue()

        # Just for the sake of code completion engine's sanity: these are initialized in Player.enter_map() anyway
        self._map = None
        ":type: Map"
        self._scene = None
        ":type: Scene"

        if game_map is not None:
            self.enter_map(game_map, scene_ref)

    # Only getter for this property: you can operate on the dict, but can't delete it or replace completely
    @property
    def inv(self):
        """
        A dict holding the items that the player finds during his journey. E.g.:
        ::
            self.inv['ping_pong_balls'] = 10
            self.inv['weapon'] = 'Shovel'

        :rtype: dict[str, unknown]
        """
        return self._inv

    # Only getter for this property: you can operate on the dict, but can't delete it or replace completely
    @property
    def state(self):
        """
        A dict holding the player state. E.g.:
        ::
            self.state['hunger'] += 1
            self.state['hair_color'] = 'Pink'

        :rtype: dict[str, unknown]
        """
        return self._state

    # Only getter for this property: you can operate on the map, but can't delete or change it
    @property
    def map(self):
        """
        A parent game map which hosts this player.

        :rtype: Map
        """
        return self._map

    def leave_map(self):
        """
        Leave a map where the player currently is (if it is).
        """
        if self._map is not None:
            self._map.remove_player(self)
            self._map = None
            self._scene = None

    def enter_map(self, game_map, scene_ref=None):
        """
        Enter a map.

        :param game_map: An instance of `Map` where the player spawns
        :type game_map: Map
        :param scene_ref: A starting scene's name or Scene object itself (must be present in the game_map).
            If set to None then default starting scene of the map is used.
        :type scene_ref: str | Scene
        :raise KeyError: if no such scene is present in the map
        """

        # Get out from the old map (if any)
        self.leave_map()

        # Add player to the map
        self._map = game_map
        self._map.add_player(self)

        # Enter the initial scene
        # self._scene is set to None by leave_map() already so even
        # if we are re-entering the same map at the same scene,
        # Scene.enter() will think that it is a first time
        if scene_ref is None:
            scene_ref = self._map.starting_scene
        self._map.scene(scene_ref).enter(self)

    # Only getter and setter for this property: you can operate on the scene and change it, but can't delete it
    @property
    def scene(self):
        """
        The current scene for this player

        :rtype: Scene
        """
        return self._scene

    @scene.setter
    def scene(self, value):
        """
        :type value: Scene
        """
        # We don't do any actions here; they should be already initiated by Scene.enter()
        self._scene = value

    # Only getter for this property: you can operate on messages object, but can't replace or delete it
    @property
    def messages(self):
        """
        The messages queue.

        :rtype: dsent.lists.Queue
        """
        return self._messages

    def push_msg(self, message):
        """
        Add a new message to be shown to the player

        :param message:
        :type message: str
        """
        self._messages.append(message)

    def pop_msg(self):
        """
        Pops a message from the message queue for the player's reading pleasure

        :return: The oldest message in queue or None if there are none.
        :rtype: str
        """
        return next(self._messages, None)  # raise IndexError if the message queue is empty


class Scene(object):
    """
    Encapsulates a single scene of the game. Should show an introduction, parse user input and provide an outcome
    based on that input. Possible outcomes are the game's end and transfer to another scene. See `do()` docstring
    for more information.

    **Important**

    Child classes should follow some rules for overriding this class' methods:
        * `__init__()`: `Scene.__init()` must be called **before** any child class specific actions
          (except for `_name` customization - see docstring for `__init__()`)
        * `do()`: `Scene.do()` must be called **after** all child class specific actions
    """

    _class_name = 'scene'
    """
    Default way to set an identifier to the scene.
    Identifiers must be unique to each `Map` instance.
    This value must be overridden in child classes to be unique,
    unless these classes provide their own way of setting `_name` in their `__init__()` methods.
    (`_name` values still need to be unique for each scene in the each `Map` instance).

    :type: str
    """

    """
    Only getter for this property: it normally equals to the class attribute `_class_name`.
    `_name` could be changed on a per-instance basis for some reasons.
    An example would be a class which is really a factory for a number of similar scenes
    (e.g. few blocks of corridor one after another - it would be stupid
    to create a number of almost identical child classes for that task)
    """
    @property
    def name(self):
        """
        The identifier for this scene. Must be unique to each `Map` instance.

        :rtype: str
        """
        return self._name

    def __init__(self, game_map, name=None):
        """
            **Important**

            If child classes provide their own versions of `__init__()`,
            `Scene.__init()` must be called **before** any child class specific actions,
            except for `_name` customizations. If child classes set their instances' `_name`s by themselves,
            it should be done **before** calling `Scene.__init__()`.

        :param game_map: An instance of `Map` to which the new scene is added
        :type game_map: Map
        :param name: A custom name for this `Scene` instance
        :type name: str
        :return: A new instance of Scene
        :rtype: Scene
        """

        # Default initialization for _name
        if not hasattr(self, '_name'):
            if name is None:
                self._name = self._class_name
            else:
                self._name = name

        self._state = {}
        self._map = game_map
        self._map.add_scene(self)

    # Only getter for this property: you can operate on the dict, but can't delete it or replace completely
    @property
    def state(self):
        """
        A dict holding the scene state which is preserved between player visits. E.g.:
        ::
            self.state['killer_bees_alive'] = 0
        **Important**

        All child classes must add anything to `self.state` *after* it's created by `Scene.__init__()`.

        :rtype: dict[str, unknown]
        """
        return self._state

    # Only getter for this property: you can operate on the map, but can't replace it or delete
    @property
    def map(self):
        """
        A parent game map which hosts this scene.

        :rtype: Map
        """
        return self._map

    def _enter_first_time(self, plr):
        """
        Initialize a scene.

        :param plr: Player entering the scene
        :type plr: Player
        """
        # Push a message to the player about entering this brand new room
        plr.push_msg(_("You're standing in some nondescript room."))

    def _enter_again(self, plr):
        """
        Give the player a short overview of the scene.

        :param plr: Player staying in the scene
        :type plr: Player
        """
        # Push a message to the player about still staying in the room
        plr.push_msg(_("How did you do that, cheater?"))

    def enter(self, player_ref):
        """
        Initialize a scene. If player.scene == self, the last executed action did not advance
        the player to the new scene, so the message could be shorter and maybe not all initializations are needed.

        :param player_ref: The name of the player entering the scene or the Player object itself
        :type player_ref: str | Player
        """
        plr = self.map.player(player_ref)
        if plr.scene is not self:  # Scene was changed
            # Change a scene.
            plr.scene = self
            self._enter_first_time(plr)
        else:
            self._enter_again(plr)

    # TODO: Should check that the player is actually in this scene
    def do(self, player_ref, input_str, game_on=None):
        """
        Parse user input string and do something accordingly.

        **Important**

        All child classes should check for their specific actions, then call `Scene.do()`.

        :param player_ref: A player name or `Player` object itself.
        :type player_ref: str | Player
        :param input_str: An input string provided by a user using input() or some other interactive method.
        :type input_str: str
        :param game_on: True/False if the player input was processed already (e.g. in child class' own `do()` method)
        :type game_on: bool | NoneType
        :return: True if the game continues, False if the game is over.
        :rtype: bool
        """

        # Actions weren't processed elsewhere so stick with defaults
        if game_on is None:
            plr = self.map.player(player_ref)
            m = re.fullmatch(_(r'(?P<scene>exit|quit)(\s+game)?'), input_str, re.I + re.X)
            if m:  # Exit action matches
                game_on = self.action_exit(plr)
            else:
                game_on = self.action_cant_parse(plr)

        return game_on

    def action_exit(self, plr):
        """
        Default action for leaving the game.

        :type plr: Player
        :return: False (Game Over)
        :rtype: bool
        """
        plr.push_msg(_("Goodbye!"))
        return False

    def action_cant_parse(self, plr):
        """
        Default action for unrecognized user input.

        :type plr: Player
        :return: False (Game Over)
        :rtype: bool
        """
        plr.push_msg(_("I don't understand that."))
        return False


class Map(object):
    """
    Encapsulates a single game map with all its scenes and all players currently there.
    """

    _class_name = _("Very Small Dungeon")

    def __init__(self, name=None, starting_scene=None):
        """
            **Important**

            If child classes provide their own versions of `__init__()`,
            `Map.__init()` must be called **before** any child class specific actions,
            except for `_name` customizations. If child classes set their instances' `_name`s by themselves,
            it should be done **before** calling `Map.__init__()`.
            All child classes should add scenes in their constructors.
            This one doesn't do that because it's really basic.

        :param name: A custom name for this `Map` instance
        :type name: str
        :param starting_scene: Default starting scene name.
            If not present, should be set by __init__() method of child classes
        :type starting_scene: str
        :return: A new instance of Map
        :rtype: Map
        """

        # Default initialization for _name
        if not hasattr(self, '_name'):
            if name is None:
                self._name = self._class_name
            else:
                self._name = name

        self._starting_scene = starting_scene
        self._scenes = {}
        """:type: dict[str, Scene]"""
        self._scenes_view = types.MappingProxyType(self._scenes)
        self._players = {}
        """:type: dict[str, Player]"""
        self._players_view = types.MappingProxyType(self._players)

    # Only getter; Name could be set on creation only
    @property
    def name(self):
        """
        A name of this glorious `Map`.

        :rtype: str
        """
        return self._name

    # Only getter; returns read-only view of the scenes dict.
    # Any modifications to scenes are allowed only through add_scene() and remove_scene() methods.
    @property
    def scenes(self):
        """
        A dict holding all the scenes currently in the map.
        It is populated only by scenes themselves on creation using add_scene(). E.g.:
        ::
            my_dungeon = Map()
            _ = Scene(my_dungeon)
            _ = Player(my_dungeon, 'scene', 'James')
            my_dungeon.scenes['scene'].enter('James')

        :rtype: dict[str, Scene]
        """
        return self._scenes_view

    # Only getter; returns read-only view of the players dict.
    # Any modifications to players are allowed only through add_player() and remove_player() methods.
    @property
    def players(self):
        """
        A read-only dict holding references to all players in the map.
        It is populated by players themselves on creation using add_player(). E.g.:
        ::
            my_dungeon = Map()
            _ = Scene(my_dungeon)
            _ = Player(my_dungeon, 'scene', 'James')
            my_dungeon.scenes['scene'].enter('James')

        :rtype: dict[str, Player]
        """
        return self._players_view

    @property
    def starting_scene(self):
        return self._starting_scene

    @starting_scene.setter
    def starting_scene(self, value):
        """

        :type value: str | Scene
        :raise KeyError: if the scene with that name doesn't exists in the map
        """
        self._starting_scene = self.scene(value).name  # self.scene raises KeyError if no such scene was added

    @staticmethod
    def _add_entity(obj, ent_dict, obj_caption):
        """
        Generic function to add entities (currently players and scenes) to the map.

        :param obj: a player or scene to add
        :type obj: Player | Scene
        :param ent_dict: a map dictionary to modify (_scenes or _players)
        :type ent_dict: dict[str, Player] | dict[str, Scene]
        :param obj_caption: a caption for error messages ('scene' or 'player')
        :type obj_caption: str
        :raise RuntimeError: If the object with the same name already exists in this map.
        """
        if obj.name in ent_dict:  # Object names must be unique to a map
            if ent_dict[obj.name] is obj:  # This particular object is already added
                raise RuntimeError('The {} `{}` was already added to the map.'.format(obj_caption, obj.name))
            else:  # Another object with the same name exists
                raise RuntimeError(
                    'The map already contains another {} with the name `{}`.'
                    ''.format(obj_caption, obj.name)
                )
        ent_dict[obj.name] = obj

    def add_scene(self, scene):
        """
        Insert a new scene to the map. Should be called by Scene instances on creation.

        :param scene: A new scene to add.
        :type scene: Scene
        :raise RuntimeError: If the scene with the same name already exists in this map.
        """
        self._add_entity(scene, self._scenes, 'scene')

    def add_player(self, player):
        """
        Insert a new player to the map. Should be called by Player instances on creation.

        :param player: A new player to add.
        :type player: Player
        :raise RuntimeError: If the player with the same name already exists in this map.
        """
        self._add_entity(player, self._players, 'player')
        player.push_msg(_('Welcome, player {} to the map {}!').format(player.name, self.name))

    @staticmethod
    def _get_entity(obj_ref, ent_dict, obj_caption):
        """
        Generic function to retrieve entities (currently players and scenes)
        from the map by their names or objects themselves

        :param obj_ref: a player or scene name to get or these objects themselves
        :type obj_ref: str | Player | Scene
        :param ent_dict: a map dictionary to search (_scenes or _players)
        :type ent_dict: dict[str, Player] | dict[str, Scene]
        :param obj_caption: a caption for error messages ('scene' or 'player')
        :type obj_caption: str
        """
        if isinstance(obj_ref, str):  # Assume that object name is provided
            obj_ref = ent_dict[obj_ref]  # This raises KeyError if this object name doesn't exist in this map
        elif ent_dict[obj_ref.name] is not obj_ref:  # Different object with the same name!
            raise KeyError(
                'The {} name `{}` is found but associated with different object.'
                ''.format(obj_caption, obj_ref.name))
        return obj_ref

    def scene(self, scene_ref):
        """
        Return a scene from this map by its name or the scene itself.

        :param scene_ref: The scene name or Scene object
        :type scene_ref: Scene | str
        :raise KeyError: If the scene doesn't exist in the map.
        :rtype: Scene
        """
        return self._get_entity(scene_ref, self._scenes, 'scene')

    def player(self, player_ref):
        """
        Return a player from this map by its name or the player itself.

        :param player_ref: The player name or Player object
        :type player_ref: Player | str
        :raise KeyError: If the player doesn't exist in the map.
        :rtype: Player
        """
        return self._get_entity(player_ref, self._players, 'player')

    def remove_scene(self, scene_ref):
        """
        Remove a scene from the map.

        :param scene_ref: A scene to remove or its name
        :type scene_ref: Scene | str
        :raise RuntimeError: If the scene couldn't be removed (e.g. some players on the map are in this scene now).
        :raise KeyError: If the scene doesn't exist.
        """
        the_scene = self.scene(scene_ref)  # Resolve a scene reference to Scene object

        # Check if any of the players is currently in the scene to be deleted
        for _, p in self._players:  # dict[str, Player]
            assert isinstance(p, Player)  # A hint for code completion
            if p.scene is scene_ref:
                raise RuntimeError('The scene `{}` is used by the player `{}`.'.format(the_scene.name, p.name))

        del self._scenes[scene_ref.name]

    def remove_player(self, player_ref):
        """
        Remove a player from the map.

        :param player_ref: A player to remove or its name
        :type player_ref: Player | str
        :raise KeyError: If the player doesn't exist in the map.
        """
        the_player = self.player(player_ref)  # Resolve a player reference to Player object
        del self._players[the_player.name]


class Game(object):
    """
    Encapsulates a simplest form of interactive single player console game session with a single map.
    Generally this class shouldn't be subclassed, just copied and modified if needed.
    """

    def __init__(self, map_cls, plr_cls):
        """

        :param map_cls: a class name of the map object (must be a subclass of Map)
        :param plr_cls: a class name of the player object (must be a subclass of Player)
        """
        self._map = map_cls()
        """:type: Map"""
        self._player = plr_cls(input(_("Tell me your name: ")), self._map)
        """:type: Player"""

    def play(self):
        """
        Main interactive game loop.
        """
        game_on = True
        while game_on:
            # if self._player.scene is None:  # The very first scene
            #     self._map.scene(self._map.starting_scene).enter(self._player)
            # else:  # Normal scene
            #     self._player.scene.enter(self._player)
            for m in self._player.messages:
                print(m)
            inp = input(_("> "))
            game_on = self._player.scene.do(self._player, inp)
        for m in self._player.messages:  # Final messages
            print(m)
        input(_("Press Enter to exit."))


if __name__ == '__main__':
    pass
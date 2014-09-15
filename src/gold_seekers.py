"""This is a sample game built using a dungeon engine"""

import re

from src.dungeon import *


__author__ = 'dsent'

_ = lang_init()


class NormalScene(Scene):
    _class_name = 'normal'

    _msg_nonsense = (
        _("You haven't really thought that was an option, have you?"),
        _("That would be stupid, don't you think?"),
        _("No way. Just no freaking way."),
        _("The thought of doing that suddenly gave you chills. No, you won't do that."),
        _("That's simply not possible."),
        _("It's no use doing that. You should have tried something else."),
    )

    _msg_excitement = (
        (2, _("enthusiastic")),
        (4, _("excited")),
        (6, _("active")),
        (8, _("calm")),
        (10, _("bored")),
        (12, _("extremely bored")),
        (14, _("fed up with your life")),
    )

    def action_cant_parse(self, plr):
        """
        :type self: NormalScene
        :type plr: Player
        """
        plr.push_msg(random.choice(self._msg_nonsense))

        exc1 = self._excitement(plr.state['boredom'])
        plr.state['boredom'] += 1
        exc2 = self._excitement(plr.state['boredom'])

        if not exc2:  # Maximum level of boredom reached
            plr.push_msg(_("You were bored to death."))
            return False
        elif exc2 != exc1:  # The level of boredom changed
            plr.push_msg(_("Not advancing is boring. You're now {}.").format(exc2))

        plr.scene.enter(plr)  # Re-enter current scene

        return True

    def _excitement(self, level):
        """
        :type self: NormalScene
        :type level: int
        """
        for i, (lvl, m) in enumerate(self._msg_excitement):
            if level <= lvl:
                return m
        return False  # death from boredom

    def _something_changed(self, plr):
        """
        :type self: NormalScene
        :type plr: Player
        """
        if plr.state['boredom'] > 2:
            if plr.state['boredom'] <= 10:
                plr.state['boredom'] = 0
            else:
                plr.state['boredom'] -= 10
            plr.push_msg(_("That was refreshing. You're now {}.").format(self._excitement(plr.state['boredom'])))


class NormalPlayer(Player):
    def __init__(self, name=None, game_map=None, scene_ref=None):
        super(NormalPlayer, self).__init__(name, game_map, scene_ref)
        self.state['boredom'] = 0


class EntranceScene(NormalScene):
    _class_name = 'entrance'

    def _enter_first_time(self, plr):
        """
        :type self: EntranceScene
        :type plr: Player
        """
        plr.push_msg(_("You're at the entrance."))

    def _enter_again(self, plr):
        """
        :type self: EntranceScene
        :type plr: Player
        """
        plr.push_msg(_("You're still at the entrance."))

    def do(self, player_ref, input_str, game_on=None):
        """
        :type self: EntranceScene
        :type player_ref: str | Player
        :type input_str: str
        :type game_on: bool
        """
        plr = self.map.player(player_ref)
        # Actions weren't processed elsewhere so stick with defaults
        if game_on is None:
            m = re.fullmatch(
                _(r"(?P<entrance>open door|go through)"), input_str, re.I + re.X)
            if m:  # Open door action matches
                game_on = self.action_open_door(plr)
            else:
                game_on = super(EntranceScene, self).do(plr, input_str)

        return game_on

    def action_open_door(self, plr):
        """
        :type self: EntranceScene
        :type plr: Player
        """
        plr.push_msg(_("The door opens. You leap into the doorway!"))
        self._something_changed(plr)
        self._map.scene('first').enter(plr)
        return True


class FirstScene(NormalScene):
    _class_name = 'first'

    def _enter_first_time(self, plr):
        """
        :type self: FirstScene
        :type plr: Player
        """
        plr.push_msg(_("You're in a dark room. There are three doors: left, right and center."))

    def _enter_again(self, plr):
        """
        :type self: FirstScene
        :type plr: Player
        """
        plr.push_msg(_("You're still in the dark room with three doors."))

    def do(self, player_ref, input_str, game_on=None):
        """
        :type self: FirstScene
        :type player_ref: str | Player
        :type input_str: str
        :type game_on: bool
        """
        plr = self.map.player(player_ref)
        # Actions weren't processed elsewhere so stick with defaults
        if game_on is None:
            dispatch = (
                (_(r"(?P<first>left|first)(\s+door)?"), self.action_left),
                (_(r"(?P<first>right|second)(\s+door)?"), self.action_right),
                (_(r"(?P<first>center|central|third)(\s+door)?"), self.action_center),
            )
            for r_exp, action in dispatch:
                m = re.fullmatch(r_exp, input_str, re.I + re.X)
                if m:  # action matches
                    game_on = action(plr)
                    break
            else:  # if not a single expression matched
                game_on = super(FirstScene, self).do(plr, input_str)

        return game_on

    def action_left(self, plr):
        """
        :type self: FirstScene
        :type plr: Player
        """
        plr.push_msg(_("Excellent choice! Or not."))
        self._something_changed(plr)
        self._map.scene('bear').enter(plr)
        return True

    def action_right(self, plr):
        """
        :type self: FirstScene
        :type plr: Player
        """
        plr.push_msg(_("Fantastic choice! No, wait, it isn't."))
        self._something_changed(plr)
        self._map.scene('cthulhu').enter(plr)
        return True

    def action_center(self, plr):
        """
        :type self: FirstScene
        :type plr: Player
        """
        plr.push_msg(_("You were asking for trouble."))
        self._something_changed(plr)
        self._map.scene('lava').enter(plr)
        return True


class BearScene(NormalScene):
    _class_name = 'bear'

    def __init__(self, game_map, name=None):
        super(BearScene, self).__init__(game_map, name)
        self._state['bear_moved'] = False

    def enter(self, player_ref):
        super(BearScene, self).enter(player_ref)

        plr = self.map.player(player_ref)
        if self._state['bear_moved']:
            plr.push_msg(_("Bears sits a few feet away from the door."))
        else:
            plr.push_msg(_("Bears sits in front of a door."))

    def _enter_first_time(self, plr):
        plr.push_msg(_("There is a fat bear here. He has a pot of honey. There is a door right before you."))

    def _enter_again(self, plr):
        plr.push_msg(_("The bear is still here."))

    def do(self, player_ref, input_str, game_on=None):
        """
        :type self: BearScene
        :type player_ref: str | Player
        :type input_str: str
        :type game_on: bool
        """
        plr = self.map.player(player_ref)
        # Actions weren't processed elsewhere so stick with defaults

        if game_on is None:
            dispatch = (
                (_(r"(?P<bear>take\s+)?(honey|pot)"), self.action_honey),
                (_(r"(?P<bear>taunt|scream)(\s+at)?(\s+bear)?"), self.action_taunt),
                (_(r"(?P<bear>open door|go through)"), self.action_door),
            )
            for r_exp, action in dispatch:
                m = re.fullmatch(r_exp, input_str, re.I + re.X)
                if m:  # action matches
                    game_on = action(plr)
                    break
            else:  # if not a single expression matched
                game_on = super(BearScene, self).do(plr, input_str)

        return game_on

    def action_honey(self, plr):
        """
        :type self: BearScene
        :type plr: Player
        """
        plr.push_msg(_("The bear looks at you then slaps your face off."))
        return False

    def action_taunt(self, plr):
        """
        :type self: BearScene
        :type plr: Player
        """
        if self._state['bear_moved']:
            plr.push_msg(_("The bear gets pissed off and chews your leg off."))
            return False
        else:
            self._state['bear_moved'] = True
            plr.push_msg(_("The bear moves away from the door."))
            self._something_changed(plr)
            return True

    def action_door(self, plr):
        """
        :type self: BearScene
        :type plr: Player
        """
        if self._state['bear_moved']:
            plr.push_msg(_("The bear didn't even look at you as you passed it."))
            self._something_changed(plr)
            self._map.scene('gold').enter(plr)
            return True
        else:
            plr.push_msg(_("The bear eats your belly."))
            return False


class CthulhuScene(NormalScene):
    _class_name = 'cthulhu'

    def _enter_first_time(self, plr):
        plr.push_msg(_("You see Cthulhu. You can try to flee or eat your head."))

    # _enter_again from Scene does what we need: 'cheater' message

    def do(self, player_ref, input_str, game_on=None):
        """
        :type self: CthulhuScene
        :type player_ref: str | Player
        :type input_str: str
        :type game_on: bool
        """
        plr = self.map.player(player_ref)
        # Actions weren't processed elsewhere so stick with defaults

        if game_on is None:
            dispatch = (
                (_(r"(?P<cthulhu>flee)"), self.action_flee),
                (_(r"(?P<cthulhu>(?:eat)?(?:\s*\bmy)?(?:\s*\bhead)?(?<!^))"), self.action_head),
                (_(r"(?P<cthulhu>.*)"), self.action_head_anyway),
            )
            for r_exp, action in dispatch:
                m = re.fullmatch(r_exp, input_str, re.I + re.X)
                if m:  # action matches
                    game_on = action(plr)
                    break
            else:  # if not a single expression matched
                game_on = super(CthulhuScene, self).do(plr, input_str)

        return game_on

    def action_flee(self, plr):
        """
        :type self: CthulhuScene
        :type plr: Player
        """
        plr.push_msg(_("Cthulhu didn't follow you. You got away."))
        self._something_changed(plr)
        self._map.scene('first').enter(plr)
        return True

    def action_head(self, plr):
        """
        :type self: CthulhuScene
        :type plr: Player
        """
        plr.push_msg(_("You smiled as you ate your head. That was yummy!"))
        return False

    def action_head_anyway(self, plr):
        """
        :type self: CthulhuScene
        :type plr: Player
        """
        plr.push_msg(_("You didn't feel like doing it and ate your head instead. It was yummy!"))
        return False


class GoldScene(NormalScene):
    _class_name = 'gold'

    def _enter_first_time(self, plr):
        plr.push_msg(_("This room is full of gold. You should take some."))

    # _enter_again from Scene does what we need: 'cheater' message

    def do(self, player_ref, input_str, game_on=None):
        """
        :type self: GoldScene
        :type player_ref: str | Player
        :type input_str: str
        :type game_on: bool
        """
        plr = self.map.player(player_ref)
        # Actions weren't processed elsewhere so stick with defaults

        if game_on is None:
            m = re.fullmatch(_(r"(?P<amount>(?:\\d+[.,]?\\d*|none|nothing|zero))"), input_str, re.I + re.X)
            if m:  # action matches
                game_on = self.action_gold(plr, m)
            else:  # if not a single expression matched
                game_on = self.action_none(plr)

        return game_on

    def action_gold(self, plr, match):
        """

        :type self: GoldScene
        :type plr: Player
        """
        if match.group('amount') in [_('none'), _('nothing'), _('zero')]:
            amount = 0
        else:
            amount = float(match.group('amount').replace(',', '.'))

        if amount <= 50:
            plr.push_msg(_("Nice, you're not greedy!"))
        else:
            plr.push_msg(_("You're greedy bastard!"))

        return False

    def action_none(self, plr):
        """
        :type self: GoldScene
        :type plr: Player
        """
        plr.push_msg(_("You can't even enter a number? You die of dumbness."))
        return False


class LavaScene(NormalScene):
    _class_name = 'lava'

    def _enter_first_time(self, plr):
        """
        :type self: LavaScene
        :type plr: Player
        """
        plr.push_msg(_("The room is filled with lava."))

    # _enter_again from Scene does what we need: 'cheater' message

    def do(self, player_ref, input_str, game_on=None):
        """
        :type self: LavaScene
        :type player_ref: str | Player
        :type input_str: str
        :type game_on: bool
        """
        plr = self.map.player(player_ref)
        # Actions weren't processed elsewhere so stick with defaults
        if game_on is None:
            game_on = self.action_lava_death(plr)

        return game_on

    def action_lava_death(self, plr):
        """
        :type self: LavaScene
        :type plr: Player
        """
        plr.push_msg(_("You fall to the bottom and die."))
        return False


class SimpleMap(Map):
    _class_name = _("The Underground Realm of the Dread Lord Cthulhu")

    def __init__(self):
        super(SimpleMap, self).__init__()
        _ = EntranceScene(self)
        _ = FirstScene(self)
        _ = CthulhuScene(self)
        _ = LavaScene(self)
        _ = BearScene(self)
        _ = GoldScene(self)
        self.starting_scene = 'entrance'


if __name__ == '__main__':
    def test_default_dungeon():
        # Test default dungeon classes
        my_dungeon = Map()  # This class is not intended to be really used so it doesn't create its scenes
        dumb_scene = Scene(my_dungeon)  # Let's add a scene manually
        my_dungeon.starting_scene = dumb_scene  # And set is as default
        james = Player("James", my_dungeon)
        game_on = True
        while game_on:
            for m in james.messages:
                print(m)
            inp = input(_("> "))
            game_on = james.scene.do(james, inp)
        for m in james.messages:
            print(m)
    pass
    # test_default_dungeon()

    def test_simplest_dungeon():
        # Test simplest dungeon classes
        my_dungeon = SimpleMap()
        plr = NormalPlayer(input(_("Tell me your name: ")), my_dungeon)
        game_on = True
        while game_on:
            for m in plr.messages:
                print(m)
            inp = input(_("> "))
            game_on = plr.scene.do(plr, inp)
        for m in plr.messages:
            print(m)
    pass
    # test_simplest_dungeon()

    def test_simplest_dungeon2():
        # Test simplest dungeon with a Game class
        g = Game(SimpleMap, NormalPlayer)
        g.play()
    pass
    test_simplest_dungeon2()


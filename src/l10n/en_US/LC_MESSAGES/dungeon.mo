��    F      L  a   |         /        1     P  (   n  5   �     �     �  "   �  )        <  !   \     ~     �  )   �     �  (   �       %   ,     R     [     y  =   �     �     �     �  '   	     8	     M	  #   a	  &   �	     �	  /   �	  2   �	     +
  0   E
     v
  /   �
  "   �
  *   �
       J   *  R   u  0   �     �  !     3   .  F   b     �  8   �  6     0   9     j     �     �     �  E   �  )        ?  /   ]     �     �     �     �     �     �     �     �     �     �  �  �  �   �    �  f  �  �     "  �       �             	  #    -  z   9     �  �   �  �     �        �  %        8  "   I  ;   l  =   �     �  \   �     P  =   n     �  (   �  3   �  &         E   /   a   C   �   ~   �   B   T!  _   �!  N   �!     F"  �   �"  �   W#  J   �#  �   )$  0   �$  6   �$  L    %  C   m%  K   �%  �  �%  8   �'  �   �'  5   �(     �(    �(  �   �)  P   �*  �  �*  t   �,  z    -  �   {-     .     .     %.     *.     7.     ?.     O.     e.     j.     r.        <   -   "       )          #      
              &   4   ?   (                          1      =             B      9      8   >   +              5             ;       F             :   	      .   A   !       ,   *                     $       6   '   E                      2   3   7                     %      /   C           @              D      0    (?P<amount>(?:\\d+[.,]?\\d*|none|nothing|zero)) (?P<bear>open door|go through) (?P<bear>take\s+)?(honey|pot) (?P<bear>taunt|scream)(\s+at)?(\s+bear)? (?P<cthulhu>(?:eat)?(?:\s*\bmy)?(?:\s*\bhead)?(?<!^)) (?P<cthulhu>.*) (?P<cthulhu>flee) (?P<entrance>open door|go through) (?P<first>center|central|third)(\s+door)? (?P<first>left|first)(\s+door)? (?P<first>right|second)(\s+door)? (?P<scene>exit|quit)(\s+game)? >  Bears sits a few feet away from the door. Bears sits in front of a door. Cthulhu didn't follow you. You got away. Excellent choice! Or not. Fantastic choice! No, wait, it isn't. Goodbye! How did you do that, cheater? I don't understand that. It's no use doing that. You should have tried something else. Nameless Nice, you're not greedy! No way. Just no freaking way. Not advancing is boring. You're now {}. Press Enter to exit. Tell me your name:  That was refreshing. You're now {}. That would be stupid, don't you think? That's simply not possible. The Underground Realm of the Dread Lord Cthulhu The bear didn't even look at you as you passed it. The bear eats your belly. The bear gets pissed off and chews your leg off. The bear is still here. The bear looks at you then slaps your face off. The bear moves away from the door. The door opens. You leap into the doorway! The room is filled with lava. The thought of doing that suddenly gave you chills. No, you won't do that. There is a fat bear here. He has a pot of honey. There is a door right before you. This room is full of gold. You should take some. Very Small Dungeon Welcome, player {} to the map {}! You can't even enter a number? You die of dumbness. You didn't feel like doing it and ate your head instead. It was yummy! You fall to the bottom and die. You haven't really thought that was an option, have you? You see Cthulhu. You can try to flee or eat your head. You smiled as you ate your head. That was yummy! You were asking for trouble. You were bored to death. You're at the entrance. You're greedy bastard! You're in a dark room. There are three doors: left, right and center. You're standing in some nondescript room. You're still at the entrance. You're still in the dark room with three doors. active bored calm enthusiastic excited extremely bored fed up with your life none nothing zero Project-Id-Version: dungeon
POT-Creation-Date: 2014-09-15 01:33+0400
PO-Revision-Date: 2014-09-15 09:56+0400
Last-Translator: Danila Sentyabov <info@dsent.ru>
Language-Team: 
Language: en_US
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Generator: Poedit 1.6.9
X-Poedit-Basepath: .
Plural-Forms: nplurals=2; plural=(n != 1);
X-Poedit-SourceCharset: UTF-8
X-Poedit-SearchPath-0: ../../..
 # Debugged
(?:i)?
(?:\s*\bwill|(?<=i)'ll)?
(?:\s*\bhave|(?<=i)'ve)?
(?:\s*\b
  (?:taken?|g[eo]t|st(?:eal|olen?)|snatch(?:ed)?)
)?
(?:\s*\b
  (?P<amount>
    (?:\d+[.,]?\d*|none|nothing|zero)
  )
)
(?:\s*\bgold)?
(?:\s*\b(?:coins?|items?))?
[.!]? # Debugged
(?:i)?
(?:\s*\bwill|(?<=i)'ll)?
(?:\s*\bhave|(?<=i)'ve)?
(\s*\b
  (?:open(?:ed)?|go(?:ne)?|went)?
  (?:\s*\bforward)?
)?
(?:\s*\bthrough)?
(?:\s*\b(?:the|that|this|front))?
# If <action> group matched, then door is optional
\s*(?(1)(?:\bdoor)?|\bdoor)
[.!]? # Debugged(?:i)?
(?:\s*\bwill|(?<=i)'ll)?
(?:\s*\bhave|(?<=i)'ve)?
(\s*\b
  (?:taken?|took|eat(?:en)?|ate|g[eo]t)
)?
(?:\s*\b(?:the|that|its|his|(?:the\s*\b)?bear's|bear))?
# If <action> group matched, then pot is optional
(?(1)
  (?:\s*\b((?:pot\s+of\s+)?honey(?:\s+pot)?|pot))?|
  \s*\b(?:(?:pot\s+of\s+)?honey(?:\s+pot)?|pot))  # Otherwise mandatory
[.!]? # Debugged
(?:i)?
(?:\s*\bwill|(?<=i)'ll)?
(?:\s*\bhave|(?<=i)'ve)?
(\s*\b
  (?:taunt(?:ed)?|scream(?:ed)?|lull(?:ed)?|s[iau]ng)
)
(?:\s*\b(?:to|at))?
(?:\s*\b(?:him|it|(?:(?:the|that|this)\s*\b)?(?:bear|animal)))?
[.!]? # Debugged
(?:i)?
(?:\s*\bwill|(?<=i)'ll)?
(?:\s*\bhave|(?<=i)'ve)?
(\s*\b
  (?:eat(?:en)?|ate|chew(?:ed)?|swallow(?:ed)?)
)?
(?:\s*\bon)?
(?:\s*\bmy)?
(?:\s*\bown)?
# If <eat> group matched, then head is optional
(?(1)(?:\s*\bhead)?|\s*\bhead)
(?(1)|\s*\b(?:eaten|chewed|swallowed))?
[.!]? # Debugged
.* # Debugged
(?:i)?
(?:\s*\bwill|(?<=i)'ll)?
(?:\s*\bhave|(?<=i)'ve)?
(\s*\b
  (?:fle(?:e|d)|r[ua]n|go(?:ne)?|went|escaped?)
)
(?:\s*\baway)?
(?:\s*\bfrom)?
(?:\s*\bout(?:\s+of)?)?
(?:\s*\b(?:him|there|it|(?:the\s+)?room|cthulhu))?
[.!]? # Debugged
(?:i)?
(?:\s*\bwill|(?<=i)'ll)?
(?:\s*\bhave|(?<=i)'ve)?
(\s*\b
  (?:open(?:ed)?|go(?:ne)?|went)?
  (?:\s*\bforward)?
)?
(?:\s*\bthrough)?
(?:\s*\b(?:the|that|this|front))?
# If <action> group matched, then door is optional
\s*(?(1)(?:\bdoor)?|\bdoor)
[.!]? # Debugged
(?:i)?
(?:\s*\bwill|(?<=i)'ll)?
(?:\s*\bhave|(?<=i)'ve)?
(?:\s*\b
  (?:open(?:ed)?|go(?:ne)?|went|select(?:ed)?|turn(?:ed)?|taken?|took)?
)?
(?:\s*\b(?:to|through)?)?
(?:\s*\bthe)?
(?:\s*\b
  (?:center|central|third|3(?:-?rd)?)
)
(?:\s*\b(?:side|door|one)?)?
[.!]? # Debugged
(?:i)?
(?:\s*\bwill|(?<=i)'ll)?
(?:\s*\bhave|(?<=i)'ve)?
(?:\s*\b
  (?:open(?:ed)?|go(?:ne)?|went|select(?:ed)?|turn(?:ed)?|taken?|took)?
)?
(?:\s*\b(?:to|through)?)?
(?:\s*\bthe)?
(?:\s*\b
  (?:left|first|1(?:-?st)?)
)
(?:\s*\b(?:side|door|one)?)?
[.!]? # Debugged
(?:i)?
(?:\s*\bwill|(?<=i)'ll)?
(?:\s*\bhave|(?<=i)'ve)?
(?:\s*\b
  (?:open(?:ed)?|go(?:ne)?|went|select(?:ed)?|turn(?:ed)?|taken?|took)?
)?
(?:\s*\b(?:to|through)?)?
(?:\s*\bthe)?
(?:\s*\b
  (?:right|second|2(?:-?nd)?)
)
(?:\s*\b(?:side|door|one)?)?
[.!]? # Debugged
(?:i)?
(?:\s*\bwill|(?<=i)'ll)?
(?:\s*\bhave|(?<=i)'ve)?
(?:\s*\b(?:exit|quit))
(?:\s*\b(?:the\s+)?game)?
[.!]? What do you do?  The bear sits a few feet away from the door minding his own business.
Maybe it's time to just go through the door.
Or move it a little bit more. Or take its honey, that looks delicious! The bear doesn't look very aggressive, but it sits right in front of the door.
Maybe you should move it somehow. Or just squeeze past it. Or take its honey. The mighty Cthulhu have all the time in the world and doesn't chase petty worms like you.
You've got away for now. Your insanity receded slowly.
He will see you rot eventually though — just a moment later in his eyes. Excellent choice! Or not. Fantastic choice! No, wait, it isn't. Come again soon! How did you do that, you cheater?! I can't understand a word. Let's assume you lose this game. It's no use doing that. You should have tried something else. The Nameless Nice, you're not greedy! You go through the door with your bounty.
You've just won the game! No way. Just no freaking way.  /Not getting anywhere isn't good for health!
 /You're now {} Press Enter to exit. How do I call you, fearless adventurer?   /That was a refreshing experience!
 /You're now {} That would be stupid, don't you think? That's simply not possible. The Underground Realm of the Dread Lord Cthulhu That was smooth! The bear didn't even look at you as you passed it. Good! The bear have taken a good bite of your belly
as you tried to squeeze past it to the door.
You've bled to death quickly. Awesome! The bear gets pissed off and chews your leg off.
You die. You're still in the same room with a bear and his honey.
There is a door right in front of you. A clever thing to do! The bear looks at you then slaps your face off.
You die. Nicely done! The bear has moved from the door looking slightly annoyed.
The way seems free now. But is it safe to go through?.. The door opens. Excitedly, you leap into the doorway, eager for adventures!
A door closed behind you with a sinister thud. There is no way back. The room has no floor and is filled with molten lava down there.
You balance on your toes at the threshold for a moment and then fall. The thought of doing that suddenly gave you chills. No, you won't do that. There is only one door besides the one you came from, right in front of you.
And there is a bear in the room. The bear has a big pot of honey. This room is full of gold. You should take some. The Kingdom of Very Small and Immensely Boring Dungeon Welcome, noble traveller {}!
The fate brought you to the sacred lands of {}! You couldn't figure out how to enter a number? You die of dumbness. You didn't feel like doing it and devoured your head instead. It was yummy! If you thought that could save you, it didn't work. You fall to the bottom.
You tried to scream for a little bit. It isn't a trivial task with your vocal cords burned.
It got even harder when your lungs collapsed.
It stopped worrying you in a few seconds though.
To put it into perspective, that was a pretty nice death. Almost as good as it gets in this game.
Try find the Hall of Cthulhu next time for the sake of comparison. You haven't really thought that was an option, have you? Here you see the great evil Cthulhu.
He, it, whatever stares at you and you go insane.
You may try to flee for your life or accept your fate and eat your head. You smiled as you devoured your head. That was yummy! You were asking for trouble. That's it. Your life is just meaningless!
You can't stand the thought of aimlessly roaming these damp dungeons for another second.
The existential anguish fills up your soul and your heart gives up.
Your body goes limp as you fall on the floor.
You die from boredom. Good job, you! You're standing at the entrance of the dungeon.
The entrance is lit dimly by the couple of torches on the walls.
There is a door right in front of you. You're greedy bastard! The God of Greediness comes and eats your greedy ass off. You're in a dungeon. The room is pretty dark.
You see three doors before your eyes. The one to your left has claw marks on it. Really large ones.
And a few large bumps clearly made by something from the other side.
The one to your right is covered by ominous ornaments
that make your head spin if you look at them for a couple of seconds.
The one at the center lacks any features except that it is very massive and possibly fireproof. You're standing in some nondescript room without any features.
There are no doors. No windows. Nothing to do at all. You're still standing at the entrance of the dungeon.
There is a door right in front of you. It's cold out here, you know. You're still standing in a dark room with three doors.
To the left — claw-marked one, plain at the center and the one with strange ornaments to the right. active bored calm enthusiastic excited extremely bored fed up with your life none nothing zero 
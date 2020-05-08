# Bomberman
Well known bomberman game written in python.

# About the game

Bomberman (ボンバーマン, Bonbāman, also briefly known as Dyna Blaster in Europe) is a strategic, maze-based video game franchise
originally developed by Hudson Soft and currently owned by Konami. The first game in the series was released in Japan in
December 20, 1985 (1987 in the US)  and new games have been published at irregular intervals ever since.
Today, Bomberman has featured in over 70 different games on numerous platforms. 

[You can read more about it here](https://en.wikipedia.org/wiki/Bomberman)

# Main rules of the game
  * Player's goal is to kill all ghost wandering around
  * Player has 5 HP at the beggining (it changes with futher level), if he gets hit buy a bomb's fire or steps on any ghosts - his HP
is being reduced
  * Game ends when player's HP is 0
  * Player can destroy blocks and kill ghost by placing bombs at any place on the map

# Level system
After passing the level player's stats are reduced respectively:
  * LEVEL > 5 =>  BOMB AMOUNT -= 1, BOMB RANGE -= 1
  * LEVEL > 10 => PLAYER'S SPEED -= 1
  * LEVEL > 15 => PLAYER's HEALTH -= 1 (PLAYER CANNOT DIE BECAUSE OF IT)

# How to play
* Menu: pressing particular button with mouse
* In game:
  - Movement: ARROWS - UP, DOWN, LEFT, RIGHT
  - Placing bomb: SPACEBAR
  
# Description of created classes
##### Character
Basic class initializing basic statistics of a player and simple methods for collision

##### Player
Main player class extending Character's class. That class handles movement with arrows and placing bombs

##### Ghost
Ghost class handles movement of the bots.

##### Bomb
Class for creating a bomb, finding blocks to set fire, checking if there's collision with player/ghosts/bricks after explosion,
picking proper animation frame

##### Button
It creates a button at any place with a particular size. Additionaly handles mouse hover.

##### SpriteTool
Loading sprite to memory, picking right frame.
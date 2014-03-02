import sys, pygame
from GameEngine import *


GameScreenFactory.prepare_screen_factory_for_creation("../GameImpl/Properties/")

screen = GameScreen(400, 400)

background = ExtendedDrawable(screen.getCenter()[0], screen.getCenter()[1], screen)
screen.add_active_game_object(background)

hero = BasicMovingCharacter(screen.getCenter()[0], screen.getCenter()[1], 13, 49, screen)
hero.actions = {BasicMovingCharacter.MOVE_ACTION : BasicMovingCharacter_MoveAction(), BasicMovingCharacter.STOP_ACTION : BasicMovingCharacter_StopAction()}
hero.steering = {Direction.UP : pygame.K_w, Direction.DOWN : pygame.K_s, Direction.LEFT : pygame.K_a, Direction.RIGHT : pygame.K_d}

hero2 = BasicRotatingCharacter(screen.getCenter()[0], screen.getCenter()[1], 43, 43, screen, Default.GAME_ENGINE_TEXTURES_PATH + "basicRotatingCreature/stop/rot_001.png")
hero2.actions = {BasicRotatingCharacter.MOVE_ACTION : BasicRotatingCharacter_MoveAction(), BasicRotatingCharacter.ROTATE_STOP_ACTION : BasicRotatingCharacter_RotateStopAction()}
hero2.collisionGroups = {"all" : [ (11,7), (29,6), (35,26), (21,40), (7,26)] }

screen.add_active_game_object(hero2)
screen.add_active_game_object(hero)

GameScreenFactory.add_game_screen("basic", screen)
 


screen2 = GameScreen(300,300)

background = ExtendedDrawable(screen2.getCenter()[0], screen2.getCenter()[1], screen2)
screen2.add_active_game_object(background)

hero3 = BasicMovingCharacter(screen2.getCenter()[0], screen2.getCenter()[1], 13, 49, screen2)
hero3.actions = {BasicMovingCharacter.MOVE_ACTION : BasicMovingCharacter_MoveAction(), BasicMovingCharacter.STOP_ACTION : BasicMovingCharacter_StopAction()}
screen2.add_active_game_object(hero3)

GameScreenFactory.add_game_screen("basic2", screen2)


#GameScreenFactory.gameScreens = {"basic" : GAME_SCREEN_DIRECTORY + "basic", "basic2" : GAME_SCREEN_DIRECTORY + "basic2"}
#MainMenuHelper.get_saved_games("../GameImpl/Properties/properties.xml")


game = Game() 
MainMenuHelper.new_game(game, "../GameImpl/Properties/")
#MainMenuHelper.load_game(game, "../GameImpl/Save/2014-03-02_16-46-00/")
game.start_game()


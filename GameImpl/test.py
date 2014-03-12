import sys, pygame
from GameEngine import *
from time import sleep

"""
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
"""




screen = Screen(300,300)
screen.prepare()
tiledScreen = TiledSpace(250, 250)
tiledScreen.is_main_tile = True
tiledScreen.tiles_from_x_y_coords([50,100, 150, 200], [125])


tiledSurface2 = TiledSpace(50,125)
tiledSurface2.tiles_from_x_y_coords([], [62.5])

tiledSurface3 = TiledSpace(50, 62.5)
tiledSurface3.tiles_from_x_y_coords([25], [31.25])
tiledSurface3.showNums = True
#tiledSurface3.add_tile(1, Button())

tiledSurface2.add_tile(1, tiledSurface3)

tiledScreen.add_tile(8, tiledSurface2)
tiledScreen.showBorders = True
tiledScreen.showNums = True
tiledScreen.show_tile(screen.surface)

i = 0

while True:
    Mouse.update_state()

#tiledScreen.hide_tile()

#sleep(3)
#tiledScreen.hide_tile(screen.surface)
pygame.display.update()
while True :
    pass


screen.clear_screen()



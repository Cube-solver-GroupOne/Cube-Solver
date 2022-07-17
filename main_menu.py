from cube_steps_3D.main import *
from cube_steps_3D.play_3d_cube import *
from cube_steps_3D.color_detect import *

# Class of game menu
class MenuMenu(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=camera.ui, ignore_paused=True)
        window.fullscreen = True

        # Create empty entities that will be parents of our menus content
        self.main_menu = Entity(parent=self, enabled=True, position=(0, -0.25), color=color.blue, )
        self.options_menu = Entity(parent=self, enabled=False, position=(0, -0.25), color=color.blue)
        self.help_menu = Entity(parent=self, enabled=False, position=(0, -0.25), color=color.blue)

        # Add a background. You can change 'shore' to a different texture of you'd like.
        self.background = Sprite('assessts/rubiks-share-img.png', z=1, scale=1.5)

        # [MAIN MENU] WINDOW START
        # Title of our menu
        Text("MAIN MENU", parent=self.main_menu, y=0.4, x=0, origin=(0, 0), position=(0, 0.05))

        def switch(menu1, menu2):
            menu1.enable()
            menu2.disable()

        # Button list
        ButtonList(button_dict={
            "Start": Func(self.buld_3D_play),
            "Solver": Func(self.dedectoin),
            "Options": Func(lambda: switch(self.options_menu, self.main_menu)),
            "Help": Func(lambda: Text("""This game is a smart Rubik's Cube game 
If you want tp play and solve 3D cube click on START
If you want to use our BOT to solve a real cube for you click on SOLVER
              """,origin=(0,0), position=(-0.15, 0.23))),
            "Exit": Func(lambda: application.quit())
        }, color=color.blue, y=0, parent=self.main_menu,text_size=5)
        # [MAIN MENU] WINDOW END

        # [OPTIONS MENU] WINDOW START
        # Title of our menu
        Text("OPTIONS MENU", parent=self.options_menu, y=0.4, x=0, origin=(0, 0), position=(0, 0.05))

        # Button
        Button("Back", parent=self.options_menu, y=-0.3, scale=(0.1, 0.05), color=color.blue, origin=(0, 0),
               position=(0, -0.1),
               on_click=lambda: switch(self.main_menu, self.options_menu))

        # [OPTIONS MENU] WINDOW END

        # [HELP MENU] WINDOW START
        # Title of our menu
        Text("HELP MENU", parent=self.help_menu, y=0.4, x=0, origin=(0, 0), position=(0, 0.05))

        # Button list
        # ButtonList(button_dict={
        #     "Gameplay": Func(print_on_screen, "You clicked on Gameplay help button!", position=(0, -.16),
        #                      origin=(0, 0)),
        #     "Battle": Func(print_on_screen, "You clicked on Battle help button!", position=(0, -.16), origin=(0, 0)),
        #     "Control": Func(print_on_screen, "You clicked on Control help button!", position=(0, -.16), origin=(0, 0)),
        #     "Back": Func(lambda: switch(self.main_menu, self.help_menu))
        # }, color=color.blue, y=0, parent=self.help_menu)
        # [HELP MENU] WINDOW END

        # Here we can change attributes of this class when call this class
        for key, value in kwargs.items():
            setattr(self, key, value)

    # Input function that check if key pressed on keyboard
    def input(self, key):
        # And if you want use same keys on different windows
        # Like [Escape] or [Enter] or [Arrows]
        # Just write like that:

        # If our main menu enabled and we press [Escape]
        if self.main_menu.enabled and key == "escape":
            application.quit()
        elif self.options_menu.enabled and key == "escape":
            self.main_menu.enable()
            self.options_menu.disable()
        elif self.help_menu.enabled and key == "escape":
            self.main_menu.enable()
            self.help_menu.disable()

    # Update function that check something every frame
    # You can use it similar to input with checking
    # what menu is currently enabled
    def update(self):
        pass

    def buld_3D_steps(self):
        self.main_menu.disable()
        self.background.disable()
        game = Game()

    def buld_3D_play(self):
        self.main_menu.disable()
        self.background.disable()
        game = Game3D()

if __name__ == "__main__":
    # Init application
    app = Ursina(title='Main Menu Tutorial')

    # Call our menu
    main_menu = MenuMenu()
    # Run application
    app.run()

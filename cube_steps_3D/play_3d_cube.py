from ursina import *
from main_menu import *

class Game3D:
    def __init__(self):
        super().__init__()
        window.fullscreen = True
        Entity(model='quad', scale=60, texture='white_cube', texture_scale=(60, 60), rotation_x=90, y=-5,
               color=color.light_gray)  # plane
        Entity(model='sphere', scale=100, texture='textures/sky0', double_sided=True)  # sky
        EditorCamera()
        camera.world_position = (0, 0, -15)
        self.model, self.texture = 'models/custom_cube', 'textures/rubik_texture'
        self.load_game()

    def load_game(self):
        self.create_cube_positions()
        self.CUBES = [Entity(model=self.model, texture=self.texture, position=pos) for pos in self.SIDE_POSITIONS]
        self.PARENT = Entity()
        self.rotation_axes = {'LEFT': 'x', 'RIGHT': 'x', 'TOP': 'y', 'BOTTOM': 'y', 'FACE': 'z', 'BACK': 'z'}
        self.cubes_side_positons = {'LEFT': self.LEFT, 'BOTTOM': self.BOTTOM, 'RIGHT': self.RIGHT, 'FACE': self.FACE,
                                    'BACK': self.BACK, 'TOP': self.TOP}
        self.animation_time = 0.5
        Ursina.action_trigger = True
        self.action_mode = True
        self.message = Text(origin=(0, 19), color=color.black)
        self.create_sensors()
        self.random_state(rotations=8)  # initial state of the cube, rotations - number of side turns

        u = Button(icon='models/8i7FQ(1)', color=color.black, scale_x=.15, scale_y=0.22)
        u.world_position = (-12, -7, -15)
        u.on_click = self.U_move

        r = Button(icon='models/8i7FQ(2)', color=color.black, scale_x=.15, scale_y=0.22)
        r.world_position = (-7.5, -7, -15)
        r.on_click = self.R_move

        l = Button(icon='models/8i7FQ(3)', color=color.black, scale_x=.15, scale_y=0.22)
        l.world_position = (-3, -7, -15)
        l.on_click = self.L_move

        f = Button(icon='models/8i7FQ(4)', color=color.black, scale_x=.15, scale_y=0.22)
        f.world_position = (1.5, -7, -15)
        f.on_click = self.F_move

        b = Button(icon='models/8i7FQ(5)', color=color.black, scale_x=.15, scale_y=0.22)
        b.world_position = (5.5, -7, -15)
        b.on_click = self.B_move

        t = Button(icon='models/8i7FQ(6)', color=color.black, scale_x=.15, scale_y=0.22)
        t.world_position = (10, -7, -15)
        t.on_click = self.T_move

        bb = Button(icon= "", color=color.black, scale_x=.15, scale_y=0.22)
        bb.world_position = (14, -7, -15)
        bb.on_click = self.bbbb

    def U_move(self):
        self.rotate_side('TOP')

    def R_move(self):
        self.rotate_side('RIGHT')

    def L_move(self):
        self.rotate_side('LEFT')

    def F_move(self):
        self.rotate_side('FACE')

    def B_move(self):
        self.rotate_side('BACK')

    def T_move(self):
        self.rotate_side('BOTTOM')

    def random_state(self, rotations=3):
        [self.rotate_side_without_animation(random.choice(list(self.rotation_axes))) for i in range(rotations)]

    def rotate_side_without_animation(self, side_name):
        cube_positions = self.cubes_side_positons[side_name]
        rotation_axis = self.rotation_axes[side_name]
        self.reparent_to_scene()
        for cube in self.CUBES:
            if cube.position in cube_positions:
                cube.parent = self.PARENT
                exec(f'self.PARENT.rotation_{rotation_axis} = 90')

    def create_sensors(self):
        '''detectors for each side, for detecting collisions with mouse clicks'''
        create_sensor = lambda name, pos, scale: Entity(name=name, position=pos, model='cube', color=color.dark_gray,
                                                        scale=scale, collider='box', visible=False)
        self.LEFT_sensor = create_sensor(name='LEFT', pos=(-0.99, 0, 0), scale=(1.01, 3.01, 3.01))
        self.FACE_sensor = create_sensor(name='FACE', pos=(0, 0, -0.99), scale=(3.01, 3.01, 1.01))
        self.BACK_sensor = create_sensor(name='BACK', pos=(0, 0, 0.99), scale=(3.01, 3.01, 1.01))
        self.RIGHT_sensor = create_sensor(name='RIGHT', pos=(0.99, 0, 0), scale=(1.01, 3.01, 3.01))
        self.TOP_sensor = create_sensor(name='TOP', pos=(0, 1, 0), scale=(3.01, 1.01, 3.01))
        self.BOTTOM_sensor = create_sensor(name='BOTTOM', pos=(0, -1, 0), scale=(3.01, 1.01, 3.01))



    def toggle_animation_trigger(self):
        '''prohibiting side rotation during rotation animation'''
        Ursina.action_trigger = not Ursina.action_trigger

    def rotate_side(self, side_name):
        Ursina.action_trigger = False
        cube_positions = self.cubes_side_positons[side_name]
        rotation_axis = self.rotation_axes[side_name]
        self.reparent_to_scene()
        for cube in self.CUBES:
            if cube.position in cube_positions:
                cube.parent = self.PARENT
                eval(f'self.PARENT.animate_rotation_{rotation_axis}(90, duration=self.animation_time)')
        invoke(self.toggle_animation_trigger, delay=self.animation_time + 0.11)

    def reparent_to_scene(self):
        for cube in self.CUBES:
            if cube.parent == self.PARENT:
                world_pos, world_rot = round(cube.world_position, 1), cube.world_rotation
                cube.parent = scene
                cube.position, cube.rotation = world_pos, world_rot
        self.PARENT.rotation = 0

    def create_cube_positions(self):
        self.LEFT = {Vec3(-1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.BOTTOM = {Vec3(x, -1, z) for x in range(-1, 2) for z in range(-1, 2)}
        self.FACE = {Vec3(x, y, -1) for x in range(-1, 2) for y in range(-1, 2)}
        self.BACK = {Vec3(x, y, 1) for x in range(-1, 2) for y in range(-1, 2)}
        self.RIGHT = {Vec3(1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.TOP = {Vec3(x, 1, z) for x in range(-1, 2) for z in range(-1, 2)}
        self.SIDE_POSITIONS = self.LEFT | self.BOTTOM | self.FACE | self.BACK | self.RIGHT | self.TOP
    #
    # def bbbb(self):
    #     main_menu = MenuMenu()



if __name__ == '__main__':
    game = Game3D()
    game.run()

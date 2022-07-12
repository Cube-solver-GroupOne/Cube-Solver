from ursina import *


class Game:
    def __init__(self):
        super().__init__()

        Entity(model='quad', scale=60, texture='white_cube', texture_scale=(60, 60), rotation_x=90, y=-5,
               color=color.light_gray)  # plane
        Entity(model='sphere', scale=100, texture='textures/sky0', double_sided=True)  # sky
        EditorCamera()
        camera.world_position = (-5, 7, -20)
        camera.rotation_x = (15)
        camera.rotation_y = (15)
        self.model, self.texture = 'models/custom_cube', 'textures/rubik_texture'
        self.load_game()

    def load_game(self):
        self.create_cube_positions()
        self.CUBES = [Entity(model=self.model, texture=self.texture, position=pos) for pos in self.SIDE_POSITIONS]
        self.PARENT = Entity()
        self.rotation_axes = {'LEFT': 'x', 'LEFTS': 'x', 'RIGHT': 'x', 'RIGHTS': 'x', 'TOP': 'y', 'TOPS': 'y',
                              'BOTTOM': 'y', 'BOTTOMS': 'y', 'FACE': 'z', 'FACES': 'z',
                              'BACK': 'z', 'BACKS': 'z'}
        self.cubes_side_positons = {'LEFT': self.LEFT, 'LEFTS': self.LEFT, 'BOTTOM': self.BOTTOM,
                                    'BOTTOMS': self.BOTTOM, 'RIGHT': self.RIGHT, 'RIGHTS': self.RIGHT,
                                    'FACE': self.FACE, 'FACES': self.FACE,
                                    'BACK': self.BACK, 'BACKS': self.BACK, 'TOP': self.TOP, 'TOPS': self.TOP}

        self.animation_time = 0.5
        self.action_trigger = True
        self.action_mode = True
        self.message = Text(origin=(0, 19), color=color.black)
        self.create_sensors()
        self.random_state(rotations=0)  # initial state of the cube, rotations - number of side turns
        b = Button(text='Next Move', color=color.black, scale_x=.15, scale_y=0.07, text_origin=(0, 0))
        b.world_position = (-12, -8, -15)

        b.on_click = self.Buttonss
    def Buttonss(self):
        self.rotate_side('LEFT')

    def random_state(self, rotations=3):
        [self.rotate_side_without_animation(random.choice(list(self.rotation_axes))) for i in range(rotations)]

    def my_random_state(self):
        ss = ["BACKS"]
        for x in ss:
            self.rotate_side(x)

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
        self.action_trigger = not self.action_trigger

    def rotate_side(self, side_name):
        self.action_trigger = False
        cube_positions = self.cubes_side_positons[side_name]
        rotation_axis = self.rotation_axes[side_name]

        if str(side_name[-1]) == "S":
            dgree = "-90"
        else:
            dgree = "90"

        self.reparent_to_scene()
        for cube in self.CUBES:
            if cube.position in cube_positions:
                cube.parent = self.PARENT
                eval(f'self.PARENT.animate_rotation_{rotation_axis}({dgree}, duration=self.animation_time)')
        invoke(self.toggle_animation_trigger, delay=self.animation_time + .11)

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



if __name__ == '__main__':
    game = Game()


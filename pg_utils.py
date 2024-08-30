import math, time, random, pygame

RESOLUTION = (2560, 1440)
WIDTH, HEIGHT = RESOLUTION
FPS = 165
FULLSCREEN = True
WINDOW_NAME = "PyGame Window"
ICON_LOCATION = ""


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        output = func(*args, **kwargs)
        end = time.time()

        print(f"Function {func.__name__} took {(end-start)*1000:.2f} ms to execute.")
        return output

    return wrapper


def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))


def lerp(start, end, t):
    return start + t * (end - start)


def map_value(value, start1, stop1, start2, stop2):
    return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1))


def manage_frame_rate(clock, get_ticks_last_frame):
    clock.tick(FPS)
    t = pygame.time.get_ticks()
    delta_time = (t - get_ticks_last_frame) / 1000.0
    return t, delta_time


def draw_circle(screen, color, position, radius):
    pygame.draw.circle(
        screen, color.get_tup(), (int(position.x), int(position.y)), radius
    )


def draw_rectangle(screen, color, position, size):
    pygame.draw.rect(
        screen, color.get_tup(), pygame.Rect(position.x, position.y, size.x, size.y)
    )


def draw_line(screen, color, start_pos, end_pos, width=1):
    pygame.draw.line(
        screen,
        color.get_tup(),
        (int(start_pos.x), int(start_pos.y)),
        (int(end_pos.x), int(end_pos.y)),
        width,
    )


class Text:
    def __init__(
        self,
        text,
        font,
        color,
        position,
        anti_aliasing=True,
        background=False,
        bg_color=(0, 0, 0),
    ):
        """The Text class does not accept vectors or color objects as args"""

        self.text = text
        self.font = font
        self.color = color
        self.position = position
        self.anti_aliasing = anti_aliasing
        self.background = background
        self.bg_color = bg_color

        self.center = 0
        self.bottom = 1
        self.bottom_left = 2
        self.bottom_right = 3
        self.mid_bottom = 4
        self.mid_left = 5
        self.mid_right = 6
        self.mid_top = 7
        self.top = 8
        self.top_left = 9
        self.top_right = 10
        self.left = 11
        self.right = 12

    def draw(self, surface, anchor=None):
        if anchor == None:
            anchor = self.center

        if not self.background:
            self.text = self.font.render(self.text, self.anti_aliasing, self.color)
        elif self.background:
            self.text = self.font.render(
                self.text, self.anti_aliasing, self.color, self.bg_color
            )

        self.text_rect = self.text.get_rect()

        if anchor == self.center:
            self.text_rect.center = (self.position[0], self.position[1])
        if anchor == self.bottom:
            self.text_rect.bottom = (self.position[0], self.position[1])
        if anchor == self.bottom_left:
            self.text_rect.bottomleft = (self.position[0], self.position[1])
        if anchor == self.bottom_right:
            self.text_rect.bottomright = (self.position[0], self.position[1])
        if anchor == self.mid_bottom:
            self.text_rect.midbottom = (self.position[0], self.position[1])
        if anchor == self.mid_left:
            self.text_rect.midleft = (self.position[0], self.position[1])
        if anchor == self.mid_right:
            self.text_rect.midright = (self.position[0], self.position[1])
        if anchor == self.mid_top:
            self.text_rect.midtop = (self.position[0], self.position[1])
        if anchor == self.top:
            self.text_rect.top = (self.position[0], self.position[1])
        if anchor == self.top_left:
            self.text_rect.topleft = (self.position[0], self.position[1])
        if anchor == self.top_right:
            self.text_rect.topright = (self.position[0], self.position[1])
        if anchor == self.left:
            self.text_rect.left = (self.position[0], self.position[1])
        if anchor == self.right:
            self.text_rect.right = (self.position[0], self.position[1])

        surface.blit(self.text, self.text_rect)


class Color:
    def __init__(self, r=255, g=255, b=255):
        self.r, self.g, self.b = r, g, b

    def init_colors(self):
        self.BLACK = Color(0, 0, 0)
        self.DARK_GRAY = Color(85, 85, 85)
        self.LIGHT_GRAY = Color(170, 170, 170)
        self.WHITE = Color(255, 255, 255)
        self.RED = Color(255, 0, 0)
        self.LIME = Color(0, 255, 0)
        self.BLUE = Color(0, 0, 255)
        self.YELLOW = Color(255, 255, 0)
        self.PINK = Color(255, 0, 255)
        self.LIGHT_BLUE = Color(0, 255, 255)
        self.GREEN = Color(0, 128, 0)
        self.PURPLE = Color(128, 0, 128)
        self.DARK_BLUE = Color(0, 0, 128)
        self.ORANGE = Color(255, 170, 0)
        self.BROWN = Color(128, 60, 0)

    @staticmethod
    def random():
        return Color(
            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        )

    def blend(self, other, ratio=0.5):
        r = int(self.r * ratio + other.r * (1 - ratio))
        g = int(self.g * ratio + other.g * (1 - ratio))
        b = int(self.b * ratio + other.b * (1 - ratio))
        return Color(r, g, b)

    def to_hex(self, prefix="#"):
        return f"{prefix}{self.r:02x}{self.g:02x}{self.b:02x}"

    def to_hsl(self, hue_angle=True):
        r, g, b = self.r / 255, self.g / 255, self.b / 255
        max_color = max(r, g, b)
        min_color = min(r, g, b)
        l = (max_color + min_color) / 2

        if max_color == min_color:
            h = s = 0
        else:
            diff = max_color - min_color
            s = (
                diff / (2 - max_color - min_color)
                if l > 0.5
                else diff / (max_color + min_color)
            )
            if max_color == r:
                h = (g - b) / diff + (6 if g < b else 0)
            elif max_color == g:
                h = (b - r) / diff + 2
            else:
                h = (r - g) / diff + 4
            h /= 6

        return (h * 360 if hue_angle else h, s, l)

    def get_tup(self):
        return self.r, self.g, self.b

    def __repr__(self) -> str:
        return f"R: {self.r}, G: {self.g}, B: {self.b}"


class Vector2:
    def __init__(self, x=0, y=0):
        self.x, self.y = x, y

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        mag = self.magnitude()
        try:
            return Vector2(self.x / mag, self.y / mag)
        except ZeroDivisionError:
            return Vector2()

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def angle_between(self, other):
        return math.acos(self.dot(other) / (self.magnitude() * other.magnitude()))

    def rotate(self, angle):
        rad = math.radians(angle)
        cos_theta, sin_theta = math.cos(rad), math.sin(rad)
        return Vector2(
            self.x * cos_theta - self.y * sin_theta,
            self.x * sin_theta + self.y * cos_theta,
        )

    def scale(self, factor):
        return Vector2(self.x * factor, self.y * factor)

    def translate(self, dx, dy):
        return Vector2(self.x + dx, self.y + dy)

    def get_tup(self):
        return self.x, self.y, self.z

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector2(self.x * other, self.y * other)
        raise TypeError(
            "Unsupported operand type(s) for *: 'Vector2' and '{}'".format(type(other))
        )

    def __div__(self, other):
        if isinstance(other, (int, float)):
            return Vector2(self.x / other, self.y / other)
        raise TypeError(
            "Unsupported operand type(s) for /: 'Vector2' and '{}'".format(type(other))
        )

    def __repr__(self) -> str:
        return f"X: {self.x}, Y: {self.y}"

    def init_vectors(self):
        self.ZERO = Vector2(0, 0)
        self.ONE = Vector2(1, 1)
        self.NEG_ONE = Vector2(-1, -1)
        self.UP = Vector2(0, 1)
        self.DOWN = Vector2(0, -1)
        self.LEFT = Vector2(-1, 0)
        self.RIGHT = Vector2(1, 0)


class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self):
        mag = self.magnitude()
        try:
            return Vector3(self.x / mag, self.y / mag, self.z / mag)
        except:
            return Vector3()

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def angle_between(self, other):
        return math.acos(self.dot(other) / (self.magnitude() * other.magnitude()))

    def rotate(self, angle, axis):
        rad = math.radians(angle)
        cos_theta, sin_theta = math.cos(rad), math.sin(rad)
        cross_prod = self.cross(axis)
        dot_prod = self.dot(axis)
        return (
            self.scale(cos_theta)
            + cross_prod.scale(sin_theta)
            + axis.scale(dot_prod * (1 - cos_theta))
        )

    def scale(self, factor):
        return Vector3(self.x * factor, self.y * factor, self.z * factor)

    def translate(self, dx, dy, dz):
        return Vector3(self.x + dx, self.y + dy, self.z + dz)

    def get_tup(self):
        return self.x, self.y, self.z

    def __add__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        raise TypeError(
            "Unsupported operand type(s) for +: 'Vector3' and '{}'".format(type(other))
        )

    def __sub__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
        raise TypeError(
            "Unsupported operand type(s) for -: 'Vector3' and '{}'".format(type(other))
        )

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector3(self.x * other, self.y * other, self.z * other)
        elif isinstance(other, Vector3):
            return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)
        raise TypeError(
            "Unsupported operand type(s) for *: 'Vector3' and '{}'".format(type(other))
        )

    def __div__(self, other):
        if isinstance(other, (int, float)):
            return Vector3(self.x / other, self.y / other, self.z / other)
        elif isinstance(other, Vector3):
            return Vector3(self.x / other.x, self.y / other.y, self.z / other.z)
        raise TypeError(
            "Unsupported operand type(s) for /: 'Vector3' and '{}'".format(type(other))
        )

    def __repr__(self) -> str:
        return f"X: {self.x}, Y: {self.y}, Z: {self.z}"

    def init_vectors(self):
        self.ZERO = Vector2(0, 0)
        self.ONE = Vector2(1, 1)
        self.NEG_ONE = Vector2(-1, -1)
        self.UP = Vector2(0, 1)
        self.DOWN = Vector2(0, -1)
        self.LEFT = Vector2(-1, 0)
        self.RIGHT = Vector2(1, 0)

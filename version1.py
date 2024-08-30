import pygame
from pg_utils import *

# Vector2 Setup
vector2 = Vector2()
vector2.init_vectors()

# Vector3 Setup
vector3 = Vector3()
vector3.init_vectors()

# Colors Setup
colors = Color()
colors.init_colors()

# PyGame Setup
pygame.init()

SCREEN = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN if FULLSCREEN else 0)
pygame.display.set_caption(WINDOW_NAME)
# pygame.display.set_icon(pygame.image.load(ICON_LOCATION))  # Uncomment if you have an icon

clock = pygame.time.Clock()
delta_time = 0.0

gravity = vector2.DOWN * 500
UI_HEIGHT = 100
boundary_width, boundary_height = 1600, 900


class Molecule:
    def __init__(
        self,
        position: Vector2 = vector2.ZERO,
        velocity: Vector2 = vector2.ZERO,
        radius: int = 10,
        mass: float = 1,
        color: Color = colors.WHITE,
        viscosity: float = 1,
    ):
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.mass = mass

        self.color = color

        self.effect_radius = 3

        self.viscosity = viscosity

    def update_velocity(self, molecules: list):
        for i in range(len(molecules)):
            # Just for quick access
            other = molecules[i]

            if other == self:
                continue

            # Skip iteration if particle is too far
            if (
                other.position - self.position
            ).magnitude() > self.radius * self.effect_radius:
                continue
            else:
                # Increase velocity in opposite direction from other
                self.velocity += (
                    (other.position - self.position).normalize()
                    * (other.position - self.position).magnitude()
                    * delta_time
                    * 100
                )

                # Just so the particles dont stick to the walls too much
                if self.position.x <= -(boundary_width // 2) + (self.radius * 2):
                    self.velocity.x += delta_time * 1000
                if self.position.x >= (boundary_width // 2) - (self.radius * 2):
                    self.velocity.x -= delta_time * 1000

                if self.position.y <= -(boundary_height // 2) + (self.radius * 2):
                    self.velocity.y -= delta_time * 1000
                if self.position.y >= (boundary_height // 2) - (self.radius * 2):
                    self.velocity.y += delta_time * 1000

        # Add gravity
        self.velocity += gravity * delta_time

    def update_position(self, molecules):
        # Update position with velocity
        self.position += self.velocity * delta_time

        position_temp = self.position

        # Clamp position so it doesnt escape the boundary
        self.position.x = clamp(
            self.position.x, -(boundary_width / 2), boundary_width / 2
        )

        self.position.y = clamp(
            self.position.y,
            -(boundary_height / 2),
            boundary_height / 2,
        )

        if self.position.x != position_temp.x:
            self.velocity.x = 0

        if self.position.x != position_temp.x:
            self.velocity.y = 0

        # Makes the particles not have the same position
        for other in molecules:
            if (
                other.position.x == self.position.x
                and other.position.y == self.position.y
                and other != self
            ):
                x = random.random()
                x = x * 2 - 1

                y = random.random()
                y = y * 2 - 1

                vector = Vector2(x, y).normalize() * self.radius
                self.position += vector

    def draw(self):
        screen_pos = (
            self.position.x + WIDTH // 2,
            -self.position.y + HEIGHT // 2 + UI_HEIGHT // 2,
        )

        pygame.draw.circle(SCREEN, self.color.get_tup(), screen_pos, self.radius)


def fluid_sim(molecules):
    for i in range(len(molecules)):
        molecules[i].update_velocity(molecules)

    for i in range(len(molecules)):
        molecules[i].update_position(molecules)

    for i in range(len(molecules)):
        molecules[i].draw()

    pygame.draw.rect(
        SCREEN,
        colors.LIME.get_tup(),
        pygame.Rect(
            (WIDTH - boundary_width) / 2,
            (HEIGHT + UI_HEIGHT - boundary_height) / 2,
            boundary_width,
            boundary_height,
        ),
        1,
    )


def setup(x, y, radius, spacing, offset_x, offset_y):
    molecules = []

    colors_choises = [colors.WHITE, colors.LIGHT_BLUE, colors.BLUE]

    for i in range(x):
        for j in range(y):
            m = Molecule(
                Vector2(
                    i * radius + spacing * i + offset_x - (x**2 - x),
                    j * radius + spacing * j + offset_y - (y**2 - y),
                ),
                radius=radius,
                color=random.choice(colors_choises),
            )
            molecules.append(m)

    return molecules


def main():
    global delta_time

    running = True
    get_ticks_last_frame = 0.0

    molecules = setup(10, 10, 10, 5, 0, 0)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        SCREEN.fill(colors.BLACK.get_tup())

        fluid_sim(molecules)

        pygame.display.flip()

        get_ticks_last_frame, delta_time = manage_frame_rate(
            clock, get_ticks_last_frame
        )

    pygame.quit()


if __name__ == "__main__":
    main()

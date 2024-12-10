import pygame
import math
import random

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sphere Survival")

# Colors
WHITE = (255, 255, 255)
BACKGROUND_COLOR = (10, 10, 30)
LIGHTNING_COLOR = (255, 255, 0)

# Sphere properties
sphere_radius = 50
num_points = 100
sphere_position_x, sphere_position_y = WIDTH // 2, HEIGHT // 2  # Initial position
movement_speed = 5
lightning_list = []
sphere_color = WHITE  # Initial sphere color

# Game settings
frame_count = 0
score = 0
health = 3
level = 1

# Sound effects
pygame.mixer.init()
lightning_sound = pygame.mixer.Sound("lightning bolt 1.wav")

# Generate random points on the sphere's surface
def generate_sphere_points(num_points, radius):
    points = []
    for _ in range(num_points):
        theta = random.uniform(0, 2 * math.pi)
        phi = random.uniform(0, math.pi)
        x = radius * math.sin(phi) * math.cos(theta)
        y = radius * math.sin(phi) * math.sin(theta)
        z = radius * math.cos(phi)
        points.append([x, y, z])
    return points

# Rotate points around x, y, and z axes
def rotate_point(point, angle_x, angle_y, angle_z):
    x, y, z = point

    # Rotation around X-axis
    cos_x, sin_x = math.cos(angle_x), math.sin(angle_x)
    y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x

    # Rotation around Y-axis
    cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
    x, z = x * cos_y + z * sin_y, -x * sin_y + z * cos_y

    # Rotation around Z-axis
    cos_z, sin_z = math.cos(angle_z), math.sin(angle_z)
    x, y = x * cos_z - y * sin_z, x * sin_z + y * cos_z

    return [x, y, z]

# Project 3D point to 2D
def project_point(point, screen_x, screen_y):
    x, y, z = point
    fov = 300
    distance = fov + z
    projected_x = int(screen_x + x * fov / distance)
    projected_y = int(screen_y + y * fov / distance)
    return projected_x, projected_y

# Start screen function
def start_screen():
    screen.fill(BACKGROUND_COLOR)
    font = pygame.font.SysFont(None, 72)
    title_text = font.render("Sphere Survival", True, WHITE)
    instructions_font = pygame.font.SysFont(None, 36)
    instructions_text = instructions_font.render("Press SPACE to Start", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - 200, HEIGHT // 2 - 100))
    screen.blit(instructions_text, (WIDTH // 2 - 150, HEIGHT // 2 + 50))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

# Game over screen function
def game_over_screen(final_score):
    screen.fill(BACKGROUND_COLOR)
    game_over_font = pygame.font.SysFont(None, 72)
    game_over_text = game_over_font.render("Game Over", True, WHITE)
    final_score_font = pygame.font.SysFont(None, 36)
    final_score_text = final_score_font.render(f"Final Score: {final_score}", True, WHITE)
    restart_text = final_score_font.render("Press R to Restart or Q to Quit", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 100))
    screen.blit(final_score_text, (WIDTH // 2 - 100, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - 200, HEIGHT // 2 + 100))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()  # Restart the game
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()

# Main game function
def main():
    global frame_count, lightning_list, score, health, level, sphere_position_x, sphere_position_y, sphere_color
    points = generate_sphere_points(num_points, sphere_radius)
    angle_x, angle_y, angle_z = 0, 0, 0
    running = True
    clock = pygame.time.Clock()

    # Start Screen
    start_screen()

    while running:
        screen.fill(BACKGROUND_COLOR)
        frame_count += 1

        # Increase difficulty and change color every level
        if frame_count % (10 * 60) == 0:  # Every 10 seconds
            level += 1
            health += 1
            sphere_color = [random.randint(50, 255) for _ in range(3)]  # Randomize sphere color
            for lightning in lightning_list:
                lightning['speed'] += 1

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player controls (move sphere and rotate it)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            sphere_position_y -= movement_speed
            angle_x += 0.05
        if keys[pygame.K_DOWN]:
            sphere_position_y += movement_speed
            angle_x -= 0.05
        if keys[pygame.K_LEFT]:
            sphere_position_x -= movement_speed
            angle_y += 0.05
        if keys[pygame.K_RIGHT]:
            sphere_position_x += movement_speed
            angle_y -= 0.05

        # Keep sphere within screen bounds
        sphere_position_x = max(sphere_radius, min(WIDTH - sphere_radius, sphere_position_x))
        sphere_position_y = max(sphere_radius, min(HEIGHT - sphere_radius, sphere_position_y))

        # Rotate and draw sphere points
        for point in points:
            rotated_point = rotate_point(point, angle_x, angle_y, angle_z)
            projected_x, projected_y = project_point(rotated_point, sphere_position_x, sphere_position_y)
            pygame.draw.circle(screen, sphere_color, (projected_x, projected_y), 2)

        # Spawn lightning strikes
        if frame_count % 60 == 0:  # Every second
            lightning_y = random.randint(0, HEIGHT)
            lightning_list.append({'x': WIDTH, 'y': lightning_y, 'speed': 3 + level})

        # Update and draw lightning
        for lightning in lightning_list[:]:
            lightning['x'] -= lightning['speed']
            pygame.draw.line(screen, LIGHTNING_COLOR, (lightning['x'], lightning['y']),
                             (lightning['x'] + 20, lightning['y']), 2)

            # Collision detection (check sphere bounds)
            if abs(lightning['x'] - sphere_position_x) < sphere_radius and abs(
                    lightning['y'] - sphere_position_y) < sphere_radius:
                health -= 1
                lightning_list.remove(lightning)
                if health <= 0:
                    running = False

            # Remove off-screen lightning
            if lightning['x'] < -20:
                lightning_list.remove(lightning)
                score += 1
                lightning_sound.play()  # Play sound when lightning passes through sphere

        # Display stats
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        health_text = font.render(f"Health: {health}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(health_text, (10, 50))
        screen.blit(level_text, (10, 90))

        # Update display
        pygame.display.flip()
        clock.tick(60)

    # Game over screen
    game_over_screen(score)

# Run the game
main()
pygame.quit()

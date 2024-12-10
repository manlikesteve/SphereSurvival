import pygame
import math
import random

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Rotating Bouncing Sphere")

# Colors
WHITE = (255, 255, 255)
BACKGROUND_COLOR = (10, 10, 30)

# Sphere properties
sphere_radius = 100
num_points = 200  # Number of points on the sphere's surface
points = []  # To store 3D points on the sphere

# Sphere rotation
angle_x, angle_y, angle_z = 0, 0, 0
rotation_speed = 0.02

# Sphere position and velocity for bouncing
sphere_x, sphere_y, sphere_z = WIDTH // 2, HEIGHT // 2, 0
velocity_x, velocity_y = 3, 2

# Generate random points on the surface of a 3D sphere
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
    fov = 300  # Field of view (larger value gives more perspective)
    distance = fov + z
    projected_x = int(screen_x + x * fov / distance)
    projected_y = int(screen_y + y * fov / distance)
    return projected_x, projected_y

# Initialize points on the sphere
points = generate_sphere_points(num_points, sphere_radius)

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Adjust rotation speed with arrow keys
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                rotation_speed += 0.01
            elif event.key == pygame.K_DOWN:
                rotation_speed = max(0.01, rotation_speed - 0.01)

    # Update sphere position for bouncing
    sphere_x += velocity_x
    sphere_y += velocity_y

    # Bounce within screen bounds
    if sphere_x - sphere_radius < 0 or sphere_x + sphere_radius > WIDTH:
        velocity_x = -velocity_x
    if sphere_y - sphere_radius < 0 or sphere_y + sphere_radius > HEIGHT:
        velocity_y = -velocity_y

    # Update rotation angles
    angle_x += rotation_speed
    angle_y += rotation_speed / 2
    angle_z += rotation_speed / 3

    # Clear screen
    screen.fill(BACKGROUND_COLOR)

    # Draw each point on the sphere
    for point in points:
        # Rotate the point in 3D
        rotated_point = rotate_point(point, angle_x, angle_y, angle_z)

        # Project the rotated 3D point to 2D
        projected_x, projected_y = project_point(rotated_point, sphere_x, sphere_y)

        # Calculate distance-based shading for depth
        shade = int(255 * (0.5 + rotated_point[2] / (2 * sphere_radius)))
        color = (shade, shade, 255)  # Blueish color with depth effect

        # Draw the point
        pygame.draw.circle(screen, color, (projected_x, projected_y), 3)

    # Update display and control frame rate
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
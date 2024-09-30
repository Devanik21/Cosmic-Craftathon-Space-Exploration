import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 50
ASTEROID_WIDTH, ASTEROID_HEIGHT = 40, 40
FUEL_WIDTH, FUEL_HEIGHT = 30, 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cosmic Craftathon - Space Exploration")

# Load images
spaceship_img = pygame.image.load("C:\\Users\\debna\\OneDrive\\Desktop\\spaceship.png")
spaceship_img = pygame.transform.scale(spaceship_img, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

asteroid_img = pygame.image.load("C:\\Users\\debna\\OneDrive\\Desktop\\asteroid.png")
asteroid_img = pygame.transform.scale(asteroid_img, (ASTEROID_WIDTH, ASTEROID_HEIGHT))

fuel_img = pygame.image.load("C:\\Users\\debna\\OneDrive\\Desktop\\fuel.png")
fuel_img = pygame.transform.scale(fuel_img, (FUEL_WIDTH, FUEL_HEIGHT))

# Clock
clock = pygame.time.Clock()

# Spaceship class
class Spaceship:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 100
        self.speed = 5
        self.fuel = 100
        self.score = 0

    def draw(self):
        screen.blit(spaceship_img, (self.x, self.y))

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x - self.speed > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x + self.speed + SPACESHIP_WIDTH < WIDTH:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y - self.speed > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y + self.speed + SPACESHIP_HEIGHT < HEIGHT:
            self.y += self.speed

# Asteroid class
class Asteroid:
    def __init__(self):
        self.x = random.randint(0, WIDTH - ASTEROID_WIDTH)
        self.y = random.randint(-100, -ASTEROID_HEIGHT)
        self.speed = random.randint(2, 6)

    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = random.randint(-100, -ASTEROID_HEIGHT)
            self.x = random.randint(0, WIDTH - ASTEROID_WIDTH)

    def draw(self):
        screen.blit(asteroid_img, (self.x, self.y))

# Fuel class
class Fuel:
    def __init__(self):
        self.x = random.randint(0, WIDTH - FUEL_WIDTH)
        self.y = random.randint(0, HEIGHT - FUEL_HEIGHT)

    def draw(self):
        screen.blit(fuel_img, (self.x, self.y))

# Main game loop
def main():
    spaceship = Spaceship()
    asteroids = [Asteroid() for _ in range(5)]
    fuel = Fuel()
    running = True

    while running:
        screen.fill(BLACK)

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        spaceship.move(keys)

        # Draw objects
        spaceship.draw()

        for asteroid in asteroids:
            asteroid.move()
            asteroid.draw()

            # Check for collisions with asteroids
            if spaceship.x < asteroid.x + ASTEROID_WIDTH and spaceship.x + SPACESHIP_WIDTH > asteroid.x and spaceship.y < asteroid.y + ASTEROID_HEIGHT and spaceship.y + SPACESHIP_HEIGHT > asteroid.y:
                print("Game Over!")
                running = False

        # Fuel collection
        fuel.draw()
        if spaceship.x < fuel.x + FUEL_WIDTH and spaceship.x + SPACESHIP_WIDTH > fuel.x and spaceship.y < fuel.y + FUEL_HEIGHT and spaceship.y + SPACESHIP_HEIGHT > fuel.y:
            spaceship.fuel += 20
            spaceship.score += 10
            print(f"Fuel collected! Fuel: {spaceship.fuel}, Score: {spaceship.score}")
            fuel = Fuel()  # Respawn fuel

        # Update display and limit FPS
        pygame.display.flip()
        clock.tick(60)

# Run the game
main()
pygame.quit()

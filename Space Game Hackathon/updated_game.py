import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 50
ASTEROID_WIDTH, ASTEROID_HEIGHT = 40, 40
FUEL_WIDTH, FUEL_HEIGHT = 30, 30
ENEMY_WIDTH, ENEMY_HEIGHT = 50, 50

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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

enemy_img = pygame.image.load("C:\\Users\\debna\\OneDrive\\Desktop\\spaceship_enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))

# Load sounds
pygame.mixer.music.load("C:\\Users\\debna\\OneDrive\\Desktop\\interstellar.mp3")
collision_sound = pygame.mixer.Sound("C:\\Users\\debna\\OneDrive\\Desktop\\impulse.mp3")
powerup_sound = pygame.mixer.Sound("C:\\Users\\debna\\OneDrive\\Desktop\\level_up.mp3")

# Start background music
pygame.mixer.music.play(-1)  # Loop the background music

# Clock
clock = pygame.time.Clock()

# Background stars
stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT)] for _ in range(100)]

# Spaceship class
class Spaceship:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 100
        self.speed = 5
        self.fuel = 100
        self.score = 0
        self.lives = 3  # 3 Lives for the spaceship
        self.shield = False  # New feature: Shield power-up

    def draw(self):
        screen.blit(spaceship_img, (self.x, self.y))
        if self.shield:
            pygame.draw.circle(screen, BLUE, (self.x + SPACESHIP_WIDTH // 2, self.y + SPACESHIP_HEIGHT // 2), 40, 2)

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

# Enemy ship class
class Enemy:
    def __init__(self):
        self.x = random.randint(0, WIDTH - ENEMY_WIDTH)
        self.y = random.randint(-100, -ENEMY_HEIGHT)
        self.speed = random.randint(3, 6)

    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = random.randint(-100, -ENEMY_HEIGHT)
            self.x = random.randint(0, WIDTH - ENEMY_WIDTH)

    def draw(self):
        screen.blit(enemy_img, (self.x, self.y))

# Function to move background stars
def move_stars():
    for star in stars:
        star[1] += 2  # Scroll stars down
        if star[1] > HEIGHT:
            star[1] = 0
            star[0] = random.randint(0, WIDTH)
        pygame.draw.circle(screen, WHITE, star, 2)

# Function to display score, fuel, and lives
def display_info(spaceship):
    font = pygame.font.SysFont(None, 30)
    score_text = font.render(f"Score: {spaceship.score}", True, WHITE)
    fuel_text = font.render(f"Fuel: {spaceship.fuel}", True, WHITE)
    
    screen.blit(score_text, (10, 10))
    screen.blit(fuel_text, (10, 40))
    

# Main game loop
def main():
    spaceship = Spaceship()
    asteroids = [Asteroid() for _ in range(5)]
    fuel = Fuel()
    enemies = [Enemy() for _ in range(3)]
    running = True

    # Timer variables for fuel decrease and score increase
    last_time = pygame.time.get_ticks()
    interval = 5000  # 5 seconds in milliseconds

    while running:
        screen.fill(BLACK)
        move_stars()

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Timer logic to reduce fuel and increase score every 5 seconds
        current_time = pygame.time.get_ticks()
        if current_time - last_time > interval:
            spaceship.fuel -= 20
            spaceship.score += 100
            last_time = current_time

        # Check if fuel is depleted
        if spaceship.fuel <= 0 or spaceship.lives == 0:
            print("Game Over!")
            running = False

        keys = pygame.key.get_pressed()
        spaceship.move(keys)

        # Draw and update objects
        spaceship.draw()

        for asteroid in asteroids:
            asteroid.move()
            asteroid.draw()
            # Collision detection with asteroids
            if not spaceship.shield and spaceship.x < asteroid.x + ASTEROID_WIDTH and spaceship.x + SPACESHIP_WIDTH > asteroid.x and spaceship.y < asteroid.y + ASTEROID_HEIGHT and spaceship.y + SPACESHIP_HEIGHT > asteroid.y:
                pygame.mixer.Sound.play(collision_sound)
                print("Game Over! Collision with asteroid.")
                running = False

        for enemy in enemies:
            enemy.move()
            enemy.draw()
            # Collision detection with enemy ships
            if spaceship.x < enemy.x + ENEMY_WIDTH and spaceship.x + SPACESHIP_WIDTH > enemy.x and spaceship.y < enemy.y + ENEMY_HEIGHT and spaceship.y + SPACESHIP_HEIGHT > enemy.y:
                spaceship.lives -= 1  # Lose 1 life when hit by enemy
                pygame.mixer.Sound.play(collision_sound)
                print(f"Hit by enemy! Lives remaining: {spaceship.lives}")
                enemy = Enemy()  # Respawn enemy at a new position

        # Fuel collection
        fuel.draw()
        if spaceship.x < fuel.x + FUEL_WIDTH and spaceship.x + SPACESHIP_WIDTH > fuel.x and spaceship.y < fuel.y + FUEL_HEIGHT and spaceship.y + SPACESHIP_HEIGHT > fuel.y:
            spaceship.fuel += 20
            spaceship.score += 10
            pygame.mixer.Sound.play(powerup_sound)
            print(f"Fuel collected! Fuel: {spaceship.fuel}, Score: {spaceship.score}")
            fuel = Fuel()  # Respawn fuel

        # Update UI elements
        display_info(spaceship)

        # Update display and limit FPS
        pygame.display.flip()
        clock.tick(60)

# Run the game
main()
pygame.quit()

import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1370, 700
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 30, 40
ASTEROID_WIDTH, ASTEROID_HEIGHT = 50, 50
FUEL_WIDTH, FUEL_HEIGHT = 30, 30
ENEMY_WIDTH, ENEMY_HEIGHT = 50, 50
BULLET_WIDTH, BULLET_HEIGHT = 4, 30  # Size for enemy bullets
HEART_WIDTH, HEART_HEIGHT = 30, 30  # Heart size
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cosmic Craftathon - Space Exploration")

import os
import pygame

# Get the current directory of the game file
game_folder = os.path.dirname(__file__)

# Define paths to the asset folders
image_folder = os.path.join(game_folder, 'assets', 'images')
sound_folder = os.path.join(game_folder, 'assets', 'sounds')

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cosmic Craftathon - Space Exploration")

# Load images
spaceship_img = pygame.image.load(os.path.join(image_folder, "spaceship.png"))
spaceship_img = pygame.transform.scale(spaceship_img, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

asteroid_img = pygame.image.load(os.path.join(image_folder, "asteroid.png"))
asteroid_img = pygame.transform.scale(asteroid_img, (ASTEROID_WIDTH, ASTEROID_HEIGHT))

fuel_img = pygame.image.load(os.path.join(image_folder, "fuel.png"))
fuel_img = pygame.transform.scale(fuel_img, (FUEL_WIDTH, FUEL_HEIGHT))

enemy_img = pygame.image.load(os.path.join(image_folder, "spaceship_enemy.png"))
enemy_img = pygame.transform.scale(enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))

heart_img = pygame.image.load(os.path.join(image_folder, "heart.png"))
heart_img = pygame.transform.scale(heart_img, (HEART_WIDTH, HEART_HEIGHT))

# Load sounds
pygame.mixer.music.load(os.path.join(sound_folder, "interstellar.mp3"))
collision_sound = pygame.mixer.Sound(os.path.join(sound_folder, "impulse.mp3"))
powerup_sound = pygame.mixer.Sound(os.path.join(sound_folder, "level_up.mp3"))
extra_life_sound = pygame.mixer.Sound(os.path.join(sound_folder, "seatbelt-102265.mp3"))

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
        self.lives = 50  # 3 Lives for the spaceship
        self.shield = False   # New feature: Shield power-up
        self.bullets = []  # List to hold active bullets

    def draw(self):
        screen.blit(spaceship_img, (self.x, self.y))
        if self.shield:
            pygame.draw.circle(screen, BLUE, (self.x + SPACESHIP_WIDTH // 2, self.y + SPACESHIP_HEIGHT // 2), 40, 2)
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw()

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x - self.speed > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x + self.speed + SPACESHIP_WIDTH < WIDTH:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y - self.speed > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y + self.speed + SPACESHIP_HEIGHT < HEIGHT:
            self.y += self.speed
    def fire_bullet(self):
        bullet = Bullet(self.x + SPACESHIP_WIDTH // 2 - BULLET_WIDTH // 2, self.y)
        self.bullets.append(bullet)  # Add bullet to the list

# Asteroid class
class Asteroid:
    def __init__(self):
        self.x = random.randint(0, WIDTH - ASTEROID_WIDTH)
        self.y = random.randint(-100, -ASTEROID_HEIGHT)
        self.speed = random.randint(2, 8)

    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = random.randint(-100, -ASTEROID_HEIGHT)
            self.x = random.randint(0, WIDTH - ASTEROID_WIDTH)

    def draw(self):
        screen.blit(asteroid_img, (self.x, self.y))

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10

    def move(self):
        self.y -= self.speed  # Move bullet upwards

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, BULLET_WIDTH, BULLET_HEIGHT))  # Draw bullet as a rectangle

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
        self.speed = random.randint(3, 8)
        self.bullet_timer = 0 # Timer for shooting

    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = random.randint(-100, -ENEMY_HEIGHT)
            self.x = random.randint(0, WIDTH - ENEMY_WIDTH)

    def draw(self):
        screen.blit(enemy_img, (self.x, self.y))

    def shoot(self):
        if pygame.time.get_ticks() - self.bullet_timer > 1000:  # Shoot every second
            self.bullet_timer = pygame.time.get_ticks()
            return EnemyBullet(self.x + ENEMY_WIDTH // 2, self.y + ENEMY_HEIGHT)
        return None

# Bullet class for enemies
class EnemyBullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 9

    def move(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, BULLET_WIDTH, BULLET_HEIGHT))

    def is_off_screen(self):
        return self.y > HEIGHT

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
    lives_text = font.render(f"Lives: {spaceship.lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(fuel_text, (10, 40))
    screen.blit(lives_text, (10, 70))

# New enemy class with different properties
class FastEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.speed = random.randint(6, 10)  # Faster speed
        self.bullet_timer = 0  # Timer for shooting

    def shoot(self):
        if pygame.time.get_ticks() - self.bullet_timer > 700:  # Shoot every 0.7 seconds
            self.bullet_timer = pygame.time.get_ticks()
            return EnemyBullet(self.x + ENEMY_WIDTH // 2, self.y + ENEMY_HEIGHT)
        return None


# Inside your game loop


# Add bullet class if not already present
class Bullet:
    def __init__(self, x, y, strong=False):
        self.x = x
        self.y = y
        self.width = 5 if not strong else 10  # Strong bullet is wider
        self.height = 10 if not strong else 20  # Strong bullet is taller
        self.speed = 5 if not strong else 10  # Strong bullet moves faster
        self.color = (255, 255, 0) if not strong else (255, 0, 255)  # Different color for strong bullets

    def move(self):
        self.y += self.speed  # Move bullet downward

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))  # Draw the bullet

class HeartLife:
    def __init__(self):
        self.x = random.randint(0, WIDTH - HEART_WIDTH)
        self.y = random.randint(0, HEIGHT - HEART_HEIGHT)
        self.visible = False
        self.spawn_time = pygame.time.get_ticks()
        self.duration = 5000  # Heart is visible for 5 seconds

    def spawn(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > 30000:  # Heart appears after 30 seconds
            self.visible = True
            self.spawn_time = current_time

    def draw(self):
        if self.visible:
            screen.blit(heart_img, (self.x, self.y))

    def check_collision(self, spaceship):
        if self.visible and spaceship.x < self.x + HEART_WIDTH and spaceship.x + SPACESHIP_WIDTH > self.x and spaceship.y < self.y + HEART_HEIGHT and spaceship.y + SPACESHIP_HEIGHT > self.y:
            spaceship.lives += 20  # Add one life
            pygame.mixer.Sound.play(extra_life_sound)
            self.visible = False  # Hide the heart after collection

    def disappear(self):
        if self.visible:
            current_time = pygame.time.get_ticks()
            if current_time - self.spawn_time > self.duration:  # Heart disappears after 5 seconds
                self.visible = False

# In the main game loop
def main():
    spaceship = Spaceship()
    asteroids = [Asteroid() for _ in range(9)]
    fuels = [Fuel() for _ in range(1)]  # Create 3 fuel tanks
    enemies = [Enemy() for _ in range(10)]
    enemy_bullets = []
    fast_enemy_added = False  # Track if fast enemy has been added
    heart_life = HeartLife()  # Create heart life instance
    running = True

    # Timer variables for fuel tanks
    fuel_spawn_time = pygame.time.get_ticks()  # Track when fuels appear
    fuel_duration = 6000  # 10 seconds for fuels to stay
    fuel_respawn_interval = 15000  # 15 seconds to reappear after disappearing
    fuel_visible = True  # Track if fuels are visible

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
            spaceship.fuel -= 10
            spaceship.score += 100
            last_time = current_time

        # Introduce new enemy when score reaches 1000
        if spaceship.score >= 1000 and not fast_enemy_added:
            enemies.append(FastEnemy())
            fast_enemy_added = True

        # Check if fuel is depleted or lives are 0
        if spaceship.fuel <= 0 or spaceship.lives == 0:
            print("Game Over!")
            running = False

        keys = pygame.key.get_pressed()
        spaceship.move(keys)
        
        
        heart_life.spawn()
        heart_life.draw()
        heart_life.check_collision(spaceship)
        heart_life.disappear()
        
        
        # Fuel appearance logic: control visibility and respawn
        if fuel_visible and current_time - fuel_spawn_time > fuel_duration:
            fuel_visible = False  # Hide fuel tanks after 10 seconds
            fuel_spawn_time = current_time  # Start the respawn timer
        elif not fuel_visible and current_time - fuel_spawn_time > fuel_respawn_interval:
            fuels = [Fuel() for _ in range(3)]  # Respawn 3 new fuels
            fuel_visible = True
            fuel_spawn_time = current_time  # Reset the spawn time

        # Draw and update objects
        spaceship.draw()

        for asteroid in asteroids:
            asteroid.move()
            asteroid.draw()
            # Collision detection with asteroids
            if not spaceship.shield and spaceship.x < asteroid.x + ASTEROID_WIDTH and spaceship.x + SPACESHIP_WIDTH > asteroid.x and spaceship.y < asteroid.y + ASTEROID_HEIGHT and spaceship.y + SPACESHIP_HEIGHT > asteroid.y:
                pygame.mixer.Sound.play(collision_sound)
                
                spaceship.lives -= 1
                print(f"Lives remaining: {spaceship.lives:.1f}") 
                
                
                        # Check if lives have reached zero
                if spaceship.lives <= 0:
                    print("Game Over! No lives remaining.")
                    running = False  # End the game loop

        
        
        # Check for collisions with fuel tanks if they are visible
        if fuel_visible:
            for fuel in fuels:
                fuel.draw()
                # Check for collision with spaceship and refuel
                if spaceship.x < fuel.x + FUEL_WIDTH and spaceship.x + SPACESHIP_WIDTH > fuel.x and spaceship.y < fuel.y + FUEL_HEIGHT and spaceship.y + SPACESHIP_HEIGHT > fuel.y:
                    spaceship.fuel += 20
                    if spaceship.fuel > 100:  # Limit fuel to max 100
                        spaceship.fuel = 100
                    pygame.mixer.Sound.play(powerup_sound)  # Play powerup sound
                    fuels.remove(fuel)  # Remove fuel that was collected

                    
                    
        for enemy in enemies:
            enemy.move()
            enemy.draw()
            # Shooting mechanism
            bullet = enemy.shoot()
            if bullet:
                enemy_bullets.append(bullet)

        for bullet in enemy_bullets:
            bullet.move()
            bullet.draw()
            if bullet.is_off_screen():
                enemy_bullets.remove(bullet)
            # Collision detection with spaceship
            if spaceship.x < bullet.x + BULLET_WIDTH and spaceship.x + SPACESHIP_WIDTH > bullet.x and spaceship.y < bullet.y + BULLET_HEIGHT and spaceship.y + SPACESHIP_HEIGHT > bullet.y:
                spaceship.lives -= 10
                enemy_bullets.remove(bullet)
            if spaceship.lives <= 0:
                print("Game Over! No lives remaining.")
                running = False  # End the game loop    
          
        for bullet in spaceship.bullets[:]:  # Use a copy to avoid modification during iteration
            bullet.move()
            bullet.draw()
            if bullet.y < 0:  # Remove bullet if it goes off-screen
                spaceship.bullets.remove(bullet)

        # Display score, fuel, and lives
        display_info(spaceship)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()



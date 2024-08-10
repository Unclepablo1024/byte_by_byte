import pygame
import random
import os

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, folder_path, screen_width, ground_level, main_character):
        super().__init__()
        self.folder_path = folder_path
        self.enemy_type = enemy_type
        self.walk_images = self.load_images("Walk.png")
        self.attack_images = self.load_images("Attack_1.png")
        self.hurt_images = self.load_images("Hurt.png")
        self.dead_images = self.load_images("Dead.png")
        self.image = self.walk_images[0]
        self.rect = self.image.get_rect()
        self.hitbox = self.rect.inflate(-150, -150)

        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100
        self.health = 100
        self.current_frame = 0
        self.state = "walking"
        self.is_dead = False
        self.screen_width = screen_width
        self.ground_level = ground_level
        self.main_character = main_character
        self.direction = -1
        self.attack_distance = 35
        self.attack_damage = 10
        self.speed = 2
        self.hits_received = 0
        self.max_hits = 1
        self.death_start_time = None
        self.damage_time = None
        self.reset_position()

    def set_enemy_attributes(self):
        if "Robot" in self.enemy_type:
            self.speed = 3
            self.attack_power = 15
            self.health = 120
        elif "Vampire" in self.enemy_type:
            self.speed = 4
            self.attack_power = 20
            self.health = 100
        elif self.enemy_type in ["Cat", "Dog"]:
            self.speed = 5
            self.attack_power = 10
            self.health = 80
        else:  # Homeless
            self.speed = 2
            self.attack_power = 5
            self.health = 100

    def load_images(self, action):
        images = []
        image_path = os.path.join(self.folder_path, self.enemy_type, action)
        image = pygame.image.load(image_path).convert_alpha()
        width, height = image.get_size()
        frame_height = height
        for i in range(width // frame_height):
            frame_rect = pygame.Rect(i * frame_height, 0, frame_height, frame_height)
            frame = image.subsurface(frame_rect)
            images.append(frame)
        return images

    def draw_rectangle(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def update(self):
        now = pygame.time.get_ticks()

        #Handle death state
        if self.is_dead:
            if self.death_start_time and now - self.death_start_time > 2000:
                self.kill()
            elif now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_frame = min(self.current_frame + 1, len(self.dead_images) - 1)
                self.image = self.dead_images[self.current_frame]
            return
        
        # Handle movement and attack logic if the character is not dead
        if self.main_character and not self.is_dead:
            player_x = self.main_character.rect.centerx
            enemy_x = self.rect.centerx
            distance = abs(player_x - enemy_x)

            #Determines Direction and attack state
            if distance < self.attack_distance:
                self.attack()
                self.direction = 1 if player_x > enemy_x else -1
            else:
                self.stop_attack()
                self.direction = -1 if player_x < enemy_x else 1

            if self.state == "walking":
                self.move(self.speed * self.direction, 0)

            if now - self.last_update > self.frame_rate:
                self.last_update = now
                if self.state == "attacking":
                    self.current_frame = (self.current_frame + 1) % len(self.attack_images)
                    self.image = self.attack_images[self.current_frame]
                    if self.current_frame == 0 and not self.main_character.is_dead:
                        self.main_character.hurt(self.attack_damage)
                elif self.state == "walking":
                    self.current_frame = (self.current_frame + 1) % len(self.walk_images)
                    self.image = self.walk_images[self.current_frame]

            self.image = pygame.transform.flip(self.image, self.direction == 1, False)

            new_rect = self.image.get_rect()
            new_rect.bottom = self.ground_level
            new_rect.centerx = self.rect.centerx

            self.rect = new_rect
            self.hitbox = self.rect.inflate(-150, -150)

        # Check if it's time to apply delayed damage
        if self.damage_time and now >= self.damage_time:
            self.take_damage(self.main_character.attack_damage)
            self.damage_time = None

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.bottom = self.ground_level

    def reset_position(self):
        self.rect.bottom = self.ground_level
        self.rect.left = self.screen_width + random.randint(50, 200)
        self.state = "walking"
        self.current_frame = 0
        self.image = self.walk_images[self.current_frame]
        self.direction = -1
        self.is_dead = False
        self.set_enemy_attributes()  # Reset health and other attributes

    def attack(self):
        if self.state != "attacking":
            self.state = "attacking"
            self.current_frame = 0
            if self.main_character and not self.main_character.is_dead:
                self.main_character.hurt(self.attack_damage)

            return self.attack_power
        return 0

    def stop_attack(self):
        if self.state != "walking":
            self.state = "walking"
            self.current_frame = 0

    def take_damage(self, damage):

        if not self.is_dead:
            self.hits_received += 1
            if self.hits_received >= self.max_hits:
                self.die()
            else:
                self.state = "hurt"
                self.current_frame = 0
                self.image = self.hurt_images[self.current_frame]

    def die(self):
        self.is_dead = True
        self.current_frame = 0
        self.death_start_time = pygame.time.get_ticks()
        self.image = self.dead_images[self.current_frame]

    def mark_for_damage(self, time):
        self.damage_time = time

    def is_off_screen(self):
        return self.rect.right < 0 or self.rect.left > self.screen_width

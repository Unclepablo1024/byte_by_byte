# # import pygame

# # #Adds the background for first level

# # class Background:
# #     def __init__(self, image_path, size):
# #         self.image = pygame.image.load(image_path).convert_alpha()
# #         self.image = pygame.transform.scale(self.image, size)
# #         self.rect = self.image.get_rect()
# #         self.rect.topleft = (0, 0)

# #     def draw(self, surface):
# #         surface.blit(self.image, self.rect.topleft)

# import pygame

# class Background:
#     def __init__(self, image_path, size):
#         self.image = pygame.image.load(image_path).convert_alpha()
#         self.image = pygame.transform.scale(self.image, size)
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (0, 0)
#         self.size = size

#     def update(self, dx):
#         self.rect.x -= dx
#         if self.rect.x <= -self.size[0]:
#             self.rect.x = 0

#     def draw(self, surface):
#         surface.blit(self.image, self.rect.topleft)
#         surface.blit(self.image, (self.rect.x + self.size[0], self.rect.y))

import pygame

class Background:
    def __init__(self, image_path, size):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.size = size
        self.rect1 = self.image.get_rect()
        self.rect2 = self.image.get_rect()
        self.rect1.topleft = (0, 0)
        self.rect2.topleft = (self.size[0], 0)

    def update(self, dx):
        if dx > 0:  # Only scroll the background if moving right (dx > 0)
            self.rect1.x -= dx
            self.rect2.x -= dx

            if self.rect1.right <= 0:
                self.rect1.x = self.rect2.right
            if self.rect2.right <= 0:
                self.rect2.x = self.rect1.right

    def draw(self, surface):
        surface.blit(self.image, self.rect1.topleft)
        surface.blit(self.image, self.rect2.topleft)

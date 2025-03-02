import pygame

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (25, 25, 25)
LIGHT_GRAY = (50, 50, 50)

SCREEN_W = 800
SCREEN_H = 450
TILE_SIZE = SCREEN_H // 10
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

grass = pygame.image.load("tiles/grass.jpg")
ground = pygame.image.load("tiles/ground.jpg")
stone = pygame.image.load("tiles/stone.jpg")
water = pygame.image.load("tiles/water.jpg")
lava = pygame.image.load("tiles/lava.jpg")

grass = pygame.transform.scale(grass, (TILE_SIZE, TILE_SIZE))
ground = pygame.transform.scale(ground, (TILE_SIZE, TILE_SIZE))
stone = pygame.transform.scale(stone, (TILE_SIZE, TILE_SIZE))
water = pygame.transform.scale(water, (TILE_SIZE, TILE_SIZE))
lava = pygame.transform.scale(lava, (TILE_SIZE, TILE_SIZE))


world_width = 25
world_height = 25
world = [[None] * world_width] * world_height

visible_world_width = 10
visible_world_height = 10

x_shift = 0
y_shift = 0


class Button:
    def __init__(self, tile, text):
        font = pygame.font.Font(None, 30)

        self.tile = tile
        self.tile_rect : pygame.Rect = self.tile.get_rect()

        self.text = font.render(text, True, WHITE)
        self.text_rect = self.text.get_rect()

        self.w = self.text_rect.width + TILE_SIZE + 50
        self.h = max(TILE_SIZE, self.text_rect.height) + 20
        self.rect = pygame.Rect(0, 0, self.w, self.h)

        self.is_hovered = False
        self.is_active = False

    def check_collision(self, pos):
        self.is_hovered = False
        if self.rect.collidepoint(pos):
            self.is_hovered = True
        return self.is_hovered

    def render(self, screen):
        if self.is_hovered:
            pygame.draw.rect(screen, GRAY, self.rect)
        if self.is_active:
            pygame.draw.rect(screen, LIGHT_GRAY, self.rect)
        screen.blit(self.text, self.text_rect)
        screen.blit(self.tile, self.tile_rect)


grass_btn = Button(grass, "Grass")
ground_btn = Button(ground, "Ground")
lava_btn = Button(lava, "Lava")
stone_btn = Button(stone, "Stone")
water_btn = Button(water, "Water")

grass_btn.rect.left = TILE_SIZE * 10 + 25
grass_btn.rect.top = TILE_SIZE // 2
grass_btn.tile_rect.left = grass_btn.rect.left + 20
grass_btn.tile_rect.centery = grass_btn.rect.centery
grass_btn.text_rect.left = grass_btn.tile_rect.right + 10
grass_btn.text_rect.centery = grass_btn.tile_rect.centery

ground_btn.rect.left = TILE_SIZE * 10 + 25
ground_btn.rect.top = grass_btn.rect.bottom +10
ground_btn.tile_rect.left = ground_btn.rect.left + 20
ground_btn.tile_rect.centery = ground_btn.rect.centery
ground_btn.text_rect.left = ground_btn.tile_rect.right + 10
ground_btn.text_rect.centery = ground_btn.tile_rect.centery


tiles_buttons = [grass_btn, ground_btn, stone_btn, water_btn]
selected_tile = None


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and y_shift > 0:
                y_shift -= 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                if y_shift < world_height - visible_world_height:
                    y_shift += 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and x_shift > 0:
                x_shift -= 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if x_shift < world_width - visible_world_width:
                    x_shift += 1

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            w = TILE_SIZE * visible_world_width
            h = TILE_SIZE * visible_world_height
            if x < w and y < h:
                tile_x = x // TILE_SIZE + x_shift
                tile_y = y // TILE_SIZE + y_shift
                world[tile_y][tile_x] = selected_tile

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            any_button_pressed = False
            for button in tiles_buttons:
                if button.check_collision(event.pos):
                    any_button_pressed = True
                    break

            if not any_button_pressed:
                continue

            for button in tiles_buttons:
                if button.check_collision(event.pos):
                    button.is_active = not button.is_active
                else:
                    button.is_active = False

    mouse_pos = pygame.mouse.get_pos()

    grass_btn.check_collision(mouse_pos)

    selected_tile = None
    for button in tiles_buttons:
        if button.is_active:
            selected_tile = button.tile

    screen.fill(BLACK)

    for i in range(visible_world_height):
        for j in range(visible_world_width):
            x = j * TILE_SIZE
            y = i * TILE_SIZE
            cell = world[i + y_shift][j + x_shift]
            if cell is not None:
                screen.blit(cell, (x, y))
            else:
                w = TILE_SIZE
                h = TILE_SIZE
                pygame.draw.rect(screen, WHITE, (x, y, w, h), 1)

    grass_btn.render(screen)

    pygame.time.delay(50)
    pygame.display.update()
pygame.quit()

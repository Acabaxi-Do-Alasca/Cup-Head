import pygame
import sys
import math
import random

pygame.init()

WIDTH, HEIGHT = 1000, 650
PLAYER_SPEED = 5
JUMP_HEIGHT = 19
GRAVITY = 1
PLAYER_BULLET_SPEED = 15
PLAYER_BULLET_DAMAGE = 5
BOSS_BULLET_SPEED = 8
BOSS_BULLET_DAMAGE = 10
BOSS_HEALTH = 100
PLAYER_HEALTH = 100
BOSS_DAMAGE_PERCENTAGE = 10

WHITE = (255, 255, 255)
RED = (255, 0, 0)

score = 0  # Adicione uma variável de pontuação

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boss Battle")

background_image = pygame.image.load("fundo.jpeg")
player_image = pygame.Surface((50, 50))
player_image.fill(RED)

player_image = pygame.image.load("dinosaur3.png")
player_image = pygame.transform.scale(player_image, (50, 50))


boss_image = pygame.image.load("Bruno.png")
boss_image = pygame.transform.scale(boss_image, (150, 510))

boss2_image = pygame.image.load("Bruno.png")
boss2_image = pygame.transform.scale(boss2_image, (150, 510))

player_bullet_image = pygame.image.load("grito.png")
player_bullet_image = pygame.transform.scale(player_bullet_image, (20, 20))

boss_bullet_image = pygame.image.load("tiro.png")
boss_bullet_image = pygame.transform.scale(boss_bullet_image, (30, 30))

snake_images = []  # Lista para armazenar imagens de cobras
for i in range(2):  # Adiciona duas imagens diferentes de cobras
    snake_img_a = pygame.image.load(f"CobraA.png")
    snake_img_b = pygame.image.load(f"CobraB.png")
    snake_img_a = pygame.transform.scale(snake_img_a, (50, 400))
    snake_img_b = pygame.transform.scale(snake_img_b, (50, 400))
    snake_images.extend([snake_img_a, snake_img_b])

warning_image = pygame.image.load("aviso.png")
warning_image = pygame.transform.scale(warning_image, (50, 50))  # Ajuste o tamanho conforme necessário


player_pos = [50, HEIGHT - 60]
boss_pos = [WIDTH - 150, HEIGHT - 500]

player_velocity = [0, 0]
boss_velocity = [0, 0]

player_on_ground = False
jumps = 0
max_jumps = 2

boss_health = BOSS_HEALTH
player_health = PLAYER_HEALTH

bullets = []
boss_bullets = []

snake_warnings = []  # Lista para armazenar os quadrados vermelhos de aviso
snakes = []  # Lista para armazenar as cobras

clock = pygame.time.Clock()


def reset_level():
    global boss_pos, boss_health, boss_velocity, jumps
    boss_pos[0] = WIDTH - 150
    boss_pos[1] = HEIGHT - 500
    boss_health = BOSS_HEALTH
    boss_velocity = [0, 0]
    jumps = 0


def calculate_distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


reset_level()

boss_attack_timer = 0
snake_spawn_timer = pygame.time.get_ticks()

boss_attack_timer = 0
snake_spawn_timer = pygame.time.get_ticks()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and (player_on_ground or jumps < max_jumps):
                player_velocity[1] = -JUMP_HEIGHT
                player_on_ground = False
                jumps += 1
            elif event.key == pygame.K_c:
                bullets.append([player_pos[0] + 25, player_pos[1] + 25])

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_velocity[0] = -PLAYER_SPEED
    elif keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - 50:
        player_velocity[0] = PLAYER_SPEED
    else:
        player_velocity[0] = 0

    player_velocity[1] += GRAVITY
    player_pos[1] += player_velocity[1]

    if player_pos[1] >= HEIGHT - 60:
        player_pos[1] = HEIGHT - 60
        player_velocity[1] = 0
        player_on_ground = True
        jumps = 0

    player_pos[0] += player_velocity[0]

    # Atualizações do boss
    distance_to_player = calculate_distance(boss_pos, player_pos)
    if distance_to_player > 0:
        boss_pos[0] += boss_velocity[0]
        boss_pos[1] += boss_velocity[1]

    # Ataque do boss: lança bolas de fogo teleguiadas
    if pygame.time.get_ticks() - boss_attack_timer > random.randint(500, 1500):
        angle = math.atan2(player_pos[1] - boss_pos[1], player_pos[0] - boss_pos[0])
        boss_bullets.append([boss_pos[0] + 75, boss_pos[1] + 75, math.cos(angle) * BOSS_BULLET_SPEED, math.sin(angle) * BOSS_BULLET_SPEED])
        boss_attack_timer = pygame.time.get_ticks()

        # Atualizações dos quadrados de aviso
        warnings_to_remove = []  # Lista para armazenar os índices dos quadrados de aviso para remover
        for i, warning in enumerate(snake_warnings):
            if len(warning) > 2 and pygame.time.get_ticks() - warning[2] > 2000:  # Aviso aparece por 2 segundos
                snake_pos = [warning[0], HEIGHT - 100]
                snakes.append(snake_pos)  # Adiciona a cobra
                warnings_to_remove.append(i)  # Adiciona o índice do quadrado de aviso para remover

        # Remove os quadrados de aviso que expiraram
        for i in warnings_to_remove:
            if i < len(snake_warnings):  # Verifica se o índice ainda é válido
                snake_warnings.pop(i)

        # Desenha a imagem do quadrado de aviso
        for warning in snake_warnings:
            screen.blit(warning_image, (warning[0], warning[1]))

    # Atualizações dos tiros do jogador
    for bullet in bullets:
        bullet[0] += PLAYER_BULLET_SPEED

    # Verifica colisões com os tiros do jogador
    for bullet in bullets:
        if boss_pos[0] < bullet[0] < boss_pos[0] + 150 and boss_pos[1] < bullet[1] < boss_pos[1] + 150:
            boss_health -= PLAYER_BULLET_DAMAGE
            bullets.remove(bullet)

    # Atualizações dos tiros do boss
    for bullet in boss_bullets:
        bullet[0] += bullet[2]
        bullet[1] += bullet[3]

    # Verifica colisões com os tiros do boss
    for bullet in boss_bullets:
        if player_pos[0] < bullet[0] < player_pos[0] + 50 and player_pos[1] < bullet[1] < player_pos[1] + 50:
            player_health -= BOSS_DAMAGE_PERCENTAGE / 100 * PLAYER_HEALTH
            boss_bullets.remove(bullet)

    # Verifica colisão do jogador com o boss
    if player_pos[0] < boss_pos[0] + 150 and player_pos[0] + 50 > boss_pos[0] and player_pos[1] < boss_pos[1] + 150 and player_pos[1] + 50 > boss_pos[1]:
        player_health -= BOSS_DAMAGE_PERCENTAGE / 100 * PLAYER_HEALTH

    # Atualizações do spawn da cobra e dos quadrados de aviso
    if pygame.time.get_ticks() - snake_spawn_timer > 10000:  # A cada 10 segundos
        snake_warnings.append([random.randint(50, WIDTH - 100), HEIGHT - 100, pygame.time.get_ticks()])  # Adiciona quadrados de aviso
        snake_warnings.append([random.randint(50, WIDTH - 100), HEIGHT - 100, pygame.time.get_ticks()])
        snake_spawn_timer = pygame.time.get_ticks()  # Reinicia o temporizador

    # Atualizações das cobras
    for snake in snakes:
        if snake[1] < HEIGHT - 50:  # Se a cobra não atingiu o chão
            snake[1] -= 5  # Move a cobra para cima
        else:
            snakes.remove(snake)  # Remove a cobra quando atinge o chão

        # Verifica colisões do jogador com as cobras
        for snake_pos in snakes:
            if player_pos[0] < snake_pos[0] + 50 and player_pos[0] + 50 > snake_pos[0] and player_pos[1] < snake_pos[
                1] + 50 and \
                    player_pos[1] + 50 > snake_pos[1]:
                player_health -= 20  # Dano ao jogador
                snakes.remove(snake_pos)  # Remove a cobra

        # Atualizações do spawn da cobra e dos quadrados de aviso
        if pygame.time.get_ticks() - snake_spawn_timer > 10000:  # A cada 10 segundos
            # Adiciona cobras
            snake_pos = [random.randint(100, WIDTH - 50), HEIGHT - 100]
            snake_img = random.choice(snake_images)  # Escolhe uma imagem aleatória de cobra
            snakes.append([snake_pos, snake_img])
            snake_spawn_timer = pygame.time.get_ticks()  # Reinicia o temporizador

        # Verifica se a vida do boss atingiu zero
        if boss_health <= 0:
            reset_level()  # Reinicia o nível
            score += 1  # Incrementa a pontuação

    if player_health <= 0:
        pygame.quit()
        sys.exit()

        # Desenha na tela
    screen.blit(background_image, (0, 0))
    screen.blit(player_image, player_pos)
    if boss_health > 0:
        screen.blit(boss_image, boss_pos)
    else:
        screen.blit(boss2_image, boss_pos)

    for bullet in bullets:
        screen.blit(player_bullet_image, (bullet[0], bullet[1]))

    for bullet in boss_bullets:
        screen.blit(boss_bullet_image, (bullet[0], bullet[1]))

    for snake_pos in snakes:
        screen.blit(random.choice(snake_images), (snake_pos[0], snake_pos[1]))

    for warning in snake_warnings:
        screen.blit(warning_image, (warning[0], warning[1]))

    pygame.draw.rect(screen, (255, 0, 0), (10, 10, player_health * 2, 20))
    pygame.draw.rect(screen, (0, 255, 0), (WIDTH - 210, 10, boss_health * 2, 20))

    # Exibe a pontuação na tela
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 50))

    pygame.display.flip()
    clock.tick(60)
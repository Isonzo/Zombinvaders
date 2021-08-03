import pygame as pg
import entities
from zombie_generator import ZombieGenerator
def game(level, difficulty):
    # CONSTANTS
    SCREEN_HEIGHT = 240 * 2
    SCREEN_WIDTH = 256 * 2

    # VARIABLES
    collided = False
    seperator_hp = 5
    # Barra blanca que separa
    seperator = pg.Rect(420, 0, seperator_hp, SCREEN_HEIGHT)

    pg.mixer.init()
    pg.init()

    # RESIZABLE para poder cambiar su tamaño
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)
    # fake_screen es donde se debería hacer todos los blits y draws
    # Luego se le hace blit al screen para que todo este proporcional si cambia el tamaño de la pantalla
    fake_screen = screen.copy()

    running = True

    # Initialize players
    hero = entities.Player("hero", 230, SCREEN_HEIGHT/3)
    zero = entities.Player("zero", 230, SCREEN_HEIGHT * 2 / 3)
    # agregar player a player.Group y all_sprites.Group
    all_sprites = pg.sprite.Group()
    all_sprites.add(hero)
    all_sprites.add(zero)
    players = pg.sprite.Group()
    players.add(hero)
    players.add(zero)

    clock = pg.time.Clock()
    # Iniciar generador de zombies.
    zombie_generator = ZombieGenerator(level - difficulty, level/10 + 0.07 - difficulty/20)
    end_of_round = pg.USEREVENT + 1

    pg.time.set_timer(end_of_round, 10000)


    while running:
        # limit the framerate and get the delta time
        dt = clock.tick(60)
        # convert the delta to seconds (for easier calculation)
        delta_speed = float(dt)

        fake_screen.fill((0, 0, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.VIDEORESIZE:
                screen = pg.display.set_mode(event.size, pg.RESIZABLE)
            
            if event.type == end_of_round:
                print("next")
                game(level + 1, difficulty)


        # Input Handling
        for player in players:
            player.direction.xy = (0, 0)
        keys = pg.key.get_pressed()
        # Input Hero
        if keys[pg.K_LEFT]:
            hero.direction.x += -1
        if keys[pg.K_RIGHT]:
            hero.direction.x += 1
        if keys[pg.K_UP]:
            hero.direction.y += -1
        if keys[pg.K_DOWN]:
            hero.direction.y += 1
        if keys[pg.K_RETURN]:
            hero.shoot(dt)
        # Input Zero
        if keys[pg.K_a]:
            zero.direction.x += -1
        if keys[pg.K_d]:
            zero.direction.x += 1
        if keys[pg.K_w]:
            zero.direction.y += -1
        if keys[pg.K_s]:
            zero.direction.y += 1
        if keys[pg.K_c]:
            zero.shoot(dt)

        for player in players:
            if player.direction.x != 0 or player.direction.y != 0:  # Normalize vector
                pg.math.Vector2.normalize_ip(player.direction)

            move_speed = player.SPEED * delta_speed

            player.move(move_speed)
            player.delta -= dt

        # Zombie Generator
        zombie_generator.spawn(dt, all_sprites)

        for zombie in zombie_generator.zombies:
            zombie.direction.x = 1
            zombie.move(zombie.SPEED * delta_speed)

            if seperator.colliderect(zombie):
                zombie.kill()
                seperator_hp -= 1
            for player in players:  # Colisión balas con zombies
                gets_hit = pg.sprite.spritecollide(zombie, player.bullets, True)
                gets_attacked= pg.sprite.spritecollide(zombie, players, True)
                if gets_hit:
                    zombie.health -= 1
                    if zombie.health <= 0:
                        zombie.kill()
                        player.score += zombie.value
                if gets_attacked:
                    entities.sounds("reaccion_golpe.ogg")
        # Mover las balas
        for player in players:
            for bullet in player.bullets:
                bullet.direction.x = -1
                bullet.move(bullet.SPEED * delta_speed)
        seperator = pg.Rect(420 -seperator_hp, 0, seperator_hp, SCREEN_HEIGHT)

        pg.draw.rect(fake_screen, (255, 255, 255), seperator)
        all_sprites.draw(fake_screen)
        for player in players:
            player.bullets.draw(fake_screen)
        # Transformar fake_screen al tamaño de screen, y hacerle blit.
        screen.blit(pg.transform.scale(fake_screen, screen.get_rect().size), (0, 0))

        # Actualizar la pantalla
        pg.display.flip()
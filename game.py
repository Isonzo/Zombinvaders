import pygame as pg
from pygame.sprite import spritecollide
import entities
from zombie_generator import ZombieGenerator
from entities import sounds

def game():
    # CONSTANTS
    SCREEN_HEIGHT = 512
    SCREEN_WIDTH = 480

    # VARIABLES
    collided = False

    seperator_hp = 300

    # Barra blanca que separa
    seperator = pg.Rect(120, 0, seperator_hp, SCREEN_HEIGHT)


    pg.mixer.init()
    pg.init()

    # RESIZABLE para poder cambiar su tamaño
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)
    # fake_screen es donde se debería hacer todos los blits y draws
    # Luego se le hace blit al screen para que todo este proporcional si cambia el tamaño de la pantalla
    fake_screen = screen.copy()

    running = True

    # Initialize players
    hero = entities.Player("player", 230, SCREEN_HEIGHT/3)
    zero = entities.Player("player2", 230, SCREEN_HEIGHT * 2 / 3)
    # agregar player a player.Group y all_sprites.Group
    all_sprites = pg.sprite.Group()
    all_sprites.add(hero)
    all_sprites.add(zero)
    players = pg.sprite.Group()
    players.add(hero)
    players.add(zero)

    clock = pg.time.Clock()
    # Iniciar generador de zombies.
    zombie_generator = ZombieGenerator([], 0.3, 80)#new
    zombies = []

    # Imagen al perder
    game_over = pg.image.load("assets/over.gif")
    posx,posy= 0,-85

    # Timer
    clock = pg.time.Clock()
    counter, font= 10, "Consolas"
    counter, text =counter,"Timer: "+ str(counter).rjust(3)
    pg.time.set_timer(pg.USEREVENT, 1000)
    font = pg.font.SysFont(font, 15)

    sounds("gamesong3.mp3")# solo para no aburrirse
    while running:
        
        # limit the framerate and get the delta time
        dt = clock.tick(120)
        # convert the delta to seconds (for easier calculation)
        delta_speed = float(dt)

        fake_screen.fill((0, 0, 0))

        for event in pg.event.get():
            # TIMER
            if event.type == pg.USEREVENT: 
                    counter -= 1
                    text ="Timer: "+ str(counter).rjust(3) if counter > 0 else "Se acabó D:"

            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.VIDEORESIZE:
                screen = pg.display.set_mode(event.size, pg.RESIZABLE)

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
            entities.sounds("disparo.ogg")

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
            entities.sounds("disparo.ogg")

            zero.shoot(dt)
        

        for player in players:
            if player.direction.x != 0 or player.direction.y != 0:  # Normalize vector
                pg.math.Vector2.normalize_ip(player.direction)

            move_speed = player.SPEED * delta_speed

            player.move(move_speed)
            player.delta -= dt

        # Zombie Generator
        if seperator_hp>0 and counter>0: # Continua generando zombies
            zombie_generator.spawn(dt, all_sprites)
        
        elif seperator_hp>0 and counter==0:
            sounds("victoria.mp3")
            print("Ir juego nivel 2")
            game2()

        elif seperator_hp==0 and counter>0: # PERDIO, ya no genera más zombies
            fake_screen.blit(game_over,(posx,posy))
            counter=0 # Detiene el counter si perdio
            game()

        elif seperator_hp==0 and counter<=0: # PERDIO y se sigue mostrando imagen de "Game Over"
            fake_screen.blit(game_over,(posx,posy))
            game()

        for zombie in zombie_generator.zombies:
            zombie.direction.xy = (0, 0)
            zombie.direction.x += 1
            
            zombie.move(zombie.SPEED * delta_speed)
            for player in players:  # Colisión balas con zombies
                gets_hit = pg.sprite.spritecollide(zombie, player.bullets, True)
                gets_attacked= pg.sprite.spritecollide(zombie, players, True) # new
                if seperator.colliderect(zombie):
                    print("boom")
                    sounds("reaccion golpe.mp3")
                    zombie.kill()
                    seperator_hp-=5
                    player.temp-=5
                    seperator = pg.Rect(120, 0, seperator_hp, SCREEN_HEIGHT)
                    if seperator_hp==0:
                        print("Game Over")
                        game()
                        print(player.score)
                        seperator = pg.Rect(120, 0, seperator_hp, SCREEN_HEIGHT)
                        break  
                    if seperator_hp>0 and counter==0 :
                        print("Winnnnn!")
                    
                            

                if gets_hit: 
                    zombie.health -= 10
                    print(zombie.health)

                    if zombie.health <= 0:
                        zombie.kill()
                        player.score += 100
                if gets_attacked:
                    entities.sounds("reaccion_golpe.ogg")


                if gets_attacked: # new
                    sounds("reaccion golpe.mp3")

        # Mover las balas
        for player in players:
            for bullet in player.bullets:
                bullet.direction.x = -1
                bullet.move(bullet.SPEED * delta_speed)

        fake_screen.blit(font.render(text, 1, (230,0,0)), (10, 10))
        pg.draw.rect(fake_screen, (255, 255, 255), seperator)
        all_sprites.draw(fake_screen)
        for player in players:
            player.bullets.draw(fake_screen)
        # Transformar fake_screen al tamaño de screen, y hacerle blit.
        screen.blit(pg.transform.scale(fake_screen, screen.get_rect().size), (0, 0))

        # Actualizar la pantalla
        pg.display.flip()

game()


def game2():
    print("Game 2")
    # CONSTANTS
    SCREEN_HEIGHT = 512
    SCREEN_WIDTH = 480

    # VARIABLES
    collided = False

    seperator_hp = 200

    # Barra blanca que separa
    seperator = pg.Rect(315, 0, seperator_hp, SCREEN_HEIGHT)


    pg.mixer.init()
    pg.init()

    # RESIZABLE para poder cambiar su tamaño
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)
    # fake_screen es donde se debería hacer todos los blits y draws
    # Luego se le hace blit al screen para que todo este proporcional si cambia el tamaño de la pantalla
    fake_screen = screen.copy()

    running = True

    # Initialize players
    hero = entities.Player("player", 230, SCREEN_HEIGHT/3)
    zero = entities.Player("player2", 230, SCREEN_HEIGHT * 2 / 3)
    # agregar player a player.Group y all_sprites.Group
    all_sprites = pg.sprite.Group()
    all_sprites.add(hero)
    all_sprites.add(zero)
    players = pg.sprite.Group()
    players.add(hero)
    players.add(zero)

    clock = pg.time.Clock()
    # Iniciar generador de zombies.
    zombie_generator = ZombieGenerator([], 0.3, 80)#new
    zombies = []

    # Imagen al perder
    game_over = pg.image.load("assets/over.gif")
    posx,posy= 0,-85

    # Timer
    clock = pg.time.Clock()
    counter, font= 60, "Consolas"
    counter, text =counter,"Timer: "+ str(counter).rjust(3)
    pg.time.set_timer(pg.USEREVENT, 1000)
    font = pg.font.SysFont(font, 15)

    sounds("gamesong3.mp3")# solo para no aburrirse
    while running:
        
        # limit the framerate and get the delta time
        dt = clock.tick(120)
        # convert the delta to seconds (for easier calculation)
        delta_speed = float(dt)

        fake_screen.fill((0, 0, 0))

        for event in pg.event.get():
            # TIMER
            if event.type == pg.USEREVENT: 
                    counter -= 1
                    text ="Timer: "+ str(counter).rjust(3) if counter > 0 else "Se acabó D:"

            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.VIDEORESIZE:
                screen = pg.display.set_mode(event.size, pg.RESIZABLE)

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
            entities.sounds("disparo.ogg")

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
            entities.sounds("disparo.ogg")

            zero.shoot(dt)
        

        for player in players:
            if player.direction.x != 0 or player.direction.y != 0:  # Normalize vector
                pg.math.Vector2.normalize_ip(player.direction)

            move_speed = player.SPEED * delta_speed

            player.move(move_speed)
            player.delta -= dt

        # Zombie Generator
        if seperator_hp>0 and counter>0: # Continua generando zombies
            zombie_generator.spawn(dt, all_sprites)

        elif seperator_hp>0 and counter==0: # GANO
            sounds("victoria.mp3")
            print("Ir juego nivel 3")
            game3()
            
        elif seperator_hp==0 and counter>0: # PERDIO, ya no genera más zombies
            fake_screen.blit(game_over,(posx,posy))
            counter=0 # Detiene el counter si perdio

        elif seperator_hp==0 and counter<=0: # PERDIO y se sigue mostrando imagen de "Game Over"
            fake_screen.blit(game_over,(posx,posy))
            game2()
            print("Game 2")

        for zombie in zombie_generator.zombies:
            zombie.direction.xy = (0, 0)
            zombie.direction.x += 1
            
            zombie.move(zombie.SPEED * delta_speed)
            for player in players:  # Colisión balas con zombies
                gets_hit = pg.sprite.spritecollide(zombie, player.bullets, True)
                gets_attacked= pg.sprite.spritecollide(zombie, players, True) # new
                if seperator.colliderect(zombie):
                    print("boom")
                    sounds("reaccion golpe.mp3")
                    zombie.kill()
                    seperator_hp-=5
                    player.temp-=5
                    seperator = pg.Rect(315, 0, seperator_hp, SCREEN_HEIGHT)
                    if seperator_hp==0:
                        print("Game Over")
                        print(player.score)
                        seperator = pg.Rect(315, 0, seperator_hp, SCREEN_HEIGHT)
                        break  
                    if seperator_hp>0 and counter==0 :
                        print("Winnnnn!")
                            

                if gets_hit: 
                    zombie.health -= 10
                    print(zombie.health)

                    if zombie.health <= 0:
                        zombie.kill()
                        player.score += 100
                if gets_attacked:
                    entities.sounds("reaccion_golpe.ogg")


                if gets_attacked: # new
                    sounds("reaccion golpe.mp3")

        # Mover las balas
        for player in players:
            for bullet in player.bullets:
                bullet.direction.x = -1
                bullet.move(bullet.SPEED * delta_speed)

        fake_screen.blit(font.render(text, 1, (230,0,0)), (10, 10))
        pg.draw.rect(fake_screen, (255, 255, 255), seperator)
        all_sprites.draw(fake_screen)
        for player in players:
            player.bullets.draw(fake_screen)
        # Transformar fake_screen al tamaño de screen, y hacerle blit.
        screen.blit(pg.transform.scale(fake_screen, screen.get_rect().size), (0, 0))

        # Actualizar la pantalla
        pg.display.flip()




def game3():
    print("Game 3")
    # CONSTANTS
    SCREEN_HEIGHT = 512
    SCREEN_WIDTH = 480

    # VARIABLES
    collided = False

    seperator_hp = 200

    # Barra blanca que separa
    seperator = pg.Rect(315, 0, seperator_hp, SCREEN_HEIGHT)


    pg.mixer.init()
    pg.init()

    # RESIZABLE para poder cambiar su tamaño
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)
    # fake_screen es donde se debería hacer todos los blits y draws
    # Luego se le hace blit al screen para que todo este proporcional si cambia el tamaño de la pantalla
    fake_screen = screen.copy()

    running = True

    # Initialize players
    hero = entities.Player("player", 230, SCREEN_HEIGHT/3)
    zero = entities.Player("player2", 230, SCREEN_HEIGHT * 2 / 3)
    # agregar player a player.Group y all_sprites.Group
    all_sprites = pg.sprite.Group()
    all_sprites.add(hero)
    all_sprites.add(zero)
    players = pg.sprite.Group()
    players.add(hero)
    players.add(zero)

    clock = pg.time.Clock()
    # Iniciar generador de zombies.
    zombie_generator = ZombieGenerator([], 0.3, 80)#new
    zombies = []

    # Imagen al perder
    game_over = pg.image.load("assets/over.gif")
    posx,posy= 0,-85

    # Timer
    clock = pg.time.Clock()
    counter, font= 60, "Consolas"
    counter, text =counter,"Timer: "+ str(counter).rjust(3)
    pg.time.set_timer(pg.USEREVENT, 1000)
    font = pg.font.SysFont(font, 15)

    sounds("gamesong3.mp3")# solo para no aburrirse
    while running:
        
        # limit the framerate and get the delta time
        dt = clock.tick(120)
        # convert the delta to seconds (for easier calculation)
        delta_speed = float(dt)

        fake_screen.fill((0, 0, 0))

        for event in pg.event.get():
            # TIMER
            if event.type == pg.USEREVENT: 
                    counter -= 1
                    text ="Timer: "+ str(counter).rjust(3) if counter > 0 else "Se acabó D:"

            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.VIDEORESIZE:
                screen = pg.display.set_mode(event.size, pg.RESIZABLE)

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
            entities.sounds("disparo.ogg")

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
            entities.sounds("disparo.ogg")

            zero.shoot(dt)
        

        for player in players:
            if player.direction.x != 0 or player.direction.y != 0:  # Normalize vector
                pg.math.Vector2.normalize_ip(player.direction)

            move_speed = player.SPEED * delta_speed

            player.move(move_speed)
            player.delta -= dt

        # Zombie Generator
        if seperator_hp>0 and counter>0: # Continua generando zombies
            zombie_generator.spawn(dt, all_sprites)

        elif seperator_hp>0 and counter==0: # GANO
            sounds("victoria.mp3")
            print("Ir juego nivel 4")
            game4()
            
        elif seperator_hp==0 and counter>0: # PERDIO, ya no genera más zombies
            fake_screen.blit(game_over,(posx,posy))
            counter=0 # Detiene el counter si perdio

        elif seperator_hp==0 and counter<=0: # PERDIO y se sigue mostrando imagen de "Game Over"
            fake_screen.blit(game_over,(posx,posy))
            

        for zombie in zombie_generator.zombies:
            zombie.direction.xy = (0, 0)
            zombie.direction.x += 1
            
            zombie.move(zombie.SPEED * delta_speed)
            for player in players:  # Colisión balas con zombies
                gets_hit = pg.sprite.spritecollide(zombie, player.bullets, True)
                gets_attacked= pg.sprite.spritecollide(zombie, players, True) # new
                if seperator.colliderect(zombie):
                    print("boom")
                    sounds("reaccion golpe.mp3")
                    zombie.kill()
                    seperator_hp-=5
                    player.temp-=5
                    seperator = pg.Rect(315, 0, seperator_hp, SCREEN_HEIGHT)
                    if seperator_hp==0:
                        print("Game Over")
                        print(player.score)
                        seperator = pg.Rect(315, 0, seperator_hp, SCREEN_HEIGHT)
                        break  
                    if seperator_hp>0 and counter==0 :
                        print("Winnnnn!")
                            

                if gets_hit: 
                    zombie.health -= 10
                    print(zombie.health)

                    if zombie.health <= 0:
                        zombie.kill()
                        player.score += 100
                if gets_attacked:
                    entities.sounds("reaccion_golpe.ogg")


                if gets_attacked: # new
                    sounds("reaccion golpe.mp3")

        # Mover las balas
        for player in players:
            for bullet in player.bullets:
                bullet.direction.x = -1
                bullet.move(bullet.SPEED * delta_speed)

        fake_screen.blit(font.render(text, 1, (230,0,0)), (10, 10))
        pg.draw.rect(fake_screen, (255, 255, 255), seperator)
        all_sprites.draw(fake_screen)
        for player in players:
            player.bullets.draw(fake_screen)
        # Transformar fake_screen al tamaño de screen, y hacerle blit.
        screen.blit(pg.transform.scale(fake_screen, screen.get_rect().size), (0, 0))

        # Actualizar la pantalla
        pg.display.flip()


def game4():
    print("Game 4")
    # CONSTANTS
    SCREEN_HEIGHT = 512
    SCREEN_WIDTH = 480

    # VARIABLES
    collided = False

    seperator_hp = 200

    # Barra blanca que separa
    seperator = pg.Rect(315, 0, seperator_hp, SCREEN_HEIGHT)


    pg.mixer.init()
    pg.init()

    # RESIZABLE para poder cambiar su tamaño
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)
    # fake_screen es donde se debería hacer todos los blits y draws
    # Luego se le hace blit al screen para que todo este proporcional si cambia el tamaño de la pantalla
    fake_screen = screen.copy()

    running = True

    # Initialize players
    hero = entities.Player("player", 230, SCREEN_HEIGHT/3)
    zero = entities.Player("player2", 230, SCREEN_HEIGHT * 2 / 3)
    # agregar player a player.Group y all_sprites.Group
    all_sprites = pg.sprite.Group()
    all_sprites.add(hero)
    all_sprites.add(zero)
    players = pg.sprite.Group()
    players.add(hero)
    players.add(zero)

    clock = pg.time.Clock()
    # Iniciar generador de zombies.
    zombie_generator = ZombieGenerator([], 0.3, 80)#new
    zombies = []

    # Imagen al perder
    game_over = pg.image.load("assets/over.gif")
    posx,posy= 0,-85

    # Timer
    clock = pg.time.Clock()
    counter, font= 60, "Consolas"
    counter, text =counter,"Timer: "+ str(counter).rjust(3)
    pg.time.set_timer(pg.USEREVENT, 1000)
    font = pg.font.SysFont(font, 15)

    sounds("gamesong3.mp3")# solo para no aburrirse
    while running:
        
        # limit the framerate and get the delta time
        dt = clock.tick(120)
        # convert the delta to seconds (for easier calculation)
        delta_speed = float(dt)

        fake_screen.fill((0, 0, 0))

        for event in pg.event.get():
            # TIMER
            if event.type == pg.USEREVENT: 
                    counter -= 1
                    text ="Timer: "+ str(counter).rjust(3) if counter > 0 else "Se acabó D:"

            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.VIDEORESIZE:
                screen = pg.display.set_mode(event.size, pg.RESIZABLE)

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
            entities.sounds("disparo.ogg")

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
            entities.sounds("disparo.ogg")

            zero.shoot(dt)
        

        for player in players:
            if player.direction.x != 0 or player.direction.y != 0:  # Normalize vector
                pg.math.Vector2.normalize_ip(player.direction)

            move_speed = player.SPEED * delta_speed

            player.move(move_speed)
            player.delta -= dt

        # Zombie Generator
        if seperator_hp>0 and counter>0: # Continua generando zombies
            zombie_generator.spawn(dt, all_sprites)
        
        elif seperator_hp>0 and counter==0: # GANO
            sounds("victoria.mp3")
            print("Ir juego nivel 5")
            game5() 

        elif seperator_hp==0 and counter>0: # PERDIO, ya no genera más zombies
            fake_screen.blit(game_over,(posx,posy))
            counter=0 # Detiene el counter si perdio

        elif seperator_hp==0 and counter<=0: # PERDIO y se sigue mostrando imagen de "Game Over"
            fake_screen.blit(game_over,(posx,posy))
            game5()
            

        for zombie in zombie_generator.zombies:
            zombie.direction.xy = (0, 0)
            zombie.direction.x += 1
            
            zombie.move(zombie.SPEED * delta_speed)
            for player in players:  # Colisión balas con zombies
                gets_hit = pg.sprite.spritecollide(zombie, player.bullets, True)
                gets_attacked= pg.sprite.spritecollide(zombie, players, True) # new
                if seperator.colliderect(zombie):
                    print("boom")
                    sounds("reaccion golpe.mp3")
                    zombie.kill()
                    seperator_hp-=5
                    player.temp-=5
                    seperator = pg.Rect(315, 0, seperator_hp, SCREEN_HEIGHT)
                    if seperator_hp==0:
                        print("Game Over")
                        print(player.score)
                        seperator = pg.Rect(315, 0, seperator_hp, SCREEN_HEIGHT)
                        break  
                    if seperator_hp>0 and counter==0 :
                        print("Winnnnn!")
                            

                if gets_hit: 
                    zombie.health -= 10
                    print(zombie.health)

                    if zombie.health <= 0:
                        zombie.kill()
                        player.score += 100
                if gets_attacked:
                    entities.sounds("reaccion_golpe.ogg")


                if gets_attacked: # new
                    sounds("reaccion golpe.mp3")

        # Mover las balas
        for player in players:
            for bullet in player.bullets:
                bullet.direction.x = -1
                bullet.move(bullet.SPEED * delta_speed)

        fake_screen.blit(font.render(text, 1, (230,0,0)), (10, 10))
        pg.draw.rect(fake_screen, (255, 255, 255), seperator)
        all_sprites.draw(fake_screen)
        for player in players:
            player.bullets.draw(fake_screen)
        # Transformar fake_screen al tamaño de screen, y hacerle blit.
        screen.blit(pg.transform.scale(fake_screen, screen.get_rect().size), (0, 0))

        # Actualizar la pantalla
        pg.display.flip()


def game5():
    print("Noche 5")
    # CONSTANTS
    SCREEN_HEIGHT = 512
    SCREEN_WIDTH = 480

    # VARIABLES
    collided = False

    seperator_hp = 200

    # Barra blanca que separa
    seperator = pg.Rect(315, 0, seperator_hp, SCREEN_HEIGHT)


    pg.mixer.init()
    pg.init()

    # RESIZABLE para poder cambiar su tamaño
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)
    # fake_screen es donde se debería hacer todos los blits y draws
    # Luego se le hace blit al screen para que todo este proporcional si cambia el tamaño de la pantalla
    fake_screen = screen.copy()

    running = True

    # Initialize players
    hero = entities.Player("player", 230, SCREEN_HEIGHT/3)
    zero = entities.Player("player2", 230, SCREEN_HEIGHT * 2 / 3)
    # agregar player a player.Group y all_sprites.Group
    all_sprites = pg.sprite.Group()
    all_sprites.add(hero)
    all_sprites.add(zero)
    players = pg.sprite.Group()
    players.add(hero)
    players.add(zero)

    clock = pg.time.Clock()
    # Iniciar generador de zombies.
    zombie_generator = ZombieGenerator([], 0.3, 80)#new
    zombies = []

    # Imagen al perder
    game_over = pg.image.load("assets/over.gif")
    posx,posy= 0,-85

    # Timer
    clock = pg.time.Clock()
    counter, font= 60, "Consolas"
    counter, text =counter,"Timer: "+ str(counter).rjust(3)
    pg.time.set_timer(pg.USEREVENT, 1000)
    font = pg.font.SysFont(font, 15)

    sounds("gamesong3.mp3")# solo para no aburrirse
    while running:
        
        # limit the framerate and get the delta time
        dt = clock.tick(120)
        # convert the delta to seconds (for easier calculation)
        delta_speed = float(dt)

        fake_screen.fill((0, 0, 0))

        for event in pg.event.get():
            # TIMER
            if event.type == pg.USEREVENT: 
                    counter -= 1
                    text ="Timer: "+ str(counter).rjust(3) if counter > 0 else "Se acabó D:"

            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.VIDEORESIZE:
                screen = pg.display.set_mode(event.size, pg.RESIZABLE)

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
            entities.sounds("disparo.ogg")

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
            entities.sounds("disparo.ogg")

            zero.shoot(dt)
        

        for player in players:
            if player.direction.x != 0 or player.direction.y != 0:  # Normalize vector
                pg.math.Vector2.normalize_ip(player.direction)

            move_speed = player.SPEED * delta_speed

            player.move(move_speed)
            player.delta -= dt

        # Zombie Generator
        if seperator_hp>0 and counter>0: # Continua generando zombies
            zombie_generator.spawn(dt, all_sprites)
        
        elif seperator_hp>0 and counter==0: # GANO
            print("Ganaste el juego!")
            sounds("victoria.mp3")
            
        elif seperator_hp==0 and counter>0: # PERDIO, ya no genera más zombies
            fake_screen.blit(game_over,(posx,posy))
            counter=0 # Detiene el counter si perdio

        elif seperator_hp==0 and counter<=0: # PERDIO y se sigue mostrando imagen de "Game Over"
            fake_screen.blit(game_over,(posx,posy))
            

        for zombie in zombie_generator.zombies:
            zombie.direction.xy = (0, 0)
            zombie.direction.x += 1
            
            zombie.move(zombie.SPEED * delta_speed)
            for player in players:  # Colisión balas con zombies
                gets_hit = pg.sprite.spritecollide(zombie, player.bullets, True)
                gets_attacked= pg.sprite.spritecollide(zombie, players, True) # new
                if seperator.colliderect(zombie):
                    print("boom")
                    sounds("reaccion golpe.mp3")
                    zombie.kill()
                    seperator_hp-=5
                    player.temp-=5
                    seperator = pg.Rect(315, 0, seperator_hp, SCREEN_HEIGHT)
                    if seperator_hp==0:
                        print("Game Over")
                        print(player.score)
                        seperator = pg.Rect(315, 0, seperator_hp, SCREEN_HEIGHT)
                        break  
                    if seperator_hp>0 and counter==0 :
                        print("Winnnnn!")
                            

                if gets_hit: 
                    zombie.health -= 10
                    print(zombie.health)

                    if zombie.health <= 0:
                        zombie.kill()
                        player.score += 100
                if gets_attacked:
                    entities.sounds("reaccion_golpe.ogg")


                if gets_attacked: # new
                    sounds("reaccion golpe.mp3")

        # Mover las balas
        for player in players:
            for bullet in player.bullets:
                bullet.direction.x = -1
                bullet.move(bullet.SPEED * delta_speed)

        fake_screen.blit(font.render(text, 1, (230,0,0)), (10, 10))
        pg.draw.rect(fake_screen, (255, 255, 255), seperator)
        all_sprites.draw(fake_screen)
        for player in players:
            player.bullets.draw(fake_screen)
        # Transformar fake_screen al tamaño de screen, y hacerle blit.
        screen.blit(pg.transform.scale(fake_screen, screen.get_rect().size), (0, 0))

        # Actualizar la pantalla
        pg.display.flip()
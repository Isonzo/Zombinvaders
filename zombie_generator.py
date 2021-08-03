import random
import pygame as pg
from entities import Zombie, ZombieVariant, FastZombie, TankZombie


class ZombieGenerator:
    def __init__(self, level, frequency, maximum):
        self.level = level
        self.zombie_data = [Zombie, ZombieVariant, FastZombie, TankZombie]
        self.frequency = frequency
        self.maximum = maximum
        self.count = 0
        self.zombies = pg.sprite.Group()
        self.delta = 500

    def spawn(self, dt, all_sprites):
        self.delta -= dt
        if self.delta < 0:
            self.delta = random.randint(100, 800)
            self.count += 1
            if self.count < self.maximum and random.random() < self.frequency:
                if random.random() > 0.8:
                    choice = random.randint(0, self.level)
                else:
                    choice = random.randint(0, 1)
                new_zombie = self.zombie_data[choice](y=random.randint(0, 228))
                self.zombies.add(new_zombie)
                all_sprites.add(new_zombie)

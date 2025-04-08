import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math
import time

# Inisialisasi Pygame
pygame.init()
width, height = 800, 600
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Simulasi Penyebaran Penyakit")

# Setup OpenGL
gluOrtho2D(0, width, 0, height)
glClearColor(1.0, 1.0, 1.0, 1.0)  # Latar belakang putih

# Kelas untuk individu dalam populasi
class Person:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = "healthy"  # healthy, infected, recovered
        self.radius = 5
        self.speed = random.uniform(1, 3)
        self.angle = random.uniform(0, 2 * math.pi)
        self.infected_time = None
        self.recovered_time = None

    def move(self):
        # Pergerakan acak sederhana
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        # Pantulan jika menyentuh batas
        if self.x < 0 or self.x > width:
            self.angle = math.pi - self.angle
        if self.y < 0 or self.y > height:
            self.angle = -self.angle

    def draw(self):
        glBegin(GL_TRIANGLE_FAN)
        if self.state == "healthy":
            glColor3f(0, 1, 0)  # Hijau
        elif self.state == "infected":
            glColor3f(1, 0, 0)  # Merah
        else:
            glColor3f(0.5, 0.5, 0.5)  # Abu-abu
        for i in range(360):
            angle = i * math.pi / 180
            glVertex2f(self.x + math.cos(angle) * self.radius, self.y + math.sin(angle) * self.radius)
        glEnd()

    def distance_to(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

# Inisialisasi populasi
population = []
num_people = 50
for _ in range(num_people):
    x = random.randint(0, width)
    y = random.randint(0, height)
    population.append(Person(x, y))

# Infeksi individu pertama secara acak
# first_infected = random.randint(0, num_people - 1)
# population[first_infected].state = "infected"
# population[first_infected].infected_time = time.time()

# Infeksi dua individu secara acak
infected_indices = random.sample(range(num_people), 2)
for idx in infected_indices:
    population[idx].state = "infected"
    population[idx].infected_time = time.time()


# Fungsi untuk simulasi penyebaran penyakit
def spread_disease():
    current_time = time.time()
    for person in population:
        if person.state == "infected":
            if person.infected_time and current_time - person.infected_time > 5:  # Setelah 5 detik, menjadi recovered
                person.state = "recovered"
                person.recovered_time = current_time
            else:
                for other in population:
                    if other.state in ["healthy", "recovered"] and person.distance_to(other) < 50:  # Jarak infeksi diperluas
                        if random.random() < 0.3:  # Probabilitas infeksi meningkat
                            other.state = "infected"
                            other.infected_time = current_time
        elif person.state == "recovered":
            if person.recovered_time and current_time - person.recovered_time > 5:  # Setelah 5 detik, kembali menjadi healthy
                person.state = "healthy"

# Loop utama
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False

    # Update posisi dan penyakit
    for person in population:
        person.move()
    spread_disease()

    # Render
    glClear(GL_COLOR_BUFFER_BIT)
    for person in population:
        person.draw()
    pygame.display.flip()
    clock.tick(60)  # 60 FPS

# Cleanup

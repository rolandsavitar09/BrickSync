import pygame
import random
import os

# Inisialisasi pygame
pygame.init()

# Inisialisasi mixer untuk musik
pygame.mixer.init()

# Ukuran layar
WIDTH, HEIGHT = 600, 800
GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BrickSync: Galaxy Glow")

# Warna dasar (untuk cadangan jika tekstur tidak ditemukan)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Muat tekstur
textures = []
try:
    # Ganti dengan path ke gambar tekstur Anda
    texture_paths = ["c:/Semester 3/Pemrograman Berbasis Objek/BrickSync Galaxy Glow/Tekstur Gold.png", 
                     "c:/Semester 3/Pemrograman Berbasis Objek/BrickSync Galaxy Glow/Tekstur Merahh.png", 
                     "c:/Semester 3/Pemrograman Berbasis Objek/BrickSync Galaxy Glow/Tekstur Oren.png", 
                     "c:/Semester 3/Pemrograman Berbasis Objek/BrickSync Galaxy Glow/Tekstur Putih.png", 
                     "c:/Semester 3/Pemrograman Berbasis Objek/BrickSync Galaxy Glow/Tekstur Ungu.png"]
    textures = [pygame.transform.scale(pygame.image.load(path), (CELL_SIZE, CELL_SIZE)) for path in texture_paths]
except pygame.error:
    print("Tekstur tidak ditemukan. Menggunakan warna solid sebagai cadangan.")

# Font
FONT = pygame.font.Font(None, 36)
LARGE_FONT = pygame.font.Font(None, 72)

# Gambar background
try:
    background_image = pygame.image.load("c:/Semester 3/Pemrograman Berbasis Objek/BrickSync Galaxy Glow/Galaxy hitam.jpg")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
except pygame.error:
    background_image = None

# Muat dan putar musik latar
try:
    pygame.mixer.music.load("c:/Semester 3/Pemrograman Berbasis Objek/BrickSync Galaxy Glow/space_musik.mp3")
    pygame.mixer.music.play(-1)  # -1 berarti musik akan terus berulang
    pygame.mixer.music.set_volume(0.5)  # Atur volume (0.0 hingga 1.0)
except pygame.error:
    print("Musik tidak ditemukan atau tidak dapat dimainkan.")

# Highscore
def load_highscore():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as file:
            return int(file.read())
    return 0

def save_highscore(score):
    with open("highscore.txt", "w") as file:
        file.write(str(score))

# Kelas Balok dan Grid
class Block:
    def __init__(self):
        self.shape = random.choice(self.generate_shapes())
        self.texture_index = random.randint(0, len(textures) - 1)  
        self.x, self.y = GRID_SIZE // 2 - len(self.shape[0]) // 2, 0

    @staticmethod
    def generate_shapes():
        return [
            [[1, 1], [1, 1]],  # O
            [[1, 1, 1], [0, 1, 0]],  # T
            [[1, 1, 1], [1, 0, 0]],  # L
            [[1, 1, 1], [0, 0, 1]],  # J
            [[1, 1, 0], [0, 1, 1]],  # S
            [[0, 1, 1], [1, 1, 0]]   # Z
        ]

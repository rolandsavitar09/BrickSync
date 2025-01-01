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

    def draw(self, surface):
        for row_index, row in enumerate(self.shape):
            for col_index, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect((self.x + col_index) * CELL_SIZE, (self.y + row_index) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    if textures:
                        surface.blit(textures[self.texture_index], rect.topleft)
                    else:
                        pygame.draw.rect(surface, WHITE, rect)  # Cadangan jika tekstur tidak ditemukan

# Fungsi Game Over
def show_game_over_screen(surface, score, highscore):
    surface.fill(BLACK)
    game_over_text = LARGE_FONT.render("GAME OVER", True, WHITE)
    score_text = FONT.render(f"Your Score: {score}", True, WHITE)
    highscore_text = FONT.render(f"Highscore: {highscore}", True, WHITE)
    surface.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
    surface.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 20))
    surface.blit(highscore_text, (WIDTH // 2 - highscore_text.get_width() // 2, HEIGHT // 2 + 60))
    pygame.display.flip()

# Kelas Grid
class Grid:
    def __init__(self):
        # Membuat grid kosong (None berarti tidak ada blok di sel tersebut)
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def draw(self, surface):
        # Gambar setiap sel di grid
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if cell is not None:
                    if textures:
                        # Menggunakan tekstur jika tersedia
                        surface.blit(textures[cell], rect.topleft)
                    else:
                        # Menggunakan warna putih sebagai cadangan
                        pygame.draw.rect(surface, WHITE, rect)
                # Gambar garis grid (opsional)
                pygame.draw.rect(surface, WHITE, rect, 1)

    def place_block(self, block):
        # Menempatkan blok pada grid
        for row_index, row in enumerate(block.shape):
            for col_index, cell in enumerate(row):
                if cell:  # Jika bagian blok aktif
                    x = block.x + col_index
                    y = block.y + row_index
                    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                        self.grid[y][x] = block.texture_index

    def clear_lines(self):
        # Menghapus baris penuh dari grid
        self.grid = [row for row in self.grid if any(cell is None for cell in row)]
        # Menambahkan baris kosong di bagian atas grid
        while len(self.grid) < GRID_SIZE:
            self.grid.insert(0, [None for _ in range(GRID_SIZE)])

    def check_collision(self, block):
        # Periksa apakah balok bertabrakan dengan sesuatu
        for row_index, row in enumerate(block.shape):
            for col_index, cell in enumerate(row):
                if cell:  # Jika bagian balok aktif
                    x = block.x + col_index
                    y = block.y + row_index
                    # Periksa batas grid
                    if x < 0 or x >= GRID_SIZE or y >= GRID_SIZE:
                        return True
                    # Periksa tabrakan dengan balok lain di grid
                    if y >= 0 and self.grid[y][x] is not None:
                        return True
        return False

    def check_game_over(self):
        # Periksa apakah ada blok di baris teratas
        return any(self.grid[0][x] for x in range(GRID_SIZE))

# Fungsi utama
def main():
    clock = pygame.time.Clock()
    grid = Grid()
    block = Block()
    score = 0
    highscore = load_highscore()

    game_started = False

    while True:
        # Gambar background
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not game_started:
                    game_started = True  # Mulai game setelah tombol Enter ditekan

                # Simpan posisi sebelumnya untuk memeriksa tabrakan
                if game_started:
                    previous_x, previous_y = block.x, block.y
                    previous_shape = block.shape

                    if event.key == pygame.K_LEFT:
                        block.x -= 1
                    elif event.key == pygame.K_RIGHT:
                        block.x += 1
                    elif event.key == pygame.K_DOWN:
                        block.y += 1
                    elif event.key == pygame.K_UP:
                        # Rotasi balok searah jarum jam
                        block.shape = list(zip(*block.shape[::-1]))

                    # Kembalikan ke posisi sebelumnya jika terjadi tabrakan
                    if grid.check_collision(block):
                        block.x, block.y, block.shape = previous_x, previous_y, previous_shape

        if game_started:
            # Pergerakan otomatis ke bawah setiap frame
            block.y += 1
            if grid.check_collision(block):
                block.y -= 1
                grid.place_block(block)
                grid.clear_lines()
                score += 10
                block = Block()
                if grid.check_game_over():
                    save_highscore(max(score, highscore))  # Simpan highscore
                    show_game_over_screen(screen, score, highscore)
                    pygame.display.flip()
                    pygame.time.wait(2000)  # Memberikan waktu 2 detik sebelum permainan dimulai ulang
                    score = 0
                    grid = Grid()
                    block = Block()
                    game_started = False  # Game dimulai ulang setelah game over

            grid.draw(screen)
            block.draw(screen)
            score_text = FONT.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))
        else:
            start_text = LARGE_FONT.render("Press ENTER to Start", True, WHITE)
            screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - 50))

        pygame.display.flip()
        clock.tick(2)  # 2 frame per detik (kecepatan permainan)

# Panggil fungsi main untuk menjalankan permainan
if __name__ == "__main__":
    main()

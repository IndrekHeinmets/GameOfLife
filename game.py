import pygame
import random

pygame.init()

class Game():
    def __init__(self, width, height, tile_sz, fps, update_freq):
        self.WIDTH, self.HEIGHT = width, height
        self.TILE_SZ = tile_sz
        self.FPS = fps
        self.UPDATE_FREQ = update_freq

        self.run = True
        self.simulate = False
        self.count = 0

        self.GRID_WIDTH, self.GRID_HEIGHT = self.WIDTH // self.TILE_SZ, self.HEIGHT // self.TILE_SZ
        
        self.BLACK = (0, 0, 0)
        self.GREY = (110, 110, 110)
        self.YELLOW = (255, 255, 0)

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.screen_name = 'Game Of Life'

        self.clock = pygame.time.Clock()

        self.alive_cells = set()

    def generate(self, num):
        self.alive_cells = set([Cell((random.randrange(0, self.GRID_WIDTH), random.randrange(0, self.GRID_HEIGHT))) for _ in range(num)])

    def draw_grid(self):
        for cell in self.alive_cells:
            col, row = cell.pos
            top_left = (col * self.TILE_SZ, row * self.TILE_SZ)
            pygame.draw.rect(self.screen, self.YELLOW, (*top_left, self.TILE_SZ, self.TILE_SZ))

        for row in range(self.GRID_HEIGHT):
            pygame.draw.line(self.screen, self.BLACK, (0, row * self.TILE_SZ), (self.WIDTH, row * self.TILE_SZ))

        for col in range(self.GRID_WIDTH):
            pygame.draw.line(self.screen, self.BLACK, (col * self.TILE_SZ, 0), (col * self.TILE_SZ, self.HEIGHT))

    def get_neighbors(self, cell):
        x, y = cell.pos
        cell.neighbors.clear()
        for dx in [-1, 0, 1]:
            if x + dx < 0 or x + dx >= self.GRID_WIDTH:
                continue
            for dy in [-1, 0, 1]:
                if y + dy < 0 or y + dy >= self.GRID_HEIGHT:
                    continue
                if dx == 0 and dy == 0:
                    continue
                cell.neighbors.add(Cell((x + dx, y + dy)))

    def update_grid(self):
        new_cells = set()
        all_neighbors = set()

        for cell in self.alive_cells:
            self.get_neighbors(cell)
            all_neighbors.update(cell.neighbors)
            alive_neighbors = len([neighbor for neighbor in cell.neighbors if neighbor in self.alive_cells])
            if alive_neighbors in [2, 3]:
                new_cells.add(cell)

        for cell in all_neighbors:
            if cell not in self.alive_cells:
                self.get_neighbors(cell)
                alive_neighbors = len([neighbor for neighbor in cell.neighbors if neighbor in self.alive_cells])
                if alive_neighbors == 3:
                    new_cells.add(cell)

        self.alive_cells = new_cells

    def main(self):
        while self.run:
            self.clock.tick(self.FPS)

            if self.simulate:
                self.count += 5

            if self.count >= self.UPDATE_FREQ:
                self.count = 0
                self.update_grid()

            pygame.display.set_caption(f'{self.screen_name}: Simulating' if self.simulate else f'{self.screen_name}: Paused')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    col = x // self.TILE_SZ
                    row = y // self.TILE_SZ
                    cell = Cell((col, row))

                    for alive_cell in self.alive_cells:
                        if alive_cell == cell:
                            self.alive_cells.remove(alive_cell)
                            break
                    else:
                        self.alive_cells.add(cell)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.simulate = not self.simulate

                    if event.key == pygame.K_c:
                        self.alive_cells.clear()
                        self.simulate = False
                        self.count = 0

                    if event.key == pygame.K_g:
                        self.generate(random.randint(5, 20) * self.GRID_WIDTH)

                    if event.key == pygame.K_f:
                        self.UPDATE_FREQ -= 10

                    if event.key == pygame.K_s:
                        self.UPDATE_FREQ += 10
        
            self.screen.fill(self.GREY)
            self.draw_grid()
            pygame.display.update()
        pygame.quit()


class Cell():
    def __init__(self, pos):
        self.pos = pos
        self.neighbors = set()

    def __eq__(self, other):
        if isinstance(other, Cell):
            return self.pos == other.pos
        return False

    def __hash__(self):
        return hash(self.pos)


if __name__ == '__main__':
    WIDTH, HEIGHT = 1200, 1000
    TILE_SZ = 10
    FPS = 100
    UPDATE_FREQ = 60

    Game(WIDTH, HEIGHT, TILE_SZ, FPS, UPDATE_FREQ).main()

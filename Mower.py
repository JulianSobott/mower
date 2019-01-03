class Mower:
    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0

    def drive(self):
        self.x += 1

    def render(self, screen, pygame):
        shape = pygame.Rect(self.pos_x, self.pos_y, 500, 600)
        pygame.draw.rect(screen, (100, 100, 0), (100, 100, 100, 100))
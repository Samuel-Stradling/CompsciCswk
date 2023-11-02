import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Define colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Create a Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Finance Analysis App")

# Define a base class for all screens
class Screen:
    def __init__(self, background_color):
        self.background_color = background_color
        self.buttons = []

    def add_button(self, button):
        self.buttons.append(button)

    def render(self):
        screen.fill(self.background_color)
        for button in self.buttons:
            button.draw()

# Create a class for the home screen
class HomeScreen(Screen):
    def __init__(self):
        super().__init__(WHITE)

        # Create buttons for other screens
        self.sort_data_button = Button(100, 100, "Sort Data", BLUE)
        self.search_data_button = Button(100, 200, "Search Data", GREEN)
        self.settings_button = Button(100, 300, "Settings", GRAY)
        self.graph_button = Button(100, 400, "Graph", RED)

        self.add_button(self.sort_data_button)
        self.add_button(self.search_data_button)
        self.add_button(self.settings_button)
        self.add_button(self.graph_button)

# Create a class for other screens (Sort Data, Search Data, Settings, Graph)
class OtherScreen(Screen):
    def __init__(self, title, background_color):
        super().__init__(background_color)

        # Create a return button to go back to the home screen
        self.return_button = Button(20, 20, "Return to Home", GRAY)

        self.add_button(self.return_button)

# Create a class for buttons
class Button:
    def __init__(self, x, y, label, color):
        self.x = x
        self.y = y
        self.label = label
        self.color = color
        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render(self.label, True, (255, 255, 255))
        self.rect = self.text.get_rect(center=(self.x, self.y))

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text, self.rect)

# Initialize screens
home_screen = HomeScreen()
sort_data_screen = OtherScreen("Sort Data", BLUE)
search_data_screen = OtherScreen("Search Data", GREEN)
settings_screen = OtherScreen("Settings", GRAY)
graph_screen = OtherScreen("Graph", RED)

# Main loop
current_screen = home_screen
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == home_screen:
                if home_screen.sort_data_button.rect.collidepoint(event.pos):
                    current_screen = sort_data_screen
                elif home_screen.search_data_button.rect.collidepoint(event.pos):
                    current_screen = search_data_screen
                elif home_screen.settings_button.rect.collidepoint(event.pos):
                    current_screen = settings_screen
                elif home_screen.graph_button.rect.collidepoint(event.pos):
                    current_screen = graph_screen
            elif current_screen != home_screen and current_screen.return_button.rect.collidepoint(event.pos):
                current_screen = home_screen

    current_screen.render()
    pygame.display.flip()

pygame.quit()
sys.exit()

import pip
import pygame
from game import Game
import os

play_btn = pygame.image.load(os.path.join("game_assets/menu","button_play.png"))
logo = pygame.image.load(os.path.join("game_assets", "logo.png"))

class MainMenu:
		def __init__(self):
				self.width = 1350
				self.height = 700
				#self.window_flags = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE
				self.window_flags = 0
				self.bg = pygame.image.load(os.path.join("game_assets", "bg.png"))
				self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
				self.win = pygame.display.set_mode((self.width, self.height), self.window_flags)
				self.btn = (self.width/2 - play_btn.get_width()/2, self.height/2 - play_btn.get_height()/2, play_btn.get_width(), play_btn.get_height())
					
		def run(self):
				run = True

				while run:
						for event in pygame.event.get():
								if event.type == pygame.QUIT:
										run = False

								elif event.type == pygame.MOUSEBUTTONUP:
										#check if hit start btn
										x, y = pygame.mouse.get_pos()

										if self.btn[0] <= x <= self.btn[0] + self.btn[2]:
												if self.btn[1] <= y <= self.btn[1] + self.btn[3]:
														game = Game(self.win)
														game.run()
														del game

								elif event.type == pygame.VIDEORESIZE:
										# Handle window resizing
										screen = pygame.display.set_mode(event.size, self.window_flags)
								
								self.draw()

				pygame.quit()

		def draw(self):
				self.win.blit(self.bg, (0,0))
				self.win.blit(logo, (self.width/2 - logo.get_width()/2, 30))
				self.win.blit(play_btn,(self.btn[0], self.btn[1]))
				pygame.display.update()

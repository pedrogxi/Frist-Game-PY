# import pygame, os
# from game import *
# from game import TELA, WIDTH, BACKGROUND
# # Background
# bg = pygame.transform.scale(pygame.image.load(os.path.join("assets", "estrela1.png")), (WIDTH, HEIGHT))

# pygame.init()

# width = 1000
# i = 0

# run = True
# while run:

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False

#     TELA.fill((0,0,0))

#     #Create looping background
#     BACKGROUND.blit(bg, (i, 1))
#     bg(bg, (width+i, 1))
#     if i == -width:
#         BACKGROUND.blit(bg, (width+i, 1))
#         i = 0
#     i -= 1

#     pygame.display.update()
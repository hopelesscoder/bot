import pygame.camera
import pygame.image

pygame.camera.init()

elenco_camere = pygame.camera.list_cameras()
print "scattata foto da", elenco_camere[0]


webcam = pygame.camera.Camera(elenco_camere[0])

webcam.start()

img = webcam.get_image()

pygame.image.save(img, "photo.jpg")

pygame.camera.quit()

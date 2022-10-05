from PIL import Image
import numpy as np
import PygameEngine as pe
import sys, pygame

engine = pe.PygameEngine( "teste"
                        , 500, 500
                        , pygame.RESIZABLE
                        , pe.StretchCanvas.LARGER_BORDER )

# Exemplo usando PIL
#
#image = Image.open( "Pinguim.png" )
#
#engine.atualizarCanvasPIL( image )
#
#while True:
#    for e in pygame.event.get():
#        if e.type == pygame.QUIT: sys.exit()
#
#        engine.junelaMudouTamanho( e )
#    
#    
#    engine.atualizarJanela()

#Exemplo usando NumPy
image = np.zeros( ( 125, 250, 3 ) )
engine.atualizarCanvasNP( image )

soma = 0.01
valorTotal = 0.0

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: sys.exit()

        engine.junelaMudouTamanho( e )
    
    
    engine.atualizarJanela()

    engine.atualizarCanvasNP( image )
    if ( valorTotal <= 1.0 ):
        image = image + soma
    else:
        image[:,:,:] = 0.0
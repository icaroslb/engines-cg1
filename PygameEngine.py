import pygame
from enum import Enum

#! StretchCanvas
#  Enum para comportamento da imagem na janela
class StretchCanvas( Enum ):
    # A imagem não é esticada
    NO_STRETCH     = 1
    # A imagem é esticada até caber totalmente na janela
    FULL           = 2
    # A imagem é esticada em relação a maior borda do canvas, preservando a proporção da imagem
    LARGER_BORDER  = 3
    # A imagem é esticada em relação a menor borda do canvas, preservando a proporção da imagem
    SMALLER_BORDER = 4


#! SDLEngine
#  Classe responsável por gerenciar o SDL2
class PygameEngine:
    #_window;         # Janela
    #_surfaceScreen;  # Surface da janela, onde contém a imagem que é printada
    #_surfaceCanvas;  # Surface do canvas, copiara a imagem para o surface da janela
    #
    #_rectScreen;     # Informações de proporção da janela
    #_rectCanvas;     # Informações de proporção do canvas
    #
    #_canvas;         # Array que contém a imagem
    #_quantidadePix;  # Quantidade de pix que tem na imagem
    #
    #_scretchCanvas;  # Padrão que o canvas irá se esticar na janela

    #! PygameEngine
    #  Entrada: 
    #      nomeJanela:    Nome que a janela terá ao ser criada
    #      larguraJanela: Largura da janela
    #      alturaJanela:  Altura da janela
    #      scretchCanvas: Como a imagem se ajustará na tela
    #      flags:         flags para a janela. Os valores podem ser:
    #         pygame.FULLSCREEN    create a fullscreen display
    #           pygame.DOUBLEBUF     (obsolete in pygame 2) recommended for HWSURFACE or OPENGL
    #           pygame.HWSURFACE     (obsolete in pygame 2) hardware accelerated, only in FULLSCREEN
    #           pygame.OPENGL        create an OpenGL-renderable display
    #           pygame.RESIZABLE     display window should be sizeable
    #           pygame.NOFRAME       display window will have no border or controls
    #           pygame.SCALED        resolution depends on desktop size and scale graphics
    #           pygame.SHOWN         window is opened in visible mode (default)
    #           pygame.HIDDEN        window is opened in hidden mode
    #  Inicializa o Pygame e cria a janela que mostrará a imagem renderizada.
    def __init__ ( self, nomeJanela, larguraJanela, alturaJanela, flags = 0, scretchCanvas = StretchCanvas.NO_STRETCH ):
        pygame.init()
        self._window = pygame.display.set_mode( ( larguraJanela, alturaJanela ), flags )

        pygame.display.set_caption( nomeJanela )

        self._scretchCanvas = scretchCanvas
        self._rectCanvas = pygame.Rect( ( 0, 0 ), ( 0, 0 ) )
        self._rectWindow = self._window.get_rect()
        self._rectImagem = pygame.Rect( ( 0, 0 ), ( 0, 0 ) )
        self.imagemProporcao = self._rectImagem.copy()

##*******************************************************************
##*******************************************************************

    #! atualizarCanvasPIL
    #  Entrada: 
    #      *novoCanvas: Array com as novas cores do canvas, com cada valor variando de 0 a 1
    #  Atualiza as cores do canvas a partir de uma classe de imagem da bilioteca Pillow
    #
    def atualizarCanvasPIL ( self, novoCanvas ):
        self._canvas = pygame.image.fromstring( novoCanvas.tobytes(), novoCanvas.size, novoCanvas.mode )
        self._rectCanvas = self._canvas.get_rect()

##*******************************************************************
##*******************************************************************

    #! atualizarCanvasNP
    #  Entrada: 
    #      *novoCanvas: Array com as novas cores do canvas, com cada valor variando de 0 a 1
    #  Atualiza as cores do canvas a partir de um array numpy
    #
    def atualizarCanvasNP ( self, novoCanvas ):
        self._canvas = pygame.surfarray.make_surface( novoCanvas )
        self._rectCanvas = self._canvas.get_rect()

##*******************************************************************
##*******************************************************************

    #! mudarStretch
    #  Entrada: 
    #      scretch: Nova regra de stretch
    #  Muda a regra de stretch
    #
    def mudarStretch ( self, scretch ):
        self._scretchCanvas = scretch

##*******************************************************************
##*******************************************************************

    #! junelaMudouTamanho
    #  Verifica se houve algum evento de mudança de tamanho da janela e atualiza as informações da surface da janela caso haja o evento
    #      e: SDL_Event que informará se houve o evento de mudança de tamanho da janela
    #
    def junelaMudouTamanho ( self, e ):
        if e.type == pygame.VIDEORESIZE:
            # There's some code to add back window content here.
            self.window = pygame.display.set_mode( ( e.w, e.h )
                                                 , pygame.RESIZABLE )
            self._rectWindow = self._window.get_rect()

##*******************************************************************
##*******************************************************************

    #! atualizarProporcaoImagem
    #  Calcula as proporções da imagem
    #
    def atualizarProporcaoImagem ( self ):
        rectScreen = pygame.display.get_surface().get_rect()
        rectCanvas = self._canvas.get_rect()

        if ( self._scretchCanvas == StretchCanvas.NO_STRETCH ):
            self._rectImagem = rectCanvas
        elif ( self._scretchCanvas == StretchCanvas.FULL ):
            self._rectImagem = rectScreen
        elif ( self._scretchCanvas == StretchCanvas.SMALLER_BORDER ):
            if ( rectCanvas.w < rectCanvas.h ):   self.stretchProporcaoLargura( self._rectImagem )
            elif ( rectCanvas.w > rectCanvas.h ): self.stretchProporcaoAltura( self._rectImagem )
            else:                                 self._rectImagem = rectCanvas
        elif ( self._scretchCanvas == StretchCanvas.LARGER_BORDER ):
            if ( rectCanvas.w > rectCanvas.h ):   self.stretchProporcaoLargura( self._rectImagem )
            elif ( rectCanvas.w < rectCanvas.h ): self.stretchProporcaoAltura( self._rectImagem )
            else:                                 self._rectImagem = rectCanvas
        
        self.imagemProporcao = self._rectImagem.copy()

##*******************************************************************
##*******************************************************************

    #! atualizarJanela
    #  Atualiza a janela
    #
    def atualizarJanela ( self ):
        self._window.fill( ( 0.0, 0.0, 0.0 ) )
        
        self.atualizarProporcaoImagem()
        self._window.blit( pygame.transform.scale( self._canvas, self._rectImagem.size )
                         , self._rectImagem )
        
        pygame.display.update()

##*******************************************************************
##*******************************************************************

    #! stretchProporcaoLargura
    #  Preenche as informações de largura e altura do SDL_Rect para que a imagem preencha toda a largura sem perder a proporção
    #      rectScreen: O SDL_Rect que será preenchido
    def stretchProporcaoLargura ( self, rectStretch ):
        rectStretch.w = self._rectWindow.w
        rectStretch.h = ( self._rectWindow.w * self._rectCanvas.h ) / self._rectCanvas.w

##*******************************************************************
##*******************************************************************

    #! stretchProporcaoAltura
    #  Preenche as informações de largura e altura do SDL_Rect para que a imagem preencha toda a altura sem perder a proporção
    #      rectScreen: O SDL_Rect que será preenchido
    def stretchProporcaoAltura ( self, rectStretch ):
        rectStretch.w = ( self._rectWindow.h * self._rectCanvas.w ) / self._rectCanvas.h
        rectStretch.h = self._rectWindow.h
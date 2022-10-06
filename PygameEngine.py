import pygame
from enum import Enum

##
# \file PygameEngine.py
# \brief Engine em python
# 
# Engine em python utilizando Pygame

##
# \package PygameEngine
# 
# Pacote de gerenciamento Pygame


##
# \brief Enum utilizado na janela
#
# Enum para comportamento da imagem na janela
class StretchCanvas( Enum ):
    ## A imagem não é esticada
    NO_STRETCH     = 1
    ## A imagem é esticada até caber totalmente na janela
    FULL           = 2
    ## A imagem é esticada em relação a maior borda do canvas, preservando a proporção da imagem
    LARGER_BORDER  = 3
    ## A imagem é esticada em relação a menor borda do canvas, preservando a proporção da imagem
    SMALLER_BORDER = 4


##
# \brief Gerencia o Pygame
#
# Classe responsável por gerenciar o Pygame
class PygameEngine:

    ##
    # Inicializa o Pygame e cria a janela que mostrará a imagem renderizada.
    #
    # \param self Ponteiro do objeto
    # \param nomeJanela:    Nome que a janela terá ao ser criada
    # \param larguraJanela: Largura da janela
    # \param alturaJanela:  Altura da janela
    # \param flags:         flags para a janela. Os valores podem ser:
    # \n pygame.FULLSCREEN    create a fullscreen display
    # \n pygame.DOUBLEBUF     (obsolete in pygame 2) recommended for HWSURFACE or OPENGL
    # \n pygame.HWSURFACE     (obsolete in pygame 2) hardware accelerated, only in FULLSCREEN
    # \n pygame.OPENGL        create an OpenGL-renderable display
    # \n pygame.RESIZABLE     display window should be sizeable
    # \n pygame.NOFRAME       display window will have no border or controls
    # \n pygame.SCALED        resolution depends on desktop size and scale graphics
    # \n pygame.SHOWN         window is opened in visible mode (default)
    # \n pygame.HIDDEN        window is opened in hidden mode
    # \param scretchCanvas: Como a imagem se ajustará na tela. Os valores podem ser:
    # \n StretchCanvas.NO_STRETCH
    # \n StretchCanvas.FULL
    # \n StretchCanvas.LARGER_BORDER
    # \n StretchCanvas.SMALLER_BORDER
    def __init__ ( self, nomeJanela, larguraJanela, alturaJanela, flags = 0, scretchCanvas = StretchCanvas.NO_STRETCH ):
        pygame.init()
        self._window = pygame.display.set_mode( ( larguraJanela, alturaJanela ), flags )

        pygame.display.set_caption( nomeJanela )

        self._scretchCanvas = scretchCanvas
        self._rectCanvas = pygame.Rect( ( 0, 0 ), ( 0, 0 ) )
        self._rectWindow = self._window.get_rect()
        self._rectImagem = pygame.Rect( ( 0, 0 ), ( 0, 0 ) )
        self.imagemProporcao = self._rectImagem.copy()
        self._canvas = None

    ## 
    # Atualiza as cores do canvas a partir de uma classe de imagem da bilioteca Pillow 
    #
    # \param self Ponteiro do objeto
    # \param novoCanvas Array com as novas cores do canvas, com cada valor variando de 0 a 255
    def atualizarCanvasPIL ( self, novoCanvas ):
        if ( self._canvas != None ):
            del self._canvas
        
        self._canvas = pygame.image.fromstring( novoCanvas.tobytes(), novoCanvas.size, novoCanvas.mode )
        rectCanvasAnterior = self._rectCanvas.copy()
        self._rectCanvas = self._canvas.get_rect()
        
        if ( rectCanvasAnterior.w != self._rectCanvas.w
        or   rectCanvasAnterior.h != self._rectCanvas.h ):
            self.atualizarProporcaoImagem()

    ##
    #  Atualiza as cores do canvas a partir de um array numpy
    #
    # \param self Ponteiro do objeto
    # \param novoCanvas: Array com as novas cores do canvas, com cada valor variando de 0 a 1
    def atualizarCanvasNP ( self, novoCanvas ):
        if ( self._canvas != None ):
            del self._canvas
        
        self._canvas = pygame.surfarray.make_surface( novoCanvas * 255 )
        rectCanvasAnterior = self._rectCanvas.copy()
        self._rectCanvas = self._canvas.get_rect()
        
        if ( rectCanvasAnterior.w != self._rectCanvas.w
        or   rectCanvasAnterior.h != self._rectCanvas.h ):
            self.atualizarProporcaoImagem()

    ##
    #  Muda a regra de stretch
    #
    # \param self Ponteiro do objeto
    # \param Nova regra de stretch
    def mudarStretch ( self, scretch ):
        self._scretchCanvas = scretch
        self.atualizarProporcaoImagem()

    ##
    # Verifica se houve algum evento de mudança de tamanho da janela e atualiza as informações da surface da janela caso haja o evento
    #
    # \param self Ponteiro do objeto
    # \param event: SDL_Event que informará se houve o evento de mudança de tamanho da janela
    def junelaMudouTamanho ( self, event ):
        if event.type == pygame.VIDEORESIZE:
            # There's some code to add back window content here.
            self.window = pygame.display.set_mode( ( event.w, event.h )
                                                 , pygame.RESIZABLE )
            self._rectWindow = self._window.get_rect()
            self.atualizarProporcaoImagem()

    ##
    #  Calcula as proporções da imagem
    #
    # \param self Ponteiro do objeto
    def atualizarProporcaoImagem ( self ):
        if ( self._canvas != None ):
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

    ##
    #  Atualiza a janela
    #
    # \param self Ponteiro do objeto
    def atualizarJanela ( self ):
        self._window.fill( ( 0.0, 0.0, 0.0 ) )
        
        imgRect = self._rectImagem.copy()
        if ( self._canvas != None ):
            self._window.blit( pygame.transform.scale( self._canvas, imgRect.size )
                             , imgRect )
        
        pygame.display.update()

    ##
    # Preenche as informações de largura e altura do Rect para que a imagem preencha toda a largura sem perder a proporção
    #
    # \param self Ponteiro do objeto
    # \param rectScreen: O Rect que será preenchido
    def stretchProporcaoLargura ( self, rectStretch ):
        rectStretch.w = self._rectWindow.w
        rectStretch.h = ( self._rectWindow.w * self._rectCanvas.h ) / self._rectCanvas.w

    ##
    #  Preenche as informações de largura e altura do Rect para que a imagem preencha toda a altura sem perder a proporção
    #
    # \param self Ponteiro do objeto
    # \param rectScreen: O Rect que será preenchido
    def stretchProporcaoAltura ( self, rectStretch ):
        rectStretch.w = ( self._rectWindow.h * self._rectCanvas.w ) / self._rectCanvas.h
        rectStretch.h = self._rectWindow.h
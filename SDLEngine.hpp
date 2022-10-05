#ifndef SDL_ENGINE_HPP
#define SDL_ENGINE_HPP

#include <iostream>
#include <cstring>

#include <SDL2/SDL.h>

#if SDL_BYTEORDER == SDL_BIG_ENDIAN
    #define R_MASK 0xff000000
    #define G_MASK 0x00ff0000
    #define B_MASK 0x0000ff00
    #define A_MASK 0x000000ff
#else
    #define R_MASK 0x000000ff
    #define G_MASK 0x0000ff00
    #define B_MASK 0x00ff0000
    #define A_MASK 0xff000000
#endif

#define SHIFT_RED   << 0
#define SHIFT_GREEN << 8
#define SHIFT_BLUE  << 16

//*******************************************************************
//*******************************************************************

/*! StretchCanvas
**  Enum para comportamento da imagem na janela
*/
enum class StretchCanvas
{
    // A imagem não é esticada
    NO_STRETCH,
    // A imagem é esticada até caber totalmente na janela
    FULL,
    // A imagem é esticada em relação a maior borda do canvas, preservando a proporção da imagem
    LARGER_BORDER,
    // A imagem é esticada em relação a menor borda do canvas, preservando a proporção da imagem
    SMALLER_BORDER
};

//*******************************************************************
//*******************************************************************

/*! SDLEngine
**  Classe responsável por gerenciar o SDL2
*/
class SDLEngine {
    SDL_Window *_window;          // Janela
    SDL_Surface *_surfaceScreen;  // Surface da janela, onde contém a imagem que é printada
    SDL_Surface *_surfaceCanvas;  // Surface do canvas, copiara a imagem para o surface da janela

    SDL_Rect *_rectScreen;        // Informações de proporção da janela
    SDL_Rect *_rectCanvas;        // Informações de proporção do canvas
    SDL_Rect _imagem;             // Informações de proporção da imagem

    uint *_canvas;                // Array que contém a imagem
    uint _quantidadePix;          // Quantidade de pix que tem na imagem

    StretchCanvas _scretchCanvas; // Padrão que o canvas irá se esticar na janela

public:
    SDL_Rect imagemTamanho;       // Informações de proporção da imagem

    /*! SDLEngine
    **  Entrada: 
    **      nomeJanela:    Nome que a janela terá ao ser criada
    **      larguraJanela: Largura da janela
    **      alturaJanela:  Altura da janela
    **      larguraCanvas: Largura do canvas
    **      alturaCanvas:  Altura do canvas
    **      scretchCanvas: Como a imagem se ajustará na tela
    **      flags:         flags para a janela. Os valores podem ser:
    *          ::SDL_WINDOW_FULLSCREEN, ::SDL_WINDOW_OPENGL, ::SDL_WINDOW_HIDDEN, ::SDL_WINDOW_BORDERLESS, ::SDL_WINDOW_RESIZABLE, ::SDL_WINDOW_MAXIMIZED, ::SDL_WINDOW_MINIMIZED, ::SDL_WINDOW_INPUT_GRABBED, ::SDL_WINDOW_ALLOW_HIGHDPI, ::SDL_WINDOW_VULKAN.
    **  Inicializa o SDL e cria a janela que mostrará a imagem renderizada.
    */
    SDLEngine( const char *nomeJanela
             , uint larguraJanela, uint alturaJanela
             , uint larguraCanvas, uint alturaCanvas
             , uint flags = SDL_WINDOW_SHOWN
             , StretchCanvas scretchCanvas = StretchCanvas::NO_STRETCH );
    
    /*! ~SDLEngine
    **  Destroi o objeto, liberando a memória e desligando o SDL.
    */
    ~SDLEngine ();

    /*! atualizarCanvas
    **  Entrada: 
    **      *novoCanvas: Array com as novas cores do canvas, com cada valor variando de 0 a 1
    **  Atualiza as cores do canvas
    */
    template <class T>
    void atualizarCanvas ( T *novoCanvas );

    /*! mudarStretch
    **  Entrada: 
    **      scretch: Nova regra de stretch
    **  Muda a regra de stretch
    */
    void mudarStretch (StretchCanvas scretch);

    /*! mudarCanvas
    **  Entrada: 
    **      novaLargura: Nova lagura do canvas
    **      novaAltura: Nova altura do canvas
    **  Muda as proporções do canvas
    */
    void mudarCanvas ( uint novaLargura, uint novaAltura );

    /*! junelaMudouTamanho
    **  Verifica se houve algum evento de mudança de tamanho da janela e atualiza as informações da surface da janela caso haja o evento
    **      e: SDL_Event que informará se houve o evento de mudança de tamanho da janela
    */
    void junelaMudouTamanho ( const SDL_Event &e );

    /*! atualizarJanela
    **  Atualiza a janela
    */
    void atualizarJanela ();

private:
    
    /*! stretchProporcaoLargura
    **  Preenche as informações de largura e altura do SDL_Rect para que a imagem preencha toda a largura sem perder a proporção
    */
    void stretchProporcaoLargura ();

    /*! stretchProporcaoAltura
    **  Preenche as informações de largura e altura do SDL_Rect para que a imagem preencha toda a altura sem perder a proporção
    */
    void stretchProporcaoAltura ();

    /*! stretchProporcaoAltura
    **  Calcula as proporções da imagem
    */
    void atualizarProporcaoImagem ();

    /*! copiarCanvas
    **  Faz a cópia da imagem do canvas para a janela de acordo com a regra de stretch indicada
    */
    void copiarCanvas ();

    /*! obterJanelaSurface
    **  Atualiza as informações do surface da janela
    */
    void atualizarJanelaSurface ();
};


//*******************************************************************
//*******************************************************************

SDLEngine::SDLEngine( const char *nomeJanela
                    , uint larguraJanela, uint alturaJanela
                    , uint larguraCanvas, uint alturaCanvas
                    , uint flags
                    , StretchCanvas scretchCanvas )
: _canvas( nullptr )
, _scretchCanvas( scretchCanvas )
{
    if ( SDL_Init( SDL_INIT_VIDEO ) < 0 )
    {
        std::cerr << "SDL não conseguiu inicializar! SDL_Error: " << SDL_GetError() << std::endl;
    }
    else
    {
        _window = SDL_CreateWindow( nomeJanela
                                 , SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED
                                 , larguraJanela, alturaJanela
                                 , flags );
        if ( _window == nullptr )
        {
            std::cerr << "Não foi possível criar a janela! SDL_Error: " << SDL_GetError() << std::endl;
        }
        else
        {
            atualizarJanelaSurface();

            mudarCanvas( larguraCanvas, alturaCanvas );

            mudarStretch( _scretchCanvas );
        }
    }
}

//*******************************************************************
//*******************************************************************

SDLEngine::~SDLEngine ()
{
    SDL_FreeSurface( _surfaceScreen );
    SDL_FreeSurface( _surfaceCanvas );
    SDL_DestroyWindow( _window );
    SDL_Quit();

    if ( _canvas != nullptr)
        delete [] _canvas;
}

//*******************************************************************
//*******************************************************************

template <class T>
void SDLEngine::atualizarCanvas ( T *novoCanvas )
{
    for ( int i = 0; i < _quantidadePix; i++ )
    {
        _canvas[i] = ( ( (uint)( novoCanvas[( i * 3 )]     * T( 255 ) ) SHIFT_RED )   & R_MASK )
                   + ( ( (uint)( novoCanvas[( i * 3 ) + 1] * T( 255 ) ) SHIFT_GREEN ) & G_MASK )
                   + ( ( (uint)( novoCanvas[( i * 3 ) + 2] * T( 255 ) ) SHIFT_BLUE )  & B_MASK )
                   + A_MASK;
    }

    copiarCanvas();
}

//*******************************************************************
//*******************************************************************

void SDLEngine::mudarStretch (StretchCanvas scretch)
{
    _scretchCanvas = scretch;
    SDL_FillRect( _surfaceScreen, nullptr, A_MASK );
    copiarCanvas();
}

//*******************************************************************
//*******************************************************************

void SDLEngine::mudarCanvas ( uint novaLargura, uint novaAltura )
{
    if ( _canvas != nullptr )
    {
        SDL_FreeSurface( _surfaceCanvas );
        delete [] _canvas;
    }

    _quantidadePix = novaLargura * novaAltura;

    _canvas = new uint[_quantidadePix];
    _surfaceCanvas = SDL_CreateRGBSurfaceFrom( _canvas
                                             , novaLargura, novaAltura
                                             , 32, 4 * novaLargura
                                             , R_MASK, G_MASK, B_MASK, A_MASK );
    _rectCanvas = &( _surfaceCanvas->clip_rect );
}

//*******************************************************************
//*******************************************************************

void SDLEngine::atualizarJanela ()
{
    SDL_UpdateWindowSurface( _window );
}

//*******************************************************************
//*******************************************************************

void SDLEngine::junelaMudouTamanho ( const SDL_Event &e )
{
    if ( e.type == SDL_WINDOWEVENT )
    {
        if (e.window.event == SDL_WINDOWEVENT_RESIZED)
        {
            atualizarJanelaSurface();
            SDL_FillRect( _surfaceScreen, nullptr, A_MASK );
            copiarCanvas();
        }
    }
}

//*******************************************************************
//*******************************************************************

void SDLEngine::stretchProporcaoLargura ()
{
    _imagem.w = _rectScreen->w;
    _imagem.h = ( _rectScreen->w * _rectCanvas->h ) / _rectCanvas->w;
}

//*******************************************************************
//*******************************************************************

void SDLEngine::stretchProporcaoAltura ()
{
    _imagem.w = ( _rectScreen->h * _rectCanvas->w ) / _rectCanvas->h;
    _imagem.h = _rectScreen->h;
}

//*******************************************************************
//*******************************************************************

void SDLEngine::atualizarProporcaoImagem ()
{
    switch ( _scretchCanvas )
    {
        case StretchCanvas::NO_STRETCH:
            _imagem = *_rectCanvas;
            break;
        case StretchCanvas::FULL:
            _imagem = *_rectScreen;
            break;
        case StretchCanvas::SMALLER_BORDER:
            if ( _rectCanvas->w < _rectCanvas->h )      stretchProporcaoLargura();
            else if ( _rectCanvas->w > _rectCanvas->h ) stretchProporcaoAltura();
            else                                        _imagem = *_rectScreen;
            
            break;
        case StretchCanvas::LARGER_BORDER:
            if ( _rectCanvas->w > _rectCanvas->h )      stretchProporcaoLargura();
            else if ( _rectCanvas->w < _rectCanvas->h ) stretchProporcaoAltura();
            else                                        _imagem = *_rectScreen;
            
            break;
    }

    imagemTamanho = _imagem;
}

//*******************************************************************
//*******************************************************************

void SDLEngine::copiarCanvas ()
{
    atualizarProporcaoImagem();
    
    if ( _scretchCanvas == StretchCanvas::NO_STRETCH )
        SDL_BlitSurface( _surfaceCanvas, nullptr, _surfaceScreen, &_imagem );
    else
        SDL_BlitScaled( _surfaceCanvas, nullptr, _surfaceScreen, &_imagem );
    
}

void SDLEngine::atualizarJanelaSurface ()
{
    _surfaceScreen = SDL_GetWindowSurface( _window );
    _rectScreen = &(_surfaceScreen->clip_rect);
}

#endif
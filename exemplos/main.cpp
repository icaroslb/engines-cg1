#include "../SDLEngine.h"

#define LARGURA_TELA 500
#define ALTURA_TELA  500
#define LARGURA_CANVAS 125
#define ALTURA_CANVAS  250

int main ( void )
{
    SDLEngine sdlEngine{ "Teste"
                       , LARGURA_TELA, ALTURA_TELA
                       , LARGURA_CANVAS, ALTURA_CANVAS
                       };
    float testeArray[LARGURA_CANVAS * ALTURA_CANVAS * 3];

    SDL_Event e;
    bool quit = false;
    bool teste = true;
    int testeNum = 0; 

    for ( int i = 0; i < LARGURA_CANVAS * ALTURA_CANVAS * 3; i++ )
        testeArray[i] = 0.0f;
    
    while (!quit)
    {
        while( SDL_PollEvent( &e ) )
        {
            if( e.type == SDL_QUIT )
                quit = true;
        }

        sdlEngine.atualizarCanvas( testeArray );
        sdlEngine.atualizarJanela();

        for ( int i = 0; i < LARGURA_CANVAS * ALTURA_CANVAS * 3; i++ )
            testeArray[i] += 0.01f;
        
        testeNum = ( testeNum + 1 ) % 100;
    }

    
    return 0;
}
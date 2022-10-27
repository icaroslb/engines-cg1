# engines-cg1

Engine criada para a cadeira CK0245 - COMPUTAÇÃO GRÁFICA I.

As engines foram criadas utilizando as bibliotecas <a href='https://www.libsdl.org/'>SDL2</a> para C++, no arquivo _SDLEngine.hpp_ e <a href='https://www.pygame.org/'>Pygame</a> para Python, no arquivo _PygameEngine.py_.

Na pasta _exemplos_ possui exemplos de como utilizar as engines.

A documentação dos arquivos _SDLEngine.hpp_ e _PygameEngine.py_ estão disponível <a href='https://icaroslb.github.io/engines-cg1/'>aqui</a>.

Para compilar o teste em c++ utilize a linha:
- g++ main.cpp -o main -lSDL2

Para rodar o teste em python, coloque os arquivos _main.py_, _PygameEngine.py_ e _Pinguim.png_ na mesma pasta e utilize a linha:
- python3 main.py
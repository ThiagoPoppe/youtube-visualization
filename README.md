# youtube-visualization
Repositório para o trabalho final de Visualização de Dados

## Onde encontrar os dados
Os dados foram baixados diretamente do site Kaggle, podendo ser encontrados através desse [link](https://www.kaggle.com/datasnaek/youtube-new).

## Pré-processamento dos dados
Execute o script ``preprocess.py`` passando como parâmetro o caminho para a pasta que contém os dados ``.csv`` e ``.json``.

Esse script irá adicionar as informações das categorias e padronizará as datas para um formato de datetime. Além disso, os dados processados serão salvos na pasta ``processed/``, que poderá ser encontrada sobre o mesmo caminho o mesmo informado anteriormente.


Uma execução válida desse script pode ser vista a seguir:
```bash
python preprocess.py --datapath /path/to/youtube/data
```
No caso do exemplo acima, os dados pré-processados estarão localizados no caminho ``/path/to/youtube/data/processed/``.
# youtube-visualization
Repositório para o trabalho final de Visualização de Dados

## Onde encontrar os dados
Os dados foram baixados diretamente do site Kaggle, podendo ser encontrados através desse [link](https://www.kaggle.com/datasnaek/youtube-new).

Os dados processados podem ser acessados via o seguinte link para o drive: https://drive.google.com/drive/folders/1I14Dj4t3ICVpEe2U8rt9bASyJdJ2jbK7?usp=sharing.

## Configuração do ambiente
Utilize o arquivo ``requirements.txt`` para instalar todas as dependências necessárias através do comando:
```bash
pip install -r requirements.txt
```

## Pré-processamento dos dados
Caso deseje processar os dados localmente ao invés de já baixar eles pré-processados, execute o script ``preprocess.py`` passando como parâmetro o caminho para a pasta que contém os dados ``.csv`` e ``.json``.

Esse script irá adicionar as informações das categorias e padronizará as datas para um formato de datetime sem a informação do horário. Além disso, os dados processados serão salvos na pasta ``processed/``.


Uma execução válida desse script pode ser vista a seguir:
```bash
python preprocess.py --datapath /path/to/youtube/data
```
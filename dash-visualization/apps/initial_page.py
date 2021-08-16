import dash_html_components as html

layout = html.Div([
    html.H3('Projeto Final - Visualização de Dados'),
    html.Div([
        html.P('Esse é um projeto da disciplina de Visualização de Dados (DCC030). O objetivo desse trabalho é demonstrar parte dos conhecimentos adquiridos em sala de aula, demonstrando que podemos criar visualizações sobre um conjunto de dados de uma forma atrativa e analítica.'),
        html.P([
            'Os dados escolhidos pelo grupo foi de trendings (vídeos Em Alta) do YouTube, disponibilizados pelo site ',
            html.A('Kaggle', href = 'https://www.kaggle.com/datasnaek/youtube-new',  className='link_texto'),
            '. O nosso objetivo com esses dados era de ajudar criadores de conteúdo e novos ingressantes da plataforma em identificar "padrões" que possam auxiliar no crescimento do seu canal. Buscavamos também ter um entendimento mais profundo de como que as métricas da plataforma impactam diretamente no sucesso de um conteúdo publicado por um criador. E, além disso, queriamos entender de forma simplificada, como que o algoritmo de "seleção" do YouTube funciona, isto é, como que o algoritmo julga um conteúdo ser bom ou ruim para que ele possa ser encaminhado para a área dos vídeos "Em Alta".'
        ]),
        html.P([
            'Para sermos mais objetivos nas análises, decidimos restringir a base apenas para os vídeos de um país especifico (Estados Unidos), reduzindo assim consideravelmente o tempo necessário para gerar as visualizações de uma forma bem feita.'
        ]),
        html.P([
            'Escolha um dos possíveis links ao lado para entrar nas páginas das visualizações.'
        ]),
    ], className='texto_home'),
])
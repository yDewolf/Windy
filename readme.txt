# Resumo do Projeto / Sistema:
O Windy é um sistema de venda de jogos baseado na Steam feito em Python. O sistema tem sistema de Login, Publicação de jogos e algumas outras coisas.

# Principais Features Almejadas:
- Compra e venda de jogos | X
- Sistema de Login e criação de contas | X
- Interface aceitável | X

## Outras Features Almejadas:
- Configurações de conta: 
    - Lembrar a conta | X
    - Mudar nome de usuário
    - Mudar senha | X
    - Se tornar desenvolvedor | X
    - Deletar conta | X

- Avaliação de jogos (Texto e também 0 à 10)


## Outros objetivos do projeto:
- Evitar usar bibliotecas ou códigos externos | X
- Criar componentes que possam ser utilizados em outros projetos | X
- Criar um sistema de leitura de arquivos csv para armazenar dados | X
- Criar um sistema modular de Menus no console 
(é possível encontrar as classes Menu e Form, em MenuManager.py, foi um dos métodos que pensei para criar esse sistema de menus)

# Algumas curiosidades sobre o Projeto:

- O projeto foi nomeado de "Windy" (Ventoso) como uma inspiração do nome "Steam" (Vapor)
- O nome "Windy" ou "Ventoso", em português, também tem o significado de algo que é um tanto caótico, mas ao mesmo tempo previsível. Na minha opinião, isso define bem o projeto.
- A média de tempo que eu gastei trabalhando nesse projeto foi umas 22+ horas

- A maior parte das ideias para o projeto eu tive enquanto tomava banho
- O projeto não teve um grande planejamento, partiu de uma ideia um tanto simples (Criar algo próximo à Steam) e, devido à falta de planejamento, acabou tendo um escopo um pouco grande, o qual não pôde ser totalmente concluído.

- O controle de foco foi feito majoritáriamente pelo Whatsapp, onde eu me mandava uma lista de prioridade do que devia ser feito primeiro e depois fazia:

(Sexta-feira 30/09/24)
"coisas para implementar hj
    - Sistema de sessão: a sessão é criada quando vc abre o programa. A sessão armazena dados como: em que conta tá logado, se está online e a biblioteca
    - DataHolder (Substituição do FakeDatabase): segura dados como os usuários apenas qnd vai logar e dps descarta. Mantém dados dos jogos enquanto navega pelo menu para evitar lag

*Lista de prioridade para terminar o sistema:*
    1. Compra de jogos
    2. Poder olhar a biblioteca
    3. Configurações da conta (Poder remover a conta, manter logado, modificar para conta de desenvolvedor)
    4. Poder publicar jogos (se a conta for de desenvolvedor)
    5. PrintFramework e MenuFramework"

# Opiniões pessoais sobre o projeto:

Foi um projeto até que bem desenvolvido, obviamente poderia ter sido melhor planejado e mais organizado, principalmente na forma que os menus são construídos (dá até medo olhar o main.py).
Ainda que possa ter sido melhor desenvolvido, acredito que foi uma experiência interessante, perceber durante a criação do projeto coisas que eu não tinha pensado quando tive a ideia inicial me fez valorizar mais o planejamento.
Olhando por cima, não parece ser um sistema com muitas features e, realmente, não tem muitas features mesmo, mas a maior parte das que tem funcionam muito bem (não estou considerando os menus).
A última coisa que eu tenho a dizer é que se eu fosse melhorar esse sistema, provavelmente teria que recomeçar ele do zero, já que muita coisa acaba sendo um pouco confusa, como:
- Não tem um padrão sobre como as informações do usuário é tratada, se você não sabe como usar, você vai demorar um pouco para entender já que ao invés de usar classes, eu usei mais dicionários, onde você pode inserir qualquer informação, com chaves erradas e etc. Isso provavelmente seria evitado com o uso de classes
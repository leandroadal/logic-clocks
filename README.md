# Logic clocks - Lamport

## Description

- Projeto da disciplina de Sistemas Distribuídos que tem por objetivo mostra o funcionamento do algoritmo de Lamport em relógios lógicos.
- O projeto usa o `gRPC` como forma de comunicação.
- Em `clock_server` o servidor é "ligado"
- `update_time_service` herda do service do gRPC sendo responsável por fazer a verificação do tempo logico do relógio.

## Rodando o projeto

Para o roda o programa é simples:

- 1 - Executar o clock_server em dois ou mais terminais (em três para testar o padrão)
- 2 - Adicionar uma porta para o servidor e adicionar os peers/as portas dos outros servidores criados
- 3 - Definir a quantidade de requisições a serem feita aos outros peers.

import random
import time
from concurrent import futures
import grpc

import logic_clock_pb2
import logic_clock_pb2_grpc
import update_time_service


def conf_server():
    while True:
        standard = input('Deseja usar uma configuração pre-definida '
                         'para a porta do servidor e seus pares? S / N: ')
        if standard == 'S' or standard == 's':
            id = int(input('Digite o ID (de 1 a 3) do servidor: '))
            servers = {
                1: {'port': 50051, 'peers': [50052, 50053]},
                2: {'port': 50052, 'peers': [50051, 50053]},
                3: {'port': 50053, 'peers': [50052, 50051]}
            }
            if 0 < id < 4:
                port = servers[id]['port']
                peers = servers[id]['peers']
                return id, port, peers
            else:
                print('Erro! Digite um ID entre 1 e 3')
        elif standard == 'N' or standard == 'n':
            id = int(input('Digite o ID do servidor: '))
            port = int(input('Digite a porta do servidor: '))
            qt = int(input('Digite a quantidade de peers: '))

            peers = []
            for i in range(qt):
                p = int(input(f'{i + 1} peer: '))
                peers.append(p)
            return id, port, peers
        else:
            print('Erro! Digite S para usar uma configuração padrão e N pada definir uma própria')


# Definindo o servidor gRPC
def up_server(id, port, peers):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    logic = update_time_service.LogicalTime(id)
    logic_clock_pb2_grpc.add_LogicalTimeServicer_to_server(logic, server)
    server.add_insecure_port(f'[::]:{str(port)}')
    server.start()
    print(f'Servidor: {id}, iniciado na porta: {port}\n')
    menu_server(logic, port, peers)


def menu_server(logic, port, peer):
    stubs = get_stubs(port, peer)
    try:
        while True:
            amount = int(input('Digite quantas requisições devem ser feitas: '))
            random_request(logic, stubs, amount)
    except KeyboardInterrupt:
        print('\n')
        print('Encerando o Servidor!')


def get_stubs(port, peers):
    """ Cria um canal com métodos do serviço de cada peer """
    stubs = {}
    for peer in peers:
        if peer != port:
            channel = grpc.insecure_channel(f'localhost:{str(peer)}')
            stub = logic_clock_pb2_grpc.LogicalTimeStub(channel)
            stubs[peer] = stub
    return stubs


def random_request(logic, stubs, amount):
    """ Faz uma requisição a um peer aleatório """
    for i in range(amount):
        try:
            random_server = random.choice(list(stubs.items()))  # Escolhe um peer aleatório
            port, stub = random_server
            ran = random.randint(3, 5)
            time.sleep(ran)  # Para visualizar melhor a troca de mensagem entre os pares
            logic.clock += 1  # Adicionando 1 antes de enviar a mensagem
            print(f'Se comunicando com o processo que está na porta: {port}! Tempo lógico atual: {logic.clock}')
            stub.update_time_logical(logic_clock_pb2.Request(logical_time=logic.clock, sender_port=port))
        except grpc.RpcError:
            print(f'Erro ao comunicar com o processo que está na porta: {port}!')


if __name__ == '__main__':
    serv_id, serv_port, serv_peers = conf_server()
    up_server(serv_id, serv_port, serv_peers)

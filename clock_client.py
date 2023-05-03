import grpc
import logic_clock_pb2
import logic_clock_pb2_grpc


def run_client():
    # Conectando ao servidor grpc no localhost
    channel = grpc.insecure_channel('localhost:50051')

    # Criando o stub do serviço gRPC
    stub = logic_clock_pb2_grpc.LogicalTimeStub(channel)

    # Relógio lógico deve ser incrementado a cada mensagem enviada ou recebida
    logic_clock = 0

    # Enviando mensagens e atualizando o relógio lógico
    for i in range(3):
        # Adicionado um ao tempo lógico já que iremos enviar uma mensagem
        logic_clock += 1
        print(f'Tempo Lógico Atual: {logic_clock}')

        # Enviando a mensagem e recebendo a resposta do servidor
        response = stub.update_time_logical(logic_clock_pb2.Request(logical_time=logic_clock))

        # Apenas para torna grafico quando o relógio está desatualizado
        if response.logical_time > logic_clock:
            print('Detectada inconsistência no relógio local')

        # Atualizando o relógio lógico local com base no maior valor entre a resposta do servidor e o valor local
        logic_clock = max(logic_clock, response.logical_time) + 1

        # Imprimindo o tempo lógico atualizado
        print(f'Tempo Lógico atualizado: {logic_clock}')


if __name__ == '__main__':
    run_client()

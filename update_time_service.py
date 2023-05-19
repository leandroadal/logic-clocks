import logic_clock_pb2
import logic_clock_pb2_grpc


class LogicalTime(logic_clock_pb2_grpc.LogicalTimeServicer):
    def __init__(self, id):
        self.id = id
        self.clock = 0

    def update_time_logical(self, request, context):
        sender_port = request.sender_port
        # Atualizando o relógio lógico com base no tempo lógico da mensagem recebida e na atual
        self.clock = max(self.clock, request.logical_time) + 1
        print(f'Tempo logico após receber a mensagem de {sender_port}: {self.clock}')

        return logic_clock_pb2.Response()

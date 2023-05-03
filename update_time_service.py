import logic_clock_pb2
import logic_clock_pb2_grpc


class LogicalTime(logic_clock_pb2_grpc.LogicalTimeServicer):
    def __init__(self):
        self.clock = 0

    def update_time_logical(self, request, context):
        # Atualizando o relógio lógico com base no tempo lógico da mensagem recebida e na atual
        self.clock = max(self.clock, request.logical_time) + 1

        # Retornando a resposta com o tempo lógico atualizado
        return logic_clock_pb2.Response(logical_time=self.clock)

from concurrent import futures
import grpc
import logic_clock_pb2_grpc
import update_time_service


# Definindo o servidor gRPC
def up_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    logic_clock_pb2_grpc.add_LogicalTimeServicer_to_server(update_time_service.LogicalTime(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print('Servidor iniciado!')
    server.wait_for_termination()
    print('Encerrando o servidor...')


if __name__ == '__main__':
    up_server()

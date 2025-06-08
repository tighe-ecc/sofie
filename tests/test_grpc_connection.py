# tests/test_grpc_connection.py
import grpc

def test_grpc_connection():
    channel = grpc.insecure_channel("localhost:6334")
    try:
        grpc.channel_ready_future(channel).result(timeout=3)
        print("✅ gRPC connection to Qdrant established")
    except grpc.FutureTimeoutError:
        print("❌ gRPC connection failed")

if __name__ == "__main__":
    test_grpc_connection()

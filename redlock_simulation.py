import redis
import time
import uuid
import multiprocessing
client_processes_waiting = [6, 1, 2, 1, 0]

class Redlock:
    def __init__(self, redis_nodes):
        connections = []
        for node in redis_nodes:
            connection = redis.StrictRedis(host=node[0], port=node[1])
            connections.append(connection)
        self.redis_nodes = connections
        pass

    def acquire_lock(self, resource, ttl):
        lock_id = str(uuid.uuid4())
        lock_acquired = 0
        start_time = time.time()

        for connection in self.redis_nodes:
            try:
                if connection.set(resource, lock_id, nx=True, px=ttl):
                    lock_acquired += 1
            except Exception as e:
                pass
        if lock_acquired >= len(self.redis_nodes):
                return True, lock_id
        else:
                return False, None


    def release_lock(self, resource, lock_id):
        for connection in self.redis_nodes:
            try:
                if connection.get(resource) == lock_id:
                    connection.delete(resource)
            except Exception as e:
                print("unexpected error occured")
                pass

def client_process(redis_nodes, resource, ttl, client_id):
    """
    Function to simulate a single client process trying to acquire and release a lock.
    """
    time.sleep(client_processes_waiting[client_id])

    redlock = Redlock(redis_nodes)
    print(f"\nClient-{client_id}: Attempting to acquire lock...")
    lock_acquired, lock_id = redlock.acquire_lock(resource, ttl)

    if lock_acquired:
        print(f"\nClient-{client_id}: Lock acquired! Lock ID: {lock_id}")
        # Simulate critical section
        time.sleep(3)  # Simulate some work
        redlock.release_lock(resource, lock_id)
        print(f"\nClient-{client_id}: Lock released!")
    else:
        print(f"\nClient-{client_id}: Failed to acquire lock.")

if __name__ == "__main__":
    # Define Redis node addresses (host, port)
    redis_nodes = [
        ("localhost", 63791),
        ("localhost", 63792),
        ("localhost", 63793),
        ("localhost", 63794),
        ("localhost", 63795),
    ]

    resource = "shared_resource"
    ttl = 5000  # Lock TTL in milliseconds (5 seconds)

    # Number of client processes
    num_clients = 5

    # Start multiple client processes
    processes = []
    for i in range(num_clients):
        process = multiprocessing.Process(target=client_process, args=(redis_nodes, resource, ttl, i))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

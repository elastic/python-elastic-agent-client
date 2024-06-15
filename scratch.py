import asyncio
import grpc
import sys
import queue

from es_agent_client.generated.elastic_agent_client_pb2_grpc import ElasticAgentStub

def main():
    print("Starting main")
    loop = get_loop()
    coro = do_stuff()
    return loop.run_until_complete(coro)

async def do_stuff():
    channel_credentials = grpc.ssl_channel_credentials()
    channel = grpc.secure_channel( # TODO: this should use `grpc.aio`, if I can figure out why that locks other tasks
        "localhost:8976",
        channel_credentials,
        options=[('grpc.ssl_target_name_override', "server")]
    )
    client = ElasticAgentStub(channel)
    send_queue = queue.SimpleQueue()
    checkin_stream = client.CheckinV2(iter(send_queue.get, None))
    task_one = asyncio.create_task(func_1())
    task_two = asyncio.create_task(func_2())
    await asyncio.gather(task_one, task_two)
    print("finished everything")

async def func_1():
    print("Entered func 1")

async def func_2():
    print("Entered func 2")


def get_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.get_event_loop_policy().get_event_loop()
        if loop is None:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    return loop

if __name__ == "__main__":
    sys.exit(main())


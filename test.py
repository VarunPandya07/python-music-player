import asyncio
import threading

player: asyncio.Task


async def play_song():
    print('song started')
    try:
        asyncio.run(other_thing())
        await asyncio.sleep(30)
        print("song_completed")
    except asyncio.CancelledError as err:
        print("song is stopped.")
        print(f"cancel msg: {err.args}")


async def init_player():
    global player
    player = asyncio.create_task(play_song())

    await player


async def other_thing():
    for i in range(0, 30):
        await asyncio.sleep(4)
        print("other.")

async def main():
    main_task = asyncio.create_task(init_player())

    await asyncio.sleep(10)

    main_task.cancel("next_song")


asyncio.run(main())

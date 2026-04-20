import sys
import anyio
import dagger

async def test_pipeline():
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        src = client.host().directory(".")

        test = (
            client.container()
            .from_("python:3.11-slim-buster")
            .with_mounted_directory("/src", src)
            .with_workdir("/src")
            .with_exec(["pip", "install", "-r", "requirements.txt"])
            .with_exec(["pip", "install", "pytest", "httpx"])
            .with_exec(["pytest", "-x"])
        )

        # Option 1: capture full output
        out = await test.stdout()
        err = await test.stderr()
        print(out)
        print(err)

        # Option 2: stream logs line by line
        # async for line in test.logs():
        #     print(line)

if __name__ == "__main__":
    anyio.run(test_pipeline)

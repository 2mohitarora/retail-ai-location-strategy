from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AgentDefinition
from rich import print
from rich.console import Console
from cli_tools import parser, print_rich_message, parse_and_print_message, get_user_input
from dotenv import load_dotenv
load_dotenv()


async def main():
    console = Console()
    args = parser.parse_args()

    options = ClaudeAgentOptions(
        model=args.model,
        permission_mode="acceptEdits",
        setting_sources=["project"],
        system_prompt="Your context window will be automatically compacted as it approaches its limit. Never stop tasks early due to token budget concerns. Always complete tasks fully, even if the end of your budget is approaching.",
        allowed_tools=[
            'Read',
            'Write',
            'Edit',
            'MultiEdit',
            'Grep',
            'Glob',
            'Task',
            'TodoWrite',
            'WebSearch',
            'WebFetch',
            'Skill'
        ]
    )

    print_rich_message(
        "system",
        f"Welcome to Retail AI Location Strategy Agent!\n\nSelected model: {args.model}",
        console
        )

    async with ClaudeSDKClient(options=options) as client:

        while True:
            input_prompt = get_user_input(console)
            if input_prompt == "exit":
                break

            await client.query(input_prompt)

            async for message in client.receive_response():
                # Uncomment to print raw messages for debugging
                # print(message)
                parse_and_print_message(message, console)


if __name__ == "__main__":
    import asyncio
    import nest_asyncio
    nest_asyncio.apply()

    asyncio.run(main())
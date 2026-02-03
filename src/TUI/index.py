from data import data
from tool import tool
import asyncio
from modules.Languages.PythonProject import PythonProject

data_local = data()

def Start():
    tool.menu()
    print("test")
    Projecttest = PythonProject(special=False)
    Projecttest.openBaseCodeJson()

async def main():
    try:
        await tool.add_path_modules(data.modules_local)
        if data_local.Debug:
            tool.verify_modules()
    except StopAsyncIteration as E:
        print(f"[ERROR] Erro StopAsycnInteration, Erro: {E}")

if __name__ == "__main__":
    asyncio.run(main())
    Start()
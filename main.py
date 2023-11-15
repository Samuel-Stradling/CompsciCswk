import asyncio
from DatabaseHandling.autoBackfill import backfill, find_last_full_date
from gui.master import tkinterApp

async def perform_backfill():
    await asyncio.sleep(0)  # Allows other tasks to run, just a placeholder
    backfill(find_last_full_date())

async def main():
    backfill_task = asyncio.create_task(perform_backfill())

    app = tkinterApp()
    app.geometry("900x900")
    app.title("Finance Analysis App")
    app.mainloop()

    await backfill_task  # Wait for the backfill task to complete

if __name__ == "__main__":
    asyncio.run(main())

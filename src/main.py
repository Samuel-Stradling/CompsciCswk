import asyncio
from DatabaseHandling.autoBackfill import backfill, find_last_full_date
from Gui.master import tkinterApp

async def display_gui():
    await asyncio.sleep(0)  # Allows other tasks to run, just a placeholder
    app = tkinterApp()
    app.geometry("900x900")
    app.title("Finance Analysis App")
    app.mainloop()

async def main():
    gui_task = asyncio.create_task(display_gui())
    print("Please wait for the backfill of the database to finish..")
    backfill(find_last_full_date())

    await gui_task  # Wait for the backfill task to complete

if __name__ == "__main__":
    asyncio.run(main())

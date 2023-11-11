import tkinter as tk

TITLE_FONT = ("Arial", 35, "bold")
BUTTON_FONT = ("Arial", 20)
STANDARD_BLUE = "#0c1469"
BACKGROUND_COLOR = "#f1f5ff"
WHITE = "#ffffff"
HOME_SCREEN_BUTTON_WIDTH = 15
HOME_SCREEN_BUTTON_HEIGHT = 3


class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, SortScreen, GraphsScreen, SearchScreen, ThresholdsScreen):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BACKGROUND_COLOR)

        label = tk.Label(
            self,
            text="Finance Analysis System",
            font=TITLE_FONT,
            fg=WHITE,
            bg=STANDARD_BLUE,
            borderwidth=3,
            relief="solid",
            padx=100,
            pady=8,
        )
        label.place(relx=0.5, rely=0.05, anchor="center")

        button1 = tk.Button(
            self,
            text="Sort Data",
            command=lambda: controller.show_frame(SortScreen),
            highlightbackground=BACKGROUND_COLOR,
            font=BUTTON_FONT,
            width=HOME_SCREEN_BUTTON_WIDTH,
            height=HOME_SCREEN_BUTTON_HEIGHT,
        )
        button1.place(relx=0.25, rely=0.25, anchor="center")

        button2 = tk.Button(
            self,
            text="Generate Graphs",
            command=lambda: controller.show_frame(GraphsScreen),
            highlightbackground=BACKGROUND_COLOR,
            font=BUTTON_FONT,
            width=HOME_SCREEN_BUTTON_WIDTH,
            height=HOME_SCREEN_BUTTON_HEIGHT,
        )
        button2.place(relx=0.25, rely=0.45, anchor="center")

        button3 = tk.Button(
            self,
            text="Search Data",
            command=lambda: controller.show_frame(SearchScreen),
            highlightbackground=BACKGROUND_COLOR,
            font=BUTTON_FONT,
            width=HOME_SCREEN_BUTTON_WIDTH,
            height=HOME_SCREEN_BUTTON_HEIGHT,
        )
        button3.place(relx=0.75, rely=0.25, anchor="center")

        button4 = tk.Button(
            self,
            text="Change Settings and Thresholds",
            command=lambda: controller.show_frame(ThresholdsScreen),
            highlightbackground=BACKGROUND_COLOR,
            font=BUTTON_FONT,
            width=HOME_SCREEN_BUTTON_WIDTH,
            height=HOME_SCREEN_BUTTON_HEIGHT,
            wraplength=120,
        )
        button4.place(relx=0.75, rely=0.45, anchor="center")


class BackButton(tk.Button):
    def __init__(self, parent, controller):
        super().__init__(
            parent,
            text="⬅",
            command=lambda: controller.show_frame(StartPage),
            highlightbackground=BACKGROUND_COLOR,
            fg="orange",
            font=BUTTON_FONT,
        )
        self.place(relx=0.95, rely=0.05, anchor="center")


class SortScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BACKGROUND_COLOR)
        label = tk.Label(self, text="Page 1", font=TITLE_FONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        backButton = BackButton(self, controller)


class GraphsScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BACKGROUND_COLOR)
        label = tk.Label(self, text="Generate Graphs", font=TITLE_FONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        backButton = BackButton(self, controller)


class SearchScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BACKGROUND_COLOR)
        label = tk.Label(self, text="Search Data", font=TITLE_FONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        backButton = BackButton(self, controller)


class ThresholdsScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BACKGROUND_COLOR)
        label = tk.Label(self, text="Change Settings and Thresholds", font=TITLE_FONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        backButton = BackButton(self, controller)


app = tkinterApp()
app.geometry("900x900")
app.mainloop()

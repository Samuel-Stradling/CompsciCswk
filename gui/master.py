import tkinter as tk
import tkinter.messagebox as mb

TITLE_FONT = ("Arial", 35, "bold")
BUTTON_FONT = ("Arial", 20)
TEXT_BOX_FONT = ("Helvetica", 15)
ITALIC_SAVE_DIR_FONT = ("Helvetica", 15, "italic")
COMMAND_BUTTON_FONT = ("Arial", 27, "bold")
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
    def show_top_10_results(self, top_10_data: list, sort_by):
        # Create or update a label to display the top 10 results
        top_10_data_reformatted = []
        top_10_data.reverse()
        for dictionary in top_10_data:
            temp = f"{dictionary['ticker']} on {dictionary['date']} at {dictionary[sort_by]} ({sort_by})"
            top_10_data_reformatted.append(temp)

        result_label = tk.Label(
            self,
            text="Top 10 Results:\n\n\n" + "\n\n".join(top_10_data_reformatted),
            font=TEXT_BOX_FONT,
            fg=WHITE,
            bg=STANDARD_BLUE,
            padx=10,
            pady=10,
            borderwidth=3,
            relief="solid",
        )
        result_label.place(relx=0.8, rely=0.4, anchor="center")

        from datetime import datetime

        date = datetime.today().date()

        save_dir_label = tk.Label(
            self,
            text=f"Saved to /DatabaseHandling/SortSearchResults/{date}-{sort_by}X.txt",
            font=ITALIC_SAVE_DIR_FONT,
            fg=WHITE,
            bg=STANDARD_BLUE,
            width=32,
            height=4,
            borderwidth=2,
            relief="solid",
            wraplength=310,
        )

        save_dir_label.place(relx=0.8, rely=0.7, anchor="center")

    def get_user_data_and_sort(
        self, start_date_entry, end_date_entry, selected_sort, sort_method
    ):
        from DatabaseHandling.sort import SortItems

        # Retrieve the entered data
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()
        sort_by = selected_sort.get()
        sort_algorithm = sort_method.get()

        # Check the validity of the data
        if not (start_date and end_date):
            warning = "Please enter both start and end dates."
        elif not sort_algorithm:
            warning = "Please select a sort method."
        else:
            try:
                sorter = SortItems(start_date, sort_by, end_date)
                if sort_algorithm == "bubble":
                    result = sorter.bubble_sort()
                elif sort_algorithm == "merge":
                    result = sorter.merge_sort()

                self.show_top_10_results(result[-10:], sorter.sortMetric)

            except Exception as e:
                mb.showwarning("Invalid Data", e)
            return

        # Show a warning message
        mb.showwarning("Data Warning", warning)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BACKGROUND_COLOR)
        label = tk.Label(
            self,
            text="Sort Data",
            font=TITLE_FONT,
            fg=WHITE,
            bg=STANDARD_BLUE,
            borderwidth=3,
            relief="solid",
            padx=100,
            pady=8,
        )
        label.place(relx=0.5, rely=0.05, anchor="center")

        backButton = BackButton(self, controller)

        # Start Date Entry
        start_label = tk.Label(
            self, text="Start Date (yyyy-mm-dd):", font=BUTTON_FONT, bg=BACKGROUND_COLOR
        )
        start_label.place(relx=0.15, rely=0.13, anchor="center")
        start_date_entry = tk.Entry(self, font=TEXT_BOX_FONT, width=12)
        start_date_entry.place(relx=0.36, rely=0.115)

        # End Date Entry
        end_label = tk.Label(
            self, text="End Date (yyyy-mm-dd):", font=BUTTON_FONT, bg=BACKGROUND_COLOR
        )
        end_label.place(relx=0.15, rely=0.23, anchor="center")
        end_date_entry = tk.Entry(self, font=TEXT_BOX_FONT, width=12)
        end_date_entry.place(relx=0.36, rely=0.215)

        # Dropdown Box for Sort Metrics
        sort_label = tk.Label(
            self, text="Sort By:", font=BUTTON_FONT, bg=BACKGROUND_COLOR
        )
        sort_label.place(relx=0.23, rely=0.33, anchor="center")

        # Options for the dropdown
        sort_options = ["high", "close", "open", "volume", "weighted_volume"]
        selected_sort = tk.StringVar(self)
        selected_sort.set(sort_options[0])  # Default value

        # Creating the dropdown
        sort_dropdown = tk.OptionMenu(self, selected_sort, *sort_options)
        sort_dropdown.config(
            font=TEXT_BOX_FONT, width=12, highlightbackground=BACKGROUND_COLOR
        )
        sort_dropdown.place(relx=0.43, rely=0.33, anchor="center")

        # Sort Method Checkbox
        sort_method_label = tk.Label(
            self, text="Sort Method:", font=BUTTON_FONT, bg=BACKGROUND_COLOR
        )
        sort_method_label.place(relx=0.21, rely=0.43, anchor="center")

        # Variable to store selected sort method
        sort_method = tk.StringVar()

        # Radio buttons for sorting methods
        bubble_radio = tk.Radiobutton(
            self,
            text="Bubble",
            variable=sort_method,
            value="bubble",
            font=TEXT_BOX_FONT,
            bg=BACKGROUND_COLOR,
        )
        bubble_radio.place(relx=0.4, rely=0.43, anchor="center")

        merge_radio = tk.Radiobutton(
            self,
            text="Merge",
            variable=sort_method,
            value="merge",
            font=TEXT_BOX_FONT,
            bg=BACKGROUND_COLOR,
        )
        merge_radio.place(relx=0.4, rely=0.46, anchor="center")

        # Button to get user data
        get_data_button = tk.Button(
            self,
            text="SORT",
            command=lambda: self.get_user_data_and_sort(
                start_date_entry, end_date_entry, selected_sort, sort_method
            ),
            highlightbackground=BACKGROUND_COLOR,
            font=COMMAND_BUTTON_FONT,
            width=10,
            height=2,
        )
        get_data_button.place(relx=0.42, rely=0.6, anchor="center")


class GraphsScreen(tk.Frame):
    def get_user_data_and_generate(
        self,
        selected_company1,
        selected_company2,
        selected_company3,
        end_date_entry,
        start_date_entry,
        graph_type,
        using_single_axes,
    ):
        from graphing.generate import Generate

        # Retrieve the selected companies from the dropdown boxes
        company1 = selected_company1.get()
        company2 = selected_company2.get()
        company3 = selected_company3.get()
        end_date = end_date_entry.get()
        start_date = start_date_entry.get()
        graph_type = graph_type.get()
        using_single_axes = using_single_axes.get()

        if not (start_date and end_date):
            warning = "Please enter both start and end dates."
            mb.showwarning("Date Warning", warning)
        elif graph_type == "":
            warning = "Please select a graph type"
            mb.showwarning("Graph Type Warning", warning)
        else:
            try:
                companies = [company1, company2, company3]
                while "None" in companies:
                    companies.remove("None")
                if len(companies) < 1:
                    message = "1 or more companies must be selected"
                    mb.showwarning("Invalid data", message=message)
                    return
                elif len(companies) == 1:
                    companies = companies[0]
                generator = Generate(start_date, end_date, *companies)
                if graph_type == "line":
                    generator.generate_line_graph(using_single_axes)
                elif graph_type == "bar":
                    generator.generate_bar_graph(using_single_axes)

            except Exception as e:
                mb.showwarning("Invalid Data", e)
            return

        # generator1 = Generate()

    def get_all_company_names(self):
        import sqlite3

        try:
            conn = sqlite3.connect("data/main.sql")
            cursor = conn.cursor()
            cursor.execute("SELECT ticker FROM Companies")
            result = cursor.fetchall()
            return [x[0] for x in result]

        except sqlite3.Error as error:
            print("Error: {}".format(error))

        finally:
            # Close the cursor and connection
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BACKGROUND_COLOR)
        label = tk.Label(
            self,
            text="Produce Graphs",
            font=TITLE_FONT,
            fg=WHITE,
            bg=STANDARD_BLUE,
            borderwidth=3,
            relief="solid",
            padx=100,
            pady=8,
        )
        label.place(relx=0.5, rely=0.05, anchor="center")

        # Start Date Entry
        start_label = tk.Label(
            self, text="Start Date (yyyy-mm-dd):", font=BUTTON_FONT, bg=BACKGROUND_COLOR
        )
        start_label.place(relx=0.235, rely=0.50, anchor="center")
        start_date_entry = tk.Entry(self, font=TEXT_BOX_FONT, width=12)
        start_date_entry.place(relx=0.44, rely=0.49)

        # End Date Entry
        end_label = tk.Label(
            self, text="End Date (yyyy-mm-dd):", font=BUTTON_FONT, bg=BACKGROUND_COLOR
        )
        end_label.place(relx=0.235, rely=0.59, anchor="center")
        end_date_entry = tk.Entry(self, font=TEXT_BOX_FONT, width=12)
        end_date_entry.place(relx=0.44, rely=0.58)

        # Dropdown Box for Company 1
        company1_label = tk.Label(
            self, text="Company 1:", font=BUTTON_FONT, bg=BACKGROUND_COLOR
        )
        company1_label.place(relx=0.3, rely=0.2, anchor="center")

        # Options for the dropdown
        company_options = ["None"] + self.get_all_company_names()

        selected_company1 = tk.StringVar(self)
        selected_company1.set(company_options[0])  # Default value

        # Creating the dropdown
        company1_dropdown = tk.OptionMenu(self, selected_company1, *company_options)
        company1_dropdown.config(
            font=TEXT_BOX_FONT, width=12, highlightbackground=BACKGROUND_COLOR
        )
        company1_dropdown.place(relx=0.51, rely=0.2, anchor="center")

        # Dropdown Box for Company 2
        company2_label = tk.Label(
            self, text="Company 2:", font=BUTTON_FONT, bg=BACKGROUND_COLOR
        )
        company2_label.place(relx=0.3, rely=0.3, anchor="center")

        selected_company2 = tk.StringVar(self)
        selected_company2.set(company_options[1])  # Default value

        # Creating the dropdown
        company2_dropdown = tk.OptionMenu(self, selected_company2, *company_options)
        company2_dropdown.config(
            font=TEXT_BOX_FONT, width=12, highlightbackground=BACKGROUND_COLOR
        )
        company2_dropdown.place(relx=0.51, rely=0.3, anchor="center")

        # Dropdown Box for Company 3
        company3_label = tk.Label(
            self, text="Company 3:", font=BUTTON_FONT, bg=BACKGROUND_COLOR
        )
        company3_label.place(relx=0.3, rely=0.4, anchor="center")

        selected_company3 = tk.StringVar(self)
        selected_company3.set(company_options[2])  # Default value

        # Creating the dropdown
        company3_dropdown = tk.OptionMenu(self, selected_company3, *company_options)
        company3_dropdown.config(
            font=TEXT_BOX_FONT, width=12, highlightbackground=BACKGROUND_COLOR
        )
        company3_dropdown.place(relx=0.51, rely=0.4, anchor="center")

        graph_type = tk.StringVar()

        graph_type_label = tk.Label(
            self, text="Select a graph type:", font=BUTTON_FONT, bg=BACKGROUND_COLOR
        )
        graph_type_label.place(relx=0.255, rely=0.7, anchor="center")

        # Radio buttons for sorting methods
        line_radio = tk.Radiobutton(
            self,
            text="Line",
            variable=graph_type,
            value="line",
            font=TEXT_BOX_FONT,
            bg=BACKGROUND_COLOR,
        )
        line_radio.place(relx=0.51, rely=0.7, anchor="center")

        bar_radio = tk.Radiobutton(
            self,
            text="Bar",
            variable=graph_type,
            value="bar",
            font=TEXT_BOX_FONT,
            bg=BACKGROUND_COLOR,
        )
        bar_radio.place(relx=0.51, rely=0.73, anchor="center")

        use_single_axes = tk.BooleanVar()
        use_single_axes_checkbox = tk.Checkbutton(
            self,
            text="Use Single Axes",
            variable=use_single_axes,
            font=TEXT_BOX_FONT,
            bg=BACKGROUND_COLOR,
        )
        use_single_axes_checkbox.place(relx=0.5, rely=0.8, anchor="center")

        get_input_button = tk.Button(
            self,
            text="GENERATE",
            command=lambda: self.get_user_data_and_generate(
                selected_company1,
                selected_company2,
                selected_company3,
                end_date_entry,
                start_date_entry,
                graph_type,
                use_single_axes,
            ),
            highlightbackground=BACKGROUND_COLOR,
            font=COMMAND_BUTTON_FONT,
            width=15,
            height=2,
        )
        get_input_button.place(relx=0.5, rely=0.95, anchor="center")

        backButton = BackButton(self, controller)


class SearchScreen(tk.Frame):
    def show_search_results(self, data, date):
        # destroy label if it already exists
        if self.result_label:
            self.result_label.destroy()

        if type(data) == dict:
            data = [
                f"current high: {data['high']}",
                f"current low: {data['low']}\n",
                f"open price: {data['open']}",
                f"current price: {data['currentPrice']}",
                f"current percentage change: {data['currentPercentageChange']}\n",
                f"current traded volume: {data['currentVolume']}",
            ]
            data = [str(x) for x in data]

            self.result_label = tk.Label(
                self,
                text=f"Live data:\n\n\n" + "\n\n".join(data),
                font=TEXT_BOX_FONT,
                fg=WHITE,
                bg=STANDARD_BLUE,
                width=35,
                pady=10,
                borderwidth=3,
                relief="solid",
            )
            self.result_label.place(relx=0.5, rely=0.75, anchor="center")

        else:
            self.result_label = tk.Label(
                self,
                text=f"Close price for {date}:" + f"\n\n{data}",
                font=TEXT_BOX_FONT,
                fg=WHITE,
                bg=STANDARD_BLUE,
                padx=10,
                pady=10,
                borderwidth=3,
                relief="solid",
            )
            self.result_label.place(relx=0.5, rely=0.7, anchor="center")

    def get_user_data_and_generate(self, company_entry, date_entry):
        from DatabaseHandling.search import search_by_date_and_company

        company = company_entry.get()
        date = date_entry.get()

        if not date:
            message = "Please enter a date"
            mb.showwarning("Date warning", message)
            return
        if not company:
            message = "Please enter a company"
            mb.showwarning("Data warning", message)
            return

        try:
            result = search_by_date_and_company(company, date)
            print(result)
            self.show_search_results(result, date)
        except Exception as e:
            mb.showwarning("Data error", e)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BACKGROUND_COLOR)
        label = tk.Label(
            self,
            text="Search Data",
            font=TITLE_FONT,
            fg=WHITE,
            bg=STANDARD_BLUE,
            borderwidth=3,
            relief="solid",
            padx=100,
            pady=8,
        )
        label.place(relx=0.5, rely=0.05, anchor="center")

        backButton = BackButton(self, controller)

        self.result_label = None  # Initialize result_label attribute

        # Company Entry
        company = tk.Label(
            self, text="Company ticker:", font=BUTTON_FONT, bg=BACKGROUND_COLOR
        )
        company.place(relx=0.235, rely=0.2, anchor="center")
        company_entry = tk.Entry(self, font=TEXT_BOX_FONT, width=12)
        company_entry.place(relx=0.44, rely=0.185)

        # Date Entry
        date = tk.Label(
            self, text="Date (yyyy-mm-dd):", font=BUTTON_FONT, bg=BACKGROUND_COLOR
        )
        date.place(relx=0.235, rely=0.3, anchor="center")
        date_entry = tk.Entry(self, font=TEXT_BOX_FONT, width=12)
        date_entry.place(relx=0.44, rely=0.285)

        get_input_button = tk.Button(
            self,
            text="SEARCH",
            command=lambda: self.get_user_data_and_generate(company_entry, date_entry),
            highlightbackground=BACKGROUND_COLOR,
            font=COMMAND_BUTTON_FONT,
            width=15,
            height=2,
        )
        get_input_button.place(relx=0.5, rely=0.45, anchor="center")


class ThresholdsScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BACKGROUND_COLOR)
        label = tk.Label(
            self,
            text="Preferences and Thresholds",
            font=TITLE_FONT,
            fg=WHITE,
            bg=STANDARD_BLUE,
            borderwidth=3,
            relief="solid",
            padx=100,
            pady=8,
        )
        label.place(relx=0.5, rely=0.05, anchor="center")

        backButton = BackButton(self, controller)

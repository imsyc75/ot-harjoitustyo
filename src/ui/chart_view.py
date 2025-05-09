import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ui.style import Style

class ChartView(tk.Toplevel):
    """Luokka, jolla näytetään visualisointeja käyttäjän kuluista.
    Näyttää piirakkakaavion kulujen jakautumisesta luokittain.

    Attributes:
        user_id: Käyttäjän yksilöllinen tunniste.
        expenses_data: Lista, joka sisältää käyttäjän kulutiedot.
        year: Valittu vuosi.
        month: Valittu kuukausi.
    """

    def __init__(self, parent, user_id, expenses_data, year, month):
        """Konstruktori, luo uuden kaavionäkymän

        Args:
            parent: Isäntäikkuna, johon tämä näkymä liittyy.
            user_id: Käyttäjän yksilöllinen tunniste.
            expenses_data: Lista, joka sisältää käyttäjän kulutiedot.
            year: Valittu vuosi.
            month: Valittu Kuukausi.
        """
        super().__init__(parent)
        self.title(f"MoneyTrack - Expense Charts ({year}/{month})")
        self.user_id = user_id
        self.expenses_data = expenses_data
        self.year = year
        self.month = month
        self.figure = None
        self.canvas = None

        Style.apply_style(self)

        self.chart_frame = tk.Frame(self)
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.create_pie_chart()

        close_button = Style.create_button(
            self, text="Close", command=self.close_window, is_primary=True
        )
        close_button.pack(pady=10)

        self.geometry("800x600")
        self.resizable(True, True)

        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def close_window(self):
        """Sulje ikkuna ja tyhjennä matplotlib-resurssit."""
        if self.figure is not None:
            plt.close(self.figure)

        for widget in self.winfo_children():
            widget.destroy()

        self.destroy()

    def create_pie_chart(self):
        """Luo piirakkakaavio, joka näyttää kulujen jakautumisen luokittain."""

        if not self.expenses_data:
            # If no data, show message
            message = tk.Label(
                self.chart_frame,
                text=f"No expenses for {self.year}/{self.month}",
                font=("Times New Roman", 14)
            )
            message.pack(fill=tk.BOTH, expand=True)
            return

        category_totals = {}
        for expense in self.expenses_data:
            category = expense["category"]
            amount = float(expense["amount"])

            if category in category_totals:
                category_totals[category] += amount
            else:
                category_totals[category] = amount

        # Prepare pie chart data
        categories = list(category_totals.keys())
        amounts = list(category_totals.values())

        total = sum(amounts)
        percentages = [(amount/total)*100 for amount in amounts]

        category_labels = [f"{cat} ({pct:.1f}%)" for cat, pct in zip(categories, percentages)]

        # Create chart
        plt.rcParams['font.sans-serif'] = ['Times New Roman', 'DejaVu Sans', 'Liberation Sans',
                                           'FreeSans', 'SimHei', 'Microsoft YaHei']
        plt.rcParams['axes.unicode_minus'] = False

        self.figure, ax = plt.subplots(figsize=(5, 4), subplot_kw=dict(aspect="equal"))

        # generoitu koodi alkaa
        wedges, texts = ax.pie(
            amounts,
            startangle=90,
            wedgeprops=dict(width=0.5)
        )

        ax.legend(
            wedges,
            category_labels,
            title="Expense Categories",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1)
        )
        # generoitu koodi loppuu

        month_names = ["January", "February", "March", "April", "May", "June",
                       "July", "August", "September", "October", "November", "December"]
        month_name = month_names[self.month - 1]
        plt.title(f"{month_name} {self.year}")

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
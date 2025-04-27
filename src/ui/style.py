import tkinter as tk
from tkinter import ttk
import sys

class Style:
    PINK_LIGHT = "#FFE6E8"
    PINK_MEDIUM = "#FFCCD0"
    PINK_DARK = "#FF9FA7"
    WHITE = "#FFFFFF"
    TEXT_COLOR = "#5A5A5A"
    ACCENT_COLOR = "#FF6B81"

    FONT_FAMILY = "Times New Roman"
    FONT_SIZE_SMALL = 10
    FONT_SIZE_NORMAL = 12
    FONT_SIZE_LARGE = 14
    FONT_SIZE_XLARGE = 18

    @classmethod
    def apply_style(cls, root):
        style = ttk.Style()
        # generoitu koodi alkaa
        style.configure(".",
                       background=cls.PINK_LIGHT,
                       foreground=cls.TEXT_COLOR,
                       font=(cls.FONT_FAMILY, cls.FONT_SIZE_NORMAL))

        style.configure("Treeview",
                       background=cls.WHITE,
                       fieldbackground=cls.WHITE,
                       foreground=cls.TEXT_COLOR,
                       font=(cls.FONT_FAMILY, cls.FONT_SIZE_NORMAL))

        style.configure("Treeview.Heading",
                      font=(cls.FONT_FAMILY, cls.FONT_SIZE_NORMAL, "bold"),
                      background=cls.PINK_MEDIUM,
                      foreground=cls.TEXT_COLOR)

        style.configure("TButton",
                      background=cls.PINK_MEDIUM,
                      foreground=cls.TEXT_COLOR,
                      font=(cls.FONT_FAMILY, cls.FONT_SIZE_NORMAL),
                      borderwidth=0,
                      relief="flat",
                      padding=6)

        style.map("TButton",
                background=[('active', cls.PINK_DARK), ('pressed', cls.PINK_DARK)])

        style.configure("TCombobox",
                      fieldbackground=cls.WHITE,
                      background=cls.WHITE)

        root.option_add("*Entry.Background", cls.WHITE)
        root.option_add("*Entry.Foreground", cls.TEXT_COLOR)
        root.option_add("*Entry.Font", (cls.FONT_FAMILY, cls.FONT_SIZE_NORMAL))

        root.option_add("*Label.Background", cls.PINK_LIGHT)
        root.option_add("*Label.Foreground", cls.TEXT_COLOR)
        root.option_add("*Label.Font", (cls.FONT_FAMILY, cls.FONT_SIZE_NORMAL))

        root.option_add("*Frame.Background", cls.PINK_LIGHT)

        root.configure(background=cls.PINK_LIGHT)
        # generoitu koodi loppuu

    @classmethod
    def create_title_label(cls, parent, text):
        label = tk.Label(parent,
                        text=text,
                        font=(cls.FONT_FAMILY, cls.FONT_SIZE_XLARGE, "bold"),
                        foreground=cls.ACCENT_COLOR,
                        background=cls.PINK_LIGHT,
                        pady=10)
        return label

    @classmethod
    def create_button(cls, parent, text, command, is_primary=True):
        # generoitu koodi alkaa
        bg_color = "#FF4D67" if is_primary else cls.PINK_DARK
        fg_color = cls.PINK_DARK

        button = tk.Button(parent,
                         text=text,
                         command=command,
                         background=bg_color,
                         foreground=fg_color,
                         font=(cls.FONT_FAMILY, cls.FONT_SIZE_NORMAL, "bold"),
                         relief=tk.FLAT,
                         borderwidth=0,
                         padx=15,
                         pady=5,
                         cursor="heart" if "win" in sys.platform else "hand2")

        hover_color = cls.PINK_DARK if not is_primary else "#FF4D67"
        button.bind("<Enter>", lambda e: e.widget.config(background=hover_color))
        button.bind("<Leave>", lambda e: e.widget.config(background=bg_color))
        # generoitu koodi loppuu
        return button
    
import tkinter as tk
from tkinter import ttk
import sys

class Style:
    # clours
    PINK_LIGHT = "#FFE6E8"
    PINK_MEDIUM = "#FFCCD0"
    PINK_DARK = "#FF9FA7"
    WHITE = "#FFFFFF"
    TEXT_COLOR = "#5A5A5A"
    ACCENT_COLOR = "#FF6B81"

    FONT_FAMILY = "Comic Sans MS" if "win" in sys.platform else "Marker Felt"
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
                       font=(cls.FONT_FAMILY, cls.FONT_SIZE_SMALL))

        style.configure("Treeview.Heading",
                      font=(cls.FONT_FAMILY, cls.FONT_SIZE_NORMAL, "bold"),
                      background=cls.PINK_MEDIUM,
                      foreground=cls.TEXT_COLOR)

        style.configure("TButton",
                      background=cls.PINK_MEDIUM,
                      foreground=cls.TEXT_COLOR,
                      font=(cls.FONT_FAMILY, cls.FONT_SIZE_NORMAL),
                      borderwidth=1,
                      relief="raised",
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
    def create_cute_button(cls, parent, text, command, is_primary=False):
        # generoitu koodi alkaa
        bg_color = cls.ACCENT_COLOR if is_primary else cls.PINK_MEDIUM
        fg_color = cls.WHITE if is_primary else cls.TEXT_COLOR

        button = tk.Button(parent,
                         text=text,
                         command=command,
                         bg=bg_color,
                         fg=fg_color,
                         font=(cls.FONT_FAMILY, cls.FONT_SIZE_NORMAL),
                         relief=tk.RAISED,
                         borderwidth=2,
                         padx=15,
                         pady=5,
                         cursor="heart" if "win" in sys.platform else "hand2")

        hover_color = cls.PINK_DARK if not is_primary else "#FF4D67"
        button.bind("<Enter>", lambda e: e.widget.config(background=hover_color))
        button.bind("<Leave>", lambda e: e.widget.config(background=bg_color))
        # generoitu koodi loppuu
        return button

    @classmethod
    def create_rounded_entry(cls, parent):
        # generoitu koodi alkaa
        frame = tk.Frame(parent, bg=cls.PINK_MEDIUM, padx=2, pady=2)
        entry = tk.Entry(frame,
                       font=(cls.FONT_FAMILY, cls.FONT_SIZE_NORMAL),
                       bg=cls.WHITE,
                       fg=cls.TEXT_COLOR,
                       relief=tk.FLAT,
                       insertbackground=cls.ACCENT_COLOR)
        entry.pack(fill=tk.BOTH, expand=True)
        # generoitu koodi loppuu
        return frame, entry

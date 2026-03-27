import tkinter as tk
from tkinter import font as tkfont

# ── Palette ───────────────────────────────────────────────────────────────────
BG            = "#F7F3EE"
CARD_BG       = "#FFFFFF"
ACCENT        = "#7C6A55"
ACCENT_DARK   = "#5C4D3C"
ACCENT_LIGHT  = "#C4AD94"
TEXT_DARK     = "#2E2219"
TEXT_MID      = "#7A6652"
TEXT_LIGHT    = "#B5A392"
ENTRY_BG      = "#F0EBE3"
ENTRY_BD      = "#D6C9B8"
BTN_READER    = "#E8F0E9"
BTN_READER_FG = "#3A6B40"
RED_ERR       = "#C0392B"


class RingraziamentiApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ringraziamenti")
        self.resizable(False, False)
        self.configure(bg=BG)

        # Fonts
        self.f_title  = tkfont.Font(family="Georgia",   size=26, weight="bold")
        self.f_sub    = tkfont.Font(family="Georgia",   size=11, slant="italic")
        self.f_label  = tkfont.Font(family="Helvetica", size=10, weight="bold")
        self.f_entry  = tkfont.Font(family="Helvetica", size=11)
        self.f_btn    = tkfont.Font(family="Helvetica", size=11, weight="bold")
        self.f_link   = tkfont.Font(family="Helvetica", size=10, underline=True)
        self.f_small  = tkfont.Font(family="Helvetica", size=9)
        self.f_mode   = tkfont.Font(family="Helvetica", size=10)

        # "login" | "register"
        self.mode = "login"

        self._build_ui()
        self._auto_size()

    # ── UI principale ─────────────────────────────────────────────────────────
    def _build_ui(self):
        outer = tk.Frame(self, bg=BG)
        outer.pack(fill="both", expand=True, padx=30, pady=30)

        # ── Header ────────────────────────────────────────────────────────────
        tk.Label(outer, text="✉", font=tkfont.Font(size=36),
                 bg=BG, fg=ACCENT).pack(pady=(0, 4))
        tk.Label(outer, text="Ringraziamenti", font=self.f_title,
                 bg=BG, fg=TEXT_DARK).pack()
        tk.Label(outer, text="Condividi la tua gratitudine con chi ami",
                 font=self.f_sub, bg=BG, fg=TEXT_MID).pack(pady=(2, 20))

        # ── Card ──────────────────────────────────────────────────────────────
        card = tk.Frame(outer, bg=CARD_BG,
                        highlightthickness=1, highlightbackground=ENTRY_BD)
        card.pack(fill="x", pady=(0, 14))

        inner = tk.Frame(card, bg=CARD_BG)
        inner.pack(fill="both", expand=True, padx=28, pady=24)

        # Titolo card
        self.card_title = tk.Label(inner,
                                   text="Accedi al tuo account",
                                   font=tkfont.Font(family="Helvetica",
                                                    size=14, weight="bold"),
                                   bg=CARD_BG, fg=TEXT_DARK, anchor="w")
        self.card_title.pack(fill="x", pady=(0, 18))

        # ── Campi ─────────────────────────────────────────────────────────────
        fields = tk.Frame(inner, bg=CARD_BG)
        fields.pack(fill="x")

        # Nome (solo registrazione)
        self.name_block = tk.Frame(fields, bg=CARD_BG)
        tk.Label(self.name_block, text="NOME COMPLETO",
                 font=self.f_label, bg=CARD_BG, fg=TEXT_MID).pack(anchor="w")
        self.entry_name = self._make_entry(self.name_block, "Es. Mario Rossi")

        # Email
        email_block = tk.Frame(fields, bg=CARD_BG)
        email_block.pack(fill="x", pady=(0, 12))
        tk.Label(email_block, text="EMAIL",
                 font=self.f_label, bg=CARD_BG, fg=TEXT_MID).pack(anchor="w")
        self.entry_email = self._make_entry(email_block, "Es. mario@email.com")

        # Password
        pwd_block = tk.Frame(fields, bg=CARD_BG)
        pwd_block.pack(fill="x", pady=(0, 6))
        tk.Label(pwd_block, text="PASSWORD",
                 font=self.f_label, bg=CARD_BG, fg=TEXT_MID).pack(anchor="w")
        self.entry_pwd = self._make_entry(pwd_block, "••••••••", show="•")

        # Conferma password (solo registrazione)
        self.confirm_block = tk.Frame(fields, bg=CARD_BG)
        tk.Label(self.confirm_block, text="CONFERMA PASSWORD",
                 font=self.f_label, bg=CARD_BG, fg=TEXT_MID).pack(anchor="w")
        self.entry_confirm = self._make_entry(self.confirm_block, "••••••••", show="•")

        # Link password dimenticata (solo login)
        self.forgot_frame = tk.Frame(inner, bg=CARD_BG)
        self.forgot_frame.pack(fill="x", pady=(4, 14))
        tk.Label(self.forgot_frame, text="Password dimenticata?",
                 font=self.f_link, bg=CARD_BG, fg=ACCENT,
                 cursor="hand2").pack(side="right")

        # Messaggio errore / conferma
        self.lbl_msg = tk.Label(inner, text="", font=self.f_small,
                                bg=CARD_BG, fg=RED_ERR, wraplength=360)
        self.lbl_msg.pack(fill="x", pady=(0, 8))

        # Bottone principale (Accedi / Crea account)
        self.btn_main = tk.Button(inner, text="Accedi",
                                  font=self.f_btn,
                                  bg=ACCENT, fg="white",
                                  activebackground=ACCENT_DARK,
                                  activeforeground="white",
                                  relief="flat", bd=0, cursor="hand2",
                                  pady=10,
                                  command=self._on_main_action)
        self.btn_main.pack(fill="x", pady=(0, 16))

        # ── Toggle Accedi / Registrati ────────────────────────────────────────
        toggle_row = tk.Frame(inner, bg=CARD_BG)
        toggle_row.pack(fill="x")

        tk.Label(toggle_row, text="Non hai un account?",
                 font=self.f_small, bg=CARD_BG, fg=TEXT_LIGHT).pack(side="left")

        self.toggle_lbl = tk.Label(toggle_row, text=" Registrati",
                                   font=tkfont.Font(family="Helvetica",
                                                    size=10, weight="bold",
                                                    underline=True),
                                   bg=CARD_BG, fg=ACCENT, cursor="hand2")
        self.toggle_lbl.pack(side="left")
        self.toggle_lbl.bind("<Button-1>", lambda e: self._switch_mode())

        # ── Separatore ────────────────────────────────────────────────────────
        sep = tk.Frame(outer, bg=BG)
        sep.pack(fill="x", pady=4)
        tk.Frame(sep, bg=ACCENT_LIGHT, height=1).pack(
            fill="x", side="left", expand=True, padx=(0, 8), pady=6)
        tk.Label(sep, text="oppure", font=self.f_small,
                 bg=BG, fg=TEXT_LIGHT).pack(side="left")
        tk.Frame(sep, bg=ACCENT_LIGHT, height=1).pack(
            fill="x", side="left", expand=True, padx=(8, 0), pady=6)

        # ── Bottone Lettore ───────────────────────────────────────────────────
        tk.Button(outer,
                  text="📖  Entra come Lettore",
                  font=self.f_btn,
                  bg=BTN_READER, fg=BTN_READER_FG,
                  activebackground="#D6EAD8",
                  activeforeground=BTN_READER_FG,
                  relief="flat", bd=0, cursor="hand2",
                  pady=10,
                  highlightthickness=1,
                  highlightbackground="#A8CCA9",
                  command=self._on_enter_as_reader).pack(fill="x")

        tk.Label(outer,
                 text="Hai un codice di ringraziamento? Accedi qui.",
                 font=self.f_small, bg=BG, fg=TEXT_LIGHT).pack(pady=(6, 0))

    # ── Switch Login ↔ Register ───────────────────────────────────────────────
    def _switch_mode(self):
        self.lbl_msg.config(text="")

        # Pulisce tutti i campi prima di cambiare vista
        self._reset_entry(self.entry_name,    "Es. Mario Rossi",  show=None)
        self._reset_entry(self.entry_email,   "Es. mario@email.com", show=None)
        self._reset_entry(self.entry_pwd,     "••••••••",          show="•")
        self._reset_entry(self.entry_confirm, "••••••••",          show="•")

        if self.mode == "login":
            # → passa a registrazione
            self.mode = "register"
            self.card_title.config(text="Crea il tuo account")
            self.btn_main.config(text="Crea account")

            # Mostra nome sopra email: pack_forget + riordino
            for child in self.name_block.master.winfo_children():
                child.pack_forget()
            self.name_block.pack(fill="x", pady=(0, 12))
            # email block è il secondo figlio
            self.name_block.master.winfo_children()[1].pack(fill="x", pady=(0, 12))
            # pwd block è il terzo
            self.name_block.master.winfo_children()[2].pack(fill="x", pady=(0, 6))
            # conferma
            self.confirm_block.pack(fill="x", pady=(0, 6))

            self.forgot_frame.pack_forget()
            self.toggle_lbl.config(text=" Accedi")
            self.toggle_lbl.master.winfo_children()[0].config(
                text="Hai già un account?")

        else:
            # → passa a login
            self.mode = "login"
            self.card_title.config(text="Accedi al tuo account")
            self.btn_main.config(text="Accedi")

            self.name_block.pack_forget()
            self.confirm_block.pack_forget()
            # Riassicura email e pwd visibili
            self.name_block.master.winfo_children()[1].pack(fill="x", pady=(0, 12))
            self.name_block.master.winfo_children()[2].pack(fill="x", pady=(0, 6))

            self.forgot_frame.pack(fill="x", pady=(4, 14))
            self.toggle_lbl.config(text=" Registrati")
            self.toggle_lbl.master.winfo_children()[0].config(
                text="Non hai un account?")

        self._auto_size()

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _make_entry(self, parent, placeholder, show=None):
        """Crea un Entry con placeholder e highlight al focus."""
        frame = tk.Frame(parent, bg=ENTRY_BG,
                         highlightthickness=1, highlightbackground=ENTRY_BD)
        frame.pack(fill="x", pady=(4, 0))

        e = tk.Entry(frame, font=self.f_entry, bg=ENTRY_BG, fg=TEXT_LIGHT,
                     relief="flat", bd=0, insertbackground=TEXT_DARK,
                     show="")
        e.pack(fill="x", padx=10, pady=8)
        e.placeholder        = placeholder
        e.showing_placeholder = True
        e.real_show          = show
        e.container_frame    = frame
        e.insert(0, placeholder)

        def on_focus_in(_):
            if e.showing_placeholder:
                e.delete(0, "end")
                e.config(fg=TEXT_DARK)
                if e.real_show:
                    e.config(show=e.real_show)
                e.showing_placeholder = False
            frame.config(highlightbackground=ACCENT)

        def on_focus_out(_):
            if e.get() == "":
                if e.real_show:
                    e.config(show="")
                e.insert(0, e.placeholder)
                e.config(fg=TEXT_LIGHT)
                e.showing_placeholder = True
            frame.config(highlightbackground=ENTRY_BD)

        e.bind("<FocusIn>",  on_focus_in)
        e.bind("<FocusOut>", on_focus_out)
        return e

    def _reset_entry(self, entry: tk.Entry, placeholder: str, show):
        """Riporta un Entry allo stato placeholder pulito."""
        entry.config(show="")
        entry.delete(0, "end")
        entry.insert(0, placeholder)
        entry.config(fg=TEXT_LIGHT)
        entry.showing_placeholder = True
        entry.real_show = show
        entry.container_frame.config(highlightbackground=ENTRY_BD)

    def _get_value(self, entry: tk.Entry) -> str:
        return "" if entry.showing_placeholder else entry.get().strip()

    def _show_msg(self, text: str, color: str = RED_ERR):
        self.lbl_msg.config(text=text, fg=color)

    def _auto_size(self):
        """Ridimensiona la finestra al contenuto e la ricentra."""
        self.update_idletasks()
        w = 460
        h = self.winfo_reqheight() + 10
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    # ── Azioni ────────────────────────────────────────────────────────────────
    def _on_main_action(self):
        email = self._get_value(self.entry_email)
        pwd   = self._get_value(self.entry_pwd)

        if self.mode == "login":
            if not email or not pwd:
                self._show_msg("Inserisci email e password per continuare.")
                return
            # TODO: logica autenticazione
            self._show_msg("✓ Login in corso…", color=BTN_READER_FG)

        else:
            name    = self._get_value(self.entry_name)
            confirm = self._get_value(self.entry_confirm)
            if not name or not email or not pwd or not confirm:
                self._show_msg("Compila tutti i campi per registrarti.")
                return
            if pwd != confirm:
                self._show_msg("Le password non coincidono.")
                return
            # TODO: logica registrazione
            self._show_msg("✓ Registrazione in corso…", color=BTN_READER_FG)

    def _on_enter_as_reader(self):
        # TODO: aprire schermata lettore
        self._show_msg("Apertura schermata lettore…", color=BTN_READER_FG)


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = RingraziamentiApp()
    app.mainloop()
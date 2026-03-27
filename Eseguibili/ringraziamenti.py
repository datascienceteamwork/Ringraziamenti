import tkinter as tk
from tkinter import font as tkfont


# ── Palette ──────────────────────────────────────────────────────────────────
BG          = "#F7F3EE"          # avorio caldo
CARD_BG     = "#FFFFFF"
ACCENT      = "#7C6A55"          # marrone caldo
ACCENT_DARK = "#5C4D3C"
ACCENT_LIGHT= "#C4AD94"
TEXT_DARK   = "#2E2219"
TEXT_MID    = "#7A6652"
TEXT_LIGHT  = "#B5A392"
ENTRY_BG    = "#F0EBE3"
ENTRY_BD    = "#D6C9B8"
BTN_READER  = "#E8F0E9"
BTN_READER_FG = "#3A6B40"
RED_ERR     = "#C0392B"

RADIUS = 12   # usato per simulare bordi arrotondati con padding


class RingraziamentiApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ringraziamenti")
        self.resizable(False, False)
        self.configure(bg=BG)

        # ── Fonts ────────────────────────────────────────────────────────────
        self.f_title   = tkfont.Font(family="Georgia",      size=26, weight="bold")
        self.f_sub     = tkfont.Font(family="Georgia",      size=11, slant="italic")
        self.f_label   = tkfont.Font(family="Helvetica",    size=10, weight="bold")
        self.f_entry   = tkfont.Font(family="Helvetica",    size=11)
        self.f_btn     = tkfont.Font(family="Helvetica",    size=11, weight="bold")
        self.f_link    = tkfont.Font(family="Helvetica",    size=10, underline=True)
        self.f_small   = tkfont.Font(family="Helvetica",    size=9)
        self.f_mode    = tkfont.Font(family="Helvetica",    size=10)

        # stato: "login" | "register"
        self.mode = tk.StringVar(value="login")

        self._build_ui()
        self._center_window(460, 620)

    # ── Layout principale ─────────────────────────────────────────────────────
    def _build_ui(self):
        # Wrapper esterno con padding
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
        card = tk.Frame(outer, bg=CARD_BG, bd=0,
                        highlightthickness=1, highlightbackground=ENTRY_BD)
        card.pack(fill="x", pady=(0, 16))

        inner = tk.Frame(card, bg=CARD_BG)
        inner.pack(fill="both", expand=True, padx=28, pady=24)

        # Titolo card + toggle switch
        header_row = tk.Frame(inner, bg=CARD_BG)
        header_row.pack(fill="x", pady=(0, 18))

        self.card_title = tk.Label(header_row, text="Accedi al tuo account",
                                   font=tkfont.Font(family="Helvetica", size=14, weight="bold"),
                                   bg=CARD_BG, fg=TEXT_DARK)
        self.card_title.pack(side="left")

        # Toggle pill  [Login | Registrati]
        pill = tk.Frame(header_row, bg=ENTRY_BG,
                        highlightthickness=1, highlightbackground=ENTRY_BD)
        pill.pack(side="right")

        self.btn_to_login = tk.Label(pill, text="Accedi", font=self.f_mode,
                                     bg=ACCENT, fg="white", cursor="hand2",
                                     padx=10, pady=4)
        self.btn_to_login.pack(side="left")
        self.btn_to_login.bind("<Button-1>", lambda e: self._switch_mode("login"))

        self.btn_to_reg = tk.Label(pill, text="Registrati", font=self.f_mode,
                                   bg=ENTRY_BG, fg=TEXT_MID, cursor="hand2",
                                   padx=10, pady=4)
        self.btn_to_reg.pack(side="left")
        self.btn_to_reg.bind("<Button-1>", lambda e: self._switch_mode("register"))

        # ── Campi ─────────────────────────────────────────────────────────────
        self.fields_frame = tk.Frame(inner, bg=CARD_BG)
        self.fields_frame.pack(fill="x")

        # Campo Nome (solo registrazione)
        self.name_block = tk.Frame(self.fields_frame, bg=CARD_BG)
        tk.Label(self.name_block, text="NOME COMPLETO",
                 font=self.f_label, bg=CARD_BG, fg=TEXT_MID).pack(anchor="w")
        self.entry_name = self._make_entry(self.name_block, "Es. Mario Rossi")
        self.name_block.pack(fill="x", pady=(0, 12))      # visibile di default,
        self.name_block.pack_forget()                       # nascosto in login

        # Campo Email
        email_block = tk.Frame(self.fields_frame, bg=CARD_BG)
        email_block.pack(fill="x", pady=(0, 12))
        tk.Label(email_block, text="EMAIL",
                 font=self.f_label, bg=CARD_BG, fg=TEXT_MID).pack(anchor="w")
        self.entry_email = self._make_entry(email_block, "Es. mario@email.com")

        # Campo Password
        pwd_block = tk.Frame(self.fields_frame, bg=CARD_BG)
        pwd_block.pack(fill="x", pady=(0, 6))
        tk.Label(pwd_block, text="PASSWORD",
                 font=self.f_label, bg=CARD_BG, fg=TEXT_MID).pack(anchor="w")
        self.entry_pwd = self._make_entry(pwd_block, "••••••••", show="•")

        # Conferma password (solo registrazione)
        self.confirm_block = tk.Frame(self.fields_frame, bg=CARD_BG)
        tk.Label(self.confirm_block, text="CONFERMA PASSWORD",
                 font=self.f_label, bg=CARD_BG, fg=TEXT_MID).pack(anchor="w")
        self.entry_confirm = self._make_entry(self.confirm_block, "••••••••", show="•")
        self.confirm_block.pack(fill="x", pady=(0, 6))
        self.confirm_block.pack_forget()

        # Link "Password dimenticata" (solo login)
        self.forgot_frame = tk.Frame(inner, bg=CARD_BG)
        self.forgot_frame.pack(fill="x", pady=(0, 20))
        self.lbl_forgot = tk.Label(self.forgot_frame, text="Password dimenticata?",
                                   font=self.f_link, bg=CARD_BG, fg=ACCENT,
                                   cursor="hand2")
        self.lbl_forgot.pack(side="right")

        # Messaggio errore / info
        self.lbl_msg = tk.Label(inner, text="", font=self.f_small,
                                bg=CARD_BG, fg=RED_ERR, wraplength=360)
        self.lbl_msg.pack(fill="x", pady=(0, 8))

        # Bottone principale
        self.btn_main = tk.Button(inner, text="Accedi",
                                  font=self.f_btn,
                                  bg=ACCENT, fg="white",
                                  activebackground=ACCENT_DARK,
                                  activeforeground="white",
                                  relief="flat", bd=0, cursor="hand2",
                                  padx=0, pady=10,
                                  command=self._on_main_action)
        self.btn_main.pack(fill="x")

        # ── Separatore ────────────────────────────────────────────────────────
        sep_frame = tk.Frame(outer, bg=BG)
        sep_frame.pack(fill="x", pady=4)
        tk.Frame(sep_frame, bg=ACCENT_LIGHT, height=1).pack(fill="x",
                                                              side="left",
                                                              expand=True,
                                                              padx=(0, 8),
                                                              pady=6)
        tk.Label(sep_frame, text="oppure", font=self.f_small,
                 bg=BG, fg=TEXT_LIGHT).pack(side="left")
        tk.Frame(sep_frame, bg=ACCENT_LIGHT, height=1).pack(fill="x",
                                                              side="left",
                                                              expand=True,
                                                              padx=(8, 0),
                                                              pady=6)

        # ── Bottone Lettore ───────────────────────────────────────────────────
        reader_btn = tk.Button(outer,
                               text="📖  Entra come Lettore",
                               font=self.f_btn,
                               bg=BTN_READER, fg=BTN_READER_FG,
                               activebackground="#D6EAD8",
                               activeforeground=BTN_READER_FG,
                               relief="flat", bd=0, cursor="hand2",
                               padx=0, pady=10,
                               highlightthickness=1,
                               highlightbackground="#A8CCA9",
                               command=self._on_enter_as_reader)
        reader_btn.pack(fill="x")

        # Nota sotto
        tk.Label(outer,
                 text="Hai un codice di ringraziamento? Accedi qui.",
                 font=self.f_small, bg=BG, fg=TEXT_LIGHT).pack(pady=(6, 0))

    # ── Entry helper ──────────────────────────────────────────────────────────
    def _make_entry(self, parent, placeholder, show=None):
        ef = tk.Frame(parent, bg=ENTRY_BG,
                      highlightthickness=1, highlightbackground=ENTRY_BD)
        ef.pack(fill="x", pady=(4, 0))

        kwargs = dict(font=self.f_entry, bg=ENTRY_BG, fg=TEXT_LIGHT,
                      relief="flat", bd=0, insertbackground=TEXT_DARK)
        if show:
            kwargs["show"] = ""          # mostra placeholder senza asterischi
        e = tk.Entry(ef, **kwargs)
        e.pack(fill="x", padx=10, pady=8)
        e.placeholder = placeholder
        e.showing_placeholder = True
        e.real_show = show              # carattere di mascheratura reale

        # Inserisci placeholder
        e.insert(0, placeholder)

        def on_focus_in(event):
            if e.showing_placeholder:
                e.delete(0, "end")
                e.config(fg=TEXT_DARK)
                if e.real_show:
                    e.config(show=e.real_show)
                e.showing_placeholder = False

        def on_focus_out(event):
            if e.get() == "":
                if e.real_show:
                    e.config(show="")
                e.insert(0, e.placeholder)
                e.config(fg=TEXT_LIGHT)
                e.showing_placeholder = True

        def on_enter(event):
            ef.config(highlightbackground=ACCENT)

        def on_leave(event):
            ef.config(highlightbackground=ENTRY_BD)

        e.bind("<FocusIn>",  on_focus_in)
        e.bind("<FocusOut>", on_focus_out)
        e.bind("<Enter>",    on_enter)
        e.bind("<Leave>",    on_leave)
        return e

    # ── Switch Login / Register ───────────────────────────────────────────────
    def _switch_mode(self, mode: str):
        self.lbl_msg.config(text="")
        if mode == self.mode.get():
            return
        self.mode.set(mode)

        if mode == "register":
            # mostra campi extra
            self.name_block.pack(fill="x", pady=(0, 12), before=self.fields_frame.winfo_children()[1]
                                  if len(self.fields_frame.winfo_children()) > 1
                                  else None)
            # repack nell'ordine corretto: nome, email, pwd, conferma
            for w in self.fields_frame.winfo_children():
                w.pack_forget()
            self.name_block.pack(fill="x", pady=(0, 12))
            # email (secondo figlio originale)
            self.fields_frame.winfo_children()[1].pack(fill="x", pady=(0, 12))
            # pwd
            self.fields_frame.winfo_children()[2].pack(fill="x", pady=(0, 6))
            # conferma
            self.confirm_block.pack(fill="x", pady=(0, 6))

            self.forgot_frame.pack_forget()
            self.btn_main.config(text="Crea account")
            self.card_title.config(text="Crea il tuo account")
            # pill
            self.btn_to_login.config(bg=ENTRY_BG, fg=TEXT_MID)
            self.btn_to_reg.config(bg=ACCENT, fg="white")

        else:  # login
            for w in self.fields_frame.winfo_children():
                w.pack_forget()
            self.name_block.pack_forget()
            self.confirm_block.pack_forget()
            # email + pwd
            self.fields_frame.winfo_children()[1].pack(fill="x", pady=(0, 12))
            self.fields_frame.winfo_children()[2].pack(fill="x", pady=(0, 6))

            self.forgot_frame.pack(fill="x", pady=(0, 20))
            self.btn_main.config(text="Accedi")
            self.card_title.config(text="Accedi al tuo account")
            # pill
            self.btn_to_login.config(bg=ACCENT, fg="white")
            self.btn_to_reg.config(bg=ENTRY_BG, fg=TEXT_MID)

        # Aggiorna finestra
        self.update_idletasks()
        self._center_window(460, 620 if mode == "login" else 680)

    # ── Azioni placeholder ────────────────────────────────────────────────────
    def _on_main_action(self):
        email = self._get_value(self.entry_email)
        pwd   = self._get_value(self.entry_pwd)

        if self.mode.get() == "login":
            if not email or not pwd:
                self._show_msg("Inserisci email e password per continuare.")
                return
            # TODO: logica di autenticazione
            self._show_msg("✓ Login in corso…", color=BTN_READER_FG)

        else:  # register
            name    = self._get_value(self.entry_name)
            confirm = self._get_value(self.entry_confirm)
            if not name or not email or not pwd or not confirm:
                self._show_msg("Compila tutti i campi per registrarti.")
                return
            if pwd != confirm:
                self._show_msg("Le password non coincidono.")
                return
            # TODO: logica di registrazione
            self._show_msg("✓ Registrazione in corso…", color=BTN_READER_FG)

    def _on_enter_as_reader(self):
        # TODO: aprire la schermata del lettore
        self._show_msg("Apertura schermata lettore…", color=BTN_READER_FG)

    # ── Utility ───────────────────────────────────────────────────────────────
    def _get_value(self, entry: tk.Entry) -> str:
        if entry.showing_placeholder:
            return ""
        return entry.get().strip()

    def _show_msg(self, text: str, color: str = RED_ERR):
        self.lbl_msg.config(text=text, fg=color)

    def _center_window(self, w: int, h: int):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x  = (sw - w) // 2
        y  = (sh - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = RingraziamentiApp()
    app.mainloop()
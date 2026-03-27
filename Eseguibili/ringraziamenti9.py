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

        # "login" | "register"
        self.mode = "login"

        # Calcola area disponibile sottraendo un margine fisso per la taskbar
        TASKBAR_MARGIN = 80
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        win_w = 460
        win_h = screen_h - TASKBAR_MARGIN
        x = (screen_w - win_w) // 2
        self.geometry(f"{win_w}x{win_h}+{x}+0")

        self._build_ui()

    # ── UI principale ─────────────────────────────────────────────────────────
    def _build_ui(self):
        root_frame = tk.Frame(self, bg=BG)
        root_frame.pack(fill="both", expand=True, padx=30)

        # Spazio flessibile superiore
        tk.Frame(root_frame, bg=BG).pack(fill="both", expand=True)

        # ── Header ────────────────────────────────────────────────────────────
        header = tk.Frame(root_frame, bg=BG)
        header.pack(fill="x")

        tk.Label(header, text="✉",
                 font=tkfont.Font(size=36),
                 bg=BG, fg=ACCENT).pack(pady=(0, 4))
        tk.Label(header, text="Ringraziamenti",
                 font=self.f_title, bg=BG, fg=TEXT_DARK).pack()
        tk.Label(header, text="Condividi la tua gratitudine con chi ami",
                 font=self.f_sub, bg=BG, fg=TEXT_MID).pack(pady=(2, 20))

        # ── Card ──────────────────────────────────────────────────────────────
        card = tk.Frame(root_frame, bg=CARD_BG,
                        highlightthickness=1, highlightbackground=ENTRY_BD)
        card.pack(fill="x")

        inner = tk.Frame(card, bg=CARD_BG)
        inner.pack(fill="both", expand=True, padx=28, pady=24)

        # Titolo card
        self.card_title = tk.Label(
            inner, text="Accedi al tuo account",
            font=tkfont.Font(family="Helvetica", size=14, weight="bold"),
            bg=CARD_BG, fg=TEXT_DARK, anchor="w")
        self.card_title.pack(fill="x", pady=(0, 18))

        # ── Contenitore campi ─────────────────────────────────────────────────
        fields = tk.Frame(inner, bg=CARD_BG)
        fields.pack(fill="x")

        # Nome (solo registrazione) — inizialmente nascosto
        self.name_block = tk.Frame(fields, bg=CARD_BG)
        tk.Label(self.name_block, text="NOME COMPLETO",
                 font=self.f_label, bg=CARD_BG, fg=TEXT_MID).pack(anchor="w")
        self.entry_name = self._make_entry(self.name_block, "Es. Mario Rossi")

        # Email
        self.email_block = tk.Frame(fields, bg=CARD_BG)
        self.email_block.pack(fill="x", pady=(0, 12))
        tk.Label(self.email_block, text="EMAIL",
                 font=self.f_label, bg=CARD_BG, fg=TEXT_MID).pack(anchor="w")
        self.entry_email = self._make_entry(self.email_block, "Es. mario@email.com")

        # Password
        self.pwd_block = tk.Frame(fields, bg=CARD_BG)
        self.pwd_block.pack(fill="x", pady=(0, 6))
        tk.Label(self.pwd_block, text="PASSWORD",
                 font=self.f_label, bg=CARD_BG, fg=TEXT_MID).pack(anchor="w")
        self.entry_pwd = self._make_entry(self.pwd_block, "••••••••", show="•")

        # Conferma password (solo registrazione) — inizialmente nascosto
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

        # Bottone principale
        self.btn_main = tk.Button(
            inner, text="Accedi",
            font=self.f_btn,
            bg=ACCENT, fg="white",
            activebackground=ACCENT_DARK, activeforeground="white",
            relief="flat", bd=0, cursor="hand2",
            pady=10, command=self._on_main_action)
        self.btn_main.pack(fill="x", pady=(0, 16))

        # Toggle Accedi / Registrati
        toggle_row = tk.Frame(inner, bg=CARD_BG)
        toggle_row.pack(fill="x")
        self.toggle_question = tk.Label(
            toggle_row, text="Non hai un account?",
            font=self.f_small, bg=CARD_BG, fg=TEXT_LIGHT)
        self.toggle_question.pack(side="left")
        self.toggle_lbl = tk.Label(
            toggle_row, text=" Registrati",
            font=tkfont.Font(family="Helvetica", size=10,
                             weight="bold", underline=True),
            bg=CARD_BG, fg=ACCENT, cursor="hand2")
        self.toggle_lbl.pack(side="left")
        self.toggle_lbl.bind("<Button-1>", lambda e: self._switch_mode())

        # Spazio flessibile centrale
        tk.Frame(root_frame, bg=BG).pack(fill="both", expand=True)

        # ── Separatore "oppure" + bottone Lettore (visibili solo in login) ────
        self.reader_section = tk.Frame(root_frame, bg=BG)
        self.reader_section.pack(fill="x", pady=(0, 20))

        # Separatore
        sep = tk.Frame(self.reader_section, bg=BG)
        sep.pack(fill="x", pady=(0, 10))
        tk.Frame(sep, bg=ACCENT_LIGHT, height=1).pack(
            fill="x", side="left", expand=True, padx=(0, 8), pady=6)
        tk.Label(sep, text="oppure", font=self.f_small,
                 bg=BG, fg=TEXT_LIGHT).pack(side="left")
        tk.Frame(sep, bg=ACCENT_LIGHT, height=1).pack(
            fill="x", side="left", expand=True, padx=(8, 0), pady=6)

        # Bottone lettore
        tk.Button(
            self.reader_section,
            text="📖  Entra come Lettore",
            font=self.f_btn,
            bg=BTN_READER, fg=BTN_READER_FG,
            activebackground="#D6EAD8", activeforeground=BTN_READER_FG,
            relief="flat", bd=0, cursor="hand2",
            pady=12,
            highlightthickness=1, highlightbackground="#A8CCA9",
            command=self._on_enter_as_reader
        ).pack(fill="x")

        tk.Label(self.reader_section,
                 text="Hai un codice di ringraziamento? Accedi qui.",
                 font=self.f_small, bg=BG, fg=TEXT_LIGHT).pack(pady=(6, 0))

        # Spazio flessibile inferiore
        tk.Frame(root_frame, bg=BG).pack(fill="both", expand=True)

    # ── Switch Login ↔ Register ───────────────────────────────────────────────
    def _switch_mode(self):
        self.lbl_msg.config(text="")

        # Rimuove il focus da qualsiasi Entry
        self.focus_set()

        # Pulisce tutti i campi
        self._reset_entry(self.entry_name,    "Es. Mario Rossi",     show=None)
        self._reset_entry(self.entry_email,   "Es. mario@email.com", show=None)
        self._reset_entry(self.entry_pwd,     "••••••••",            show="•")
        self._reset_entry(self.entry_confirm, "••••••••",            show="•")

        if self.mode == "login":
            # → Registrazione
            self.mode = "register"
            self.card_title.config(text="Crea il tuo account")
            self.btn_main.config(text="Crea account")

            self.name_block.pack_forget()
            self.email_block.pack_forget()
            self.pwd_block.pack_forget()
            self.confirm_block.pack_forget()

            self.name_block.pack(fill="x", pady=(0, 12))
            self.email_block.pack(fill="x", pady=(0, 12))
            self.pwd_block.pack(fill="x", pady=(0, 6))
            self.confirm_block.pack(fill="x", pady=(0, 6))

            self.forgot_frame.pack_forget()
            self.toggle_question.config(text="Hai già un account?")
            self.toggle_lbl.config(text=" Accedi")

            # Nasconde separatore e bottone lettore
            self.reader_section.pack_forget()

        else:
            # → Login
            self.mode = "login"
            self.card_title.config(text="Accedi al tuo account")
            self.btn_main.config(text="Accedi")

            self.name_block.pack_forget()
            self.email_block.pack_forget()
            self.pwd_block.pack_forget()
            self.confirm_block.pack_forget()

            self.email_block.pack(fill="x", pady=(0, 12))
            self.pwd_block.pack(fill="x", pady=(0, 6))

            self.forgot_frame.pack(fill="x", pady=(4, 14),
                                   before=self.lbl_msg)
            self.toggle_question.config(text="Non hai un account?")
            self.toggle_lbl.config(text=" Registrati")

            # Mostra separatore e bottone lettore
            self.reader_section.pack(fill="x", pady=(0, 20),
                                     before=self.reader_section.master.winfo_children()[-1])

    # ── Entry con placeholder ─────────────────────────────────────────────────
    def _make_entry(self, parent, placeholder, show=None):
        frame = tk.Frame(parent, bg=ENTRY_BG,
                         highlightthickness=1, highlightbackground=ENTRY_BD)
        frame.pack(fill="x", pady=(4, 0))

        e = tk.Entry(frame, font=self.f_entry,
                     bg=ENTRY_BG, fg=TEXT_LIGHT,
                     relief="flat", bd=0,
                     insertbackground=TEXT_DARK, show="")
        e.pack(fill="x", padx=10, pady=8)
        e.placeholder         = placeholder
        e.showing_placeholder = True
        e.real_show           = show
        e.container_frame     = frame
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
        entry.config(show="")
        entry.delete(0, "end")
        entry.insert(0, placeholder)
        entry.config(fg=TEXT_LIGHT)
        entry.showing_placeholder = True
        entry.real_show           = show
        entry.container_frame.config(highlightbackground=ENTRY_BD)

    def _get_value(self, entry: tk.Entry) -> str:
        return "" if entry.showing_placeholder else entry.get().strip()

    def _show_msg(self, text: str, color: str = RED_ERR):
        self.lbl_msg.config(text=text, fg=color)

    # ── Azioni ────────────────────────────────────────────────────────────────
    def _on_main_action(self):
        email = self._get_value(self.entry_email)
        pwd   = self._get_value(self.entry_pwd)

        if self.mode == "login":
            if not email or not pwd:
                self._show_msg("Inserisci email e password per continuare.")
                return
            # TODO: logica autenticazione reale
            # Per ora accediamo direttamente alla schermata dello scrittore
            self.withdraw()
            WriterWindow(self, nome_scrittore=email.split("@")[0].capitalize())

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
        """Nasconde la finestra di login e apre la finestra lettore."""
        self.withdraw()
        ReaderWindow(self)


# ── Finestra Scrittore ───────────────────────────────────────────────────────
class WriterWindow(tk.Toplevel):
    def __init__(self, login_win: "RingraziamentiApp", nome_scrittore: str):
        super().__init__()
        self.login_win      = login_win
        self.nome_scrittore = nome_scrittore
        self.title("Ringraziamenti – Scrittore")
        self.resizable(False, False)
        self.configure(bg=BG)
        self.geometry(login_win.geometry())

        self.f_title  = tkfont.Font(family="Georgia",   size=26, weight="bold")
        self.f_sub    = tkfont.Font(family="Georgia",   size=11, slant="italic")
        self.f_name   = tkfont.Font(family="Georgia",   size=18, weight="bold")
        self.f_btn    = tkfont.Font(family="Helvetica", size=11, weight="bold")
        self.f_desc   = tkfont.Font(family="Helvetica", size=9)
        self.f_small  = tkfont.Font(family="Helvetica", size=9)

        self.protocol("WM_DELETE_WINDOW", self._on_logout)
        self._build_ui()

    # ── UI ────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        root = tk.Frame(self, bg=BG)
        root.pack(fill="both", expand=True, padx=30)

        # Spazio superiore
        tk.Frame(root, bg=BG).pack(fill="both", expand=True)

        # ── Header ────────────────────────────────────────────────────────────
        tk.Label(root, text="✍",
                 font=tkfont.Font(size=36),
                 bg=BG, fg=ACCENT).pack(pady=(0, 4))
        tk.Label(root, text="Ringraziamenti",
                 font=self.f_title, bg=BG, fg=TEXT_DARK).pack()
        tk.Label(root,
                 text=f"Bentornato, {self.nome_scrittore}!",
                 font=self.f_name, bg=BG, fg=ACCENT).pack(pady=(10, 2))
        tk.Label(root,
                 text="Cosa vuoi fare oggi?",
                 font=self.f_sub, bg=BG, fg=TEXT_MID).pack(pady=(0, 28))

        # ── Card azioni ───────────────────────────────────────────────────────
        card = tk.Frame(root, bg=CARD_BG,
                        highlightthickness=1, highlightbackground=ENTRY_BD)
        card.pack(fill="x")

        inner = tk.Frame(card, bg=CARD_BG)
        inner.pack(fill="both", expand=True, padx=28, pady=28)

        # Bottone: Nuovo ringraziamento
        new_btn_frame = tk.Frame(inner, bg=CARD_BG)
        new_btn_frame.pack(fill="x", pady=(0, 14))

        tk.Button(
            new_btn_frame,
            text="✉   Scrivi un nuovo ringraziamento",
            font=self.f_btn,
            bg=ACCENT, fg="white",
            activebackground=ACCENT_DARK, activeforeground="white",
            relief="flat", bd=0, cursor="hand2",
            pady=14,
            command=self._on_new   # TODO: aprire form di inserimento
        ).pack(fill="x")

        tk.Label(new_btn_frame,
                 text="Crea un nuovo testo e genera il codice da condividere.",
                 font=self.f_desc, bg=CARD_BG, fg=TEXT_LIGHT).pack(pady=(5, 0))

        # Separatore
        tk.Frame(inner, bg=ENTRY_BD, height=1).pack(fill="x", pady=(4, 14))

        # Bottone: Visualizza ringraziamenti
        list_btn_frame = tk.Frame(inner, bg=CARD_BG)
        list_btn_frame.pack(fill="x")

        tk.Button(
            list_btn_frame,
            text="📋   Visualizza i tuoi ringraziamenti",
            font=self.f_btn,
            bg=BTN_READER, fg=BTN_READER_FG,
            activebackground="#D6EAD8", activeforeground=BTN_READER_FG,
            relief="flat", bd=0, cursor="hand2",
            pady=14,
            highlightthickness=1, highlightbackground="#A8CCA9",
            command=self._on_list   # TODO: aprire lista ringraziamenti
        ).pack(fill="x")

        tk.Label(list_btn_frame,
                 text="Consulta i ringraziamenti già inseriti e i loro codici.",
                 font=self.f_desc, bg=CARD_BG, fg=TEXT_LIGHT).pack(pady=(5, 0))

        # ── Bottone logout ────────────────────────────────────────────────────
        tk.Button(root,
                  text="← Esci e torna al login",
                  font=self.f_btn,
                  bg=ENTRY_BG, fg=TEXT_MID,
                  activebackground=ENTRY_BD, activeforeground=TEXT_DARK,
                  relief="flat", bd=0, cursor="hand2",
                  pady=10,
                  command=self._on_logout).pack(fill="x", pady=(24, 0))

        # Spazio inferiore
        tk.Frame(root, bg=BG).pack(fill="both", expand=True)

    # ── Azioni ────────────────────────────────────────────────────────────────
    def _on_new(self):
        # TODO: aprire la schermata di inserimento nuovo ringraziamento
        pass

    def _on_list(self):
        # TODO: aprire la schermata con la lista dei ringraziamenti
        pass

    def _on_logout(self):
        self.destroy()
        self.login_win.deiconify()


# ── Finestra Lettore ──────────────────────────────────────────────────────────
class ReaderWindow(tk.Toplevel):
    def __init__(self, login_win: RingraziamentiApp):
        super().__init__()
        self.login_win = login_win
        self.title("Ringraziamenti – Lettore")
        self.resizable(False, False)
        self.configure(bg=BG)

        # Stesse dimensioni della finestra di login
        geo = login_win.geometry()          # "WxH+X+Y"
        self.geometry(geo)

        # Fonts (ridefiniti localmente per indipendenza)
        self.f_title  = tkfont.Font(family="Georgia",   size=26, weight="bold")
        self.f_sub    = tkfont.Font(family="Georgia",   size=11, slant="italic")
        self.f_label  = tkfont.Font(family="Helvetica", size=10, weight="bold")
        self.f_entry  = tkfont.Font(family="Helvetica", size=11)
        self.f_btn    = tkfont.Font(family="Helvetica", size=11, weight="bold")
        self.f_small  = tkfont.Font(family="Helvetica", size=9)
        self.f_body   = tkfont.Font(family="Georgia",   size=12)
        self.f_thanks = tkfont.Font(family="Georgia",   size=13, slant="italic")

        # Intercetta la chiusura tramite [X] per tornare al login
        self.protocol("WM_DELETE_WINDOW", self._on_back)

        self._build_ui()

    # ── UI ────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        root = tk.Frame(self, bg=BG)
        root.pack(fill="both", expand=True, padx=30)

        # Spazio superiore
        tk.Frame(root, bg=BG).pack(fill="both", expand=True)

        # ── Header ────────────────────────────────────────────────────────────
        tk.Label(root, text="📖",
                 font=tkfont.Font(size=36),
                 bg=BG, fg=ACCENT).pack(pady=(0, 4))
        tk.Label(root, text="Ringraziamenti",
                 font=self.f_title, bg=BG, fg=TEXT_DARK).pack()
        tk.Label(root, text="Benvenuto! Sei pronto a leggere i tuoi ringraziamenti.",
                 font=self.f_sub, bg=BG, fg=TEXT_MID,
                 wraplength=380, justify="center").pack(pady=(4, 20))

        # ── Card form ─────────────────────────────────────────────────────────
        card = tk.Frame(root, bg=CARD_BG,
                        highlightthickness=1, highlightbackground=ENTRY_BD)
        card.pack(fill="x")

        inner = tk.Frame(card, bg=CARD_BG)
        inner.pack(fill="both", expand=True, padx=28, pady=24)

        tk.Label(inner, text="Inserisci i tuoi dati",
                 font=tkfont.Font(family="Helvetica", size=14, weight="bold"),
                 bg=CARD_BG, fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(0, 18))

        # Email scrittore
        email_block = tk.Frame(inner, bg=CARD_BG)
        email_block.pack(fill="x", pady=(0, 12))
        tk.Label(email_block, text="EMAIL DELLO SCRITTORE",
                 font=self.f_label, bg=CARD_BG, fg=TEXT_MID).pack(anchor="w")
        self.entry_email = self._make_entry(email_block, "Es. mario@email.com")

        # Codice ringraziamento
        code_block = tk.Frame(inner, bg=CARD_BG)
        code_block.pack(fill="x", pady=(0, 6))
        tk.Label(code_block, text="CODICE DI RINGRAZIAMENTO",
                 font=self.f_label, bg=CARD_BG, fg=TEXT_MID).pack(anchor="w")
        self.entry_code = self._make_entry(code_block, "Es. ABC-12345")

        # Messaggio errore
        self.lbl_msg = tk.Label(inner, text="", font=self.f_small,
                                bg=CARD_BG, fg=RED_ERR, wraplength=360)
        self.lbl_msg.pack(fill="x", pady=(10, 8))

        # Bottone Conferma
        tk.Button(inner, text="Leggi i ringraziamenti",
                  font=self.f_btn,
                  bg=ACCENT, fg="white",
                  activebackground=ACCENT_DARK, activeforeground="white",
                  relief="flat", bd=0, cursor="hand2",
                  pady=10, command=self._on_confirm).pack(fill="x", pady=(0, 10))

        # Bottone Torna al login
        tk.Button(inner, text="← Torna al login",
                  font=self.f_btn,
                  bg=ENTRY_BG, fg=TEXT_MID,
                  activebackground=ENTRY_BD, activeforeground=TEXT_DARK,
                  relief="flat", bd=0, cursor="hand2",
                  pady=10, command=self._on_back).pack(fill="x")

        # Spazio inferiore
        tk.Frame(root, bg=BG).pack(fill="both", expand=True)

    # ── Azioni ────────────────────────────────────────────────────────────────
    def _on_confirm(self):
        email = self._get_value(self.entry_email)
        code  = self._get_value(self.entry_code)

        if not email or not code:
            self.lbl_msg.config(
                text="Inserisci l'email dello scrittore e il codice.", fg=RED_ERR)
            return

        # TODO: sostituire con la vera logica di ricerca nel database
        # Simulazione: qualsiasi email + codice valido apre la finestra del testo
        destinatario = email.split("@")[0].capitalize()
        testo_esempio = (
            "Grazie di cuore per esserci stato in ogni momento importante di questo "
            "percorso. Il tuo supporto, la tua pazienza e la tua amicizia hanno reso "
            "tutto più leggero e significativo. Questo traguardo è anche un po' tuo."
        )
        autore = "Mario Rossi"   # TODO: ricavare dal database

        self.lbl_msg.config(text="")
        self.withdraw()
        ThanksWindow(self, destinatario=destinatario,
                     testo=testo_esempio, autore=autore)

    def _on_back(self):
        """Chiude la finestra lettore e ripristina il login."""
        self.destroy()
        self.login_win.deiconify()

    # ── Entry con placeholder (identica alla classe principale) ───────────────
    def _make_entry(self, parent, placeholder, show=None):
        frame = tk.Frame(parent, bg=ENTRY_BG,
                         highlightthickness=1, highlightbackground=ENTRY_BD)
        frame.pack(fill="x", pady=(4, 0))

        e = tk.Entry(frame, font=self.f_entry,
                     bg=ENTRY_BG, fg=TEXT_LIGHT,
                     relief="flat", bd=0,
                     insertbackground=TEXT_DARK, show="")
        e.pack(fill="x", padx=10, pady=8)
        e.placeholder         = placeholder
        e.showing_placeholder = True
        e.real_show           = show
        e.container_frame     = frame
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

    def _get_value(self, entry: tk.Entry) -> str:
        return "" if entry.showing_placeholder else entry.get().strip()


# ── Finestra Ringraziamento ───────────────────────────────────────────────────
class ThanksWindow(tk.Toplevel):
    def __init__(self, reader_win, destinatario: str, testo: str, autore: str):
        super().__init__()
        self.reader_win = reader_win
        self.title("Ringraziamenti – Il tuo messaggio")
        self.resizable(False, False)
        self.configure(bg=BG)

        self.geometry(reader_win.geometry())

        self.f_title  = tkfont.Font(family="Georgia",   size=26, weight="bold")
        self.f_sub    = tkfont.Font(family="Georgia",   size=11, slant="italic")
        self.f_name   = tkfont.Font(family="Georgia",   size=20, weight="bold")
        self.f_btn    = tkfont.Font(family="Helvetica", size=11, weight="bold")
        self.f_thanks = tkfont.Font(family="Georgia",   size=13, slant="italic")

        self.protocol("WM_DELETE_WINDOW", self._on_back)
        self._build_ui(destinatario, testo, autore)

    def _build_ui(self, destinatario: str, testo: str, autore: str):
        root = tk.Frame(self, bg=BG)
        root.pack(fill="both", expand=True, padx=30)

        tk.Frame(root, bg=BG).pack(fill="both", expand=True)

        # Icona + titolo app
        tk.Label(root, text="\u2709",
                 font=tkfont.Font(size=36),
                 bg=BG, fg=ACCENT).pack(pady=(0, 4))
        tk.Label(root, text="Ringraziamenti",
                 font=self.f_title, bg=BG, fg=TEXT_DARK).pack()

        # Nome destinatario
        tk.Label(root, text=f"Ciao, {destinatario}!",
                 font=self.f_name, bg=BG, fg=ACCENT).pack(pady=(14, 2))
        tk.Label(root, text="Hai ricevuto un messaggio di ringraziamento.",
                 font=self.f_sub, bg=BG, fg=TEXT_MID).pack(pady=(0, 20))

        # Card testo — dimensioni fisse, bordo card
        card = tk.Frame(root, bg=CARD_BG,
                        highlightthickness=1, highlightbackground=ENTRY_BD)
        card.pack(fill="x")

        # Padding superiore dentro la card
        tk.Frame(card, bg=CARD_BG, height=20).pack(fill="x")

        # Virgolette decorative
        tk.Label(card, text="\u201c",
                 font=tkfont.Font(family="Georgia", size=48),
                 bg=CARD_BG, fg=ACCENT_LIGHT, anchor="w",
                 padx=28).pack(fill="x")

        # ── Area di scorrimento a dimensioni fisse ────────────────────────────
        # Contenitore che fissa l'altezza massima visibile del testo
        scroll_container = tk.Frame(card, bg=CARD_BG, height=220)
        scroll_container.pack(fill="x", padx=28)
        scroll_container.pack_propagate(False)   # blocca espansione verticale

        # Scrollbar verticale
        scrollbar = tk.Scrollbar(scroll_container, orient="vertical",
                                 bg=ENTRY_BG, troughcolor=ENTRY_BD,
                                 activebackground=ACCENT_LIGHT,
                                 highlightthickness=0, bd=0)
        scrollbar.pack(side="right", fill="y")

        # Text widget — sola lettura, sfondo card, testo giustificato
        txt = tk.Text(scroll_container,
                      font=self.f_thanks,
                      bg=CARD_BG, fg=TEXT_DARK,
                      relief="flat", bd=0,
                      wrap="word",
                      cursor="arrow",
                      spacing1=4, spacing3=4,
                      yscrollcommand=scrollbar.set)
        txt.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=txt.yview)

        # Inserisce il testo con tag per l'allineamento giustificato
        txt.tag_configure("justified", justify="center")
        txt.insert("1.0", testo, "justified")
        txt.config(state="disabled")   # sola lettura

        # Linea separatrice + firma
        sep_frame = tk.Frame(card, bg=CARD_BG)
        sep_frame.pack(fill="x", padx=28, pady=(16, 0))
        tk.Frame(sep_frame, bg=ENTRY_BD, height=1).pack(fill="x")
        tk.Label(sep_frame, text=f"\u2014 {autore}",
                 font=tkfont.Font(family="Helvetica", size=10, slant="italic"),
                 bg=CARD_BG, fg=TEXT_LIGHT, anchor="e").pack(fill="x", pady=(10, 0))

        # Padding inferiore dentro la card
        tk.Frame(card, bg=CARD_BG, height=20).pack(fill="x")

        # Bottone torna alla form
        tk.Button(root, text="\u2190 Torna all'inserimento del codice",
                  font=self.f_btn,
                  bg=ENTRY_BG, fg=TEXT_MID,
                  activebackground=ENTRY_BD, activeforeground=TEXT_DARK,
                  relief="flat", bd=0, cursor="hand2",
                  pady=10, command=self._on_back).pack(fill="x", pady=(20, 0))

        tk.Frame(root, bg=BG).pack(fill="both", expand=True)

    def _on_back(self):
        self.destroy()
        self.reader_win.deiconify()


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = RingraziamentiApp()
    app.mainloop()
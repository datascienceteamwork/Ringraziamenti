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
        self.reset_login()
        self.withdraw()
        ReaderWindow(self)

    def reset_login(self):
        """Resetta tutti i campi e i messaggi della schermata di login."""
        self.focus_set()
        self._reset_entry(self.entry_name,    "Es. Mario Rossi",     show=None)
        self._reset_entry(self.entry_email,   "Es. mario@email.com", show=None)
        self._reset_entry(self.entry_pwd,     "••••••••",            show="•")
        self._reset_entry(self.entry_confirm, "••••••••",            show="•")
        self.lbl_msg.config(text="")
        # Torna sempre alla modalità login
        if self.mode == "register":
            self._switch_mode()


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
        self.withdraw()
        NewThanksWindow(self)

    def _on_list(self):
        self.withdraw()
        ListWindow(self)

    def _on_logout(self):
        self.destroy()
        self.login_win.reset_login()
        self.login_win.deiconify()

# ── Dati fittizi ─────────────────────────────────────────────────────────────
SAMPLE_THANKS = [
    {
        "id": 1,
        "destinatario": "Luca Bianchi",
        "data": "10 mar 2026",
        "codice": "GRZ-48271",
        "testo": (
            "Luca, grazie per essere stato al mio fianco in ogni momento difficile "
            "di questi anni universitari. La tua amicizia è stata la mia ancora. "
            "Questo traguardo è anche tuo. Luca, grazie per essere stato al mio fianco in ogni momento difficile "
            "di questi anni universitari. La tua amicizia è stata la mia ancora. "
            "Questo traguardo è anche tuo. Luca, grazie per essere stato al mio fianco in ogni momento difficile "
            "di questi anni universitari. La tua amicizia è stata la mia ancora. "
            "Questo traguardo è anche tuo. Luca, grazie per essere stato al mio fianco in ogni momento difficile "
            "di questi anni universitari. La tua amicizia è stata la mia ancora. "
            "Questo traguardo è anche tuo. Luca, grazie per essere stato al mio fianco in ogni momento difficile "
            "di questi anni universitari. La tua amicizia è stata la mia ancora. "
            "Questo traguardo è anche tuo. Luca, grazie per essere stato al mio fianco in ogni momento difficile "
            "di questi anni universitari. La tua amicizia è stata la mia ancora. "
            "Questo traguardo è anche tuo. Luca, grazie per essere stato al mio fianco in ogni momento difficile "
            "di questi anni universitari. La tua amicizia è stata la mia ancora. "
            "Questo traguardo è anche tuo. Luca, grazie per essere stato al mio fianco in ogni momento difficile "
            "di questi anni universitari. La tua amicizia è stata la mia ancora. "
            "Questo traguardo è anche tuo. Luca, grazie per essere stato al mio fianco in ogni momento difficile "
            "di questi anni universitari. La tua amicizia è stata la mia ancora. "
            "Questo traguardo è anche tuo."
        ),
    },
    {
        "id": 2,
        "destinatario": "Sara Esposito",
        "data": "11 mar 2026",
        "codice": "GRZ-93014",
        "testo": (
            "Sara, non avrei mai superato gli esami di analisi senza le tue spiegazioni "
            "pazienti e i tuoi appunti meravigliosi. Sei una persona straordinaria."
        ),
    },
    {
        "id": 3,
        "destinatario": "Marco e Giulia Ferretti",
        "data": "12 mar 2026",
        "codice": "GRZ-61539",
        "testo": (
            "Mamma e papà, ogni sacrificio che avete fatto per me ha avuto un senso. "
            "Vi dedico questa laurea con tutto l'amore che ho. Grazie di tutto."
        ),
    },
    {
        "id": 4,
        "destinatario": "Prof. Alessandra Conti",
        "data": "13 mar 2026",
        "codice": "GRZ-27804",
        "testo": (
            "Professoressa Conti, la sua guida durante la tesi è stata preziosa. "
            "Ha creduto in questo progetto anche quando io dubitavo. Grazie di cuore."
        ),
    },
    {
        "id": 5,
        "destinatario": "Gruppo studio ingegneria",
        "data": "14 mar 2026",
        "codice": "GRZ-55190",
        "testo": (
            "A tutto il gruppo: Riccardo, Valentina, Dario e Noemi. "
            "Cinque anni di notti in biblioteca, pizza fredda e risate. "
            "Non avrei voluto viverli con nessun altro."
        ),
    },
]


# ── Finestra Lista Ringraziamenti ─────────────────────────────────────────────
class ListWindow(tk.Toplevel):
    def __init__(self, writer_win):
        super().__init__()
        self.writer_win = writer_win
        self.title("Ringraziamenti – I tuoi messaggi")
        self.resizable(False, False)
        self.configure(bg=BG)
        self.geometry(writer_win.geometry())

        self.f_title    = tkfont.Font(family="Georgia",   size=26, weight="bold")
        self.f_sub      = tkfont.Font(family="Georgia",   size=11, slant="italic")
        self.f_btn      = tkfont.Font(family="Helvetica", size=11, weight="bold")
        self.f_card_name= tkfont.Font(family="Helvetica", size=12, weight="bold")
        self.f_card_meta= tkfont.Font(family="Helvetica", size=9)
        self.f_code     = tkfont.Font(family="Courier",   size=10, weight="bold")

        self.protocol("WM_DELETE_WINDOW", self._on_back)
        self._build_ui()

    def _build_ui(self):
        # ── Barra superiore fissa ─────────────────────────────────────────────
        top_bar = tk.Frame(self, bg=CARD_BG,
                           highlightthickness=1, highlightbackground=ENTRY_BD)
        top_bar.pack(fill="x")

        top_inner = tk.Frame(top_bar, bg=CARD_BG)
        top_inner.pack(fill="x", padx=24, pady=16)

        tk.Label(top_inner, text="✍  Ringraziamenti",
                 font=self.f_title, bg=CARD_BG, fg=TEXT_DARK).pack(side="left")

        # Sottotitolo
        sub_bar = tk.Frame(self, bg=BG)
        sub_bar.pack(fill="x", padx=24, pady=(12, 6))
        tk.Label(sub_bar,
                 text=f"Hai scritto {len(SAMPLE_THANKS)} ringraziamenti",
                 font=self.f_sub, bg=BG, fg=TEXT_MID).pack(side="left")

        # ── Area scrollabile ──────────────────────────────────────────────────
        container = tk.Frame(self, bg=BG)
        container.pack(fill="both", expand=True, padx=24, pady=(0, 0))

        scrollbar = tk.Scrollbar(container, orient="vertical")
        canvas = tk.Canvas(container, bg=BG, highlightthickness=0,
                           yscrollcommand=scrollbar.set)
        scrollbar.config(command=canvas.yview)

        # Scrollbar a destra, canvas occupa il resto — nessuna sovrapposizione
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self._scroll_frame = tk.Frame(canvas, bg=BG)

        # La finestra interna nel canvas deve allargarsi quanto il canvas
        def _on_canvas_resize(event):
            canvas.itemconfig(win_id, width=event.width)

        win_id = canvas.create_window((0, 0), window=self._scroll_frame, anchor="nw")
        canvas.bind("<Configure>", _on_canvas_resize)

        self._scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Mousewheel
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))

        # Popola la lista
        for item in SAMPLE_THANKS:
            self._make_card(self._scroll_frame, item)

        # ── Bottone indietro fisso in fondo ───────────────────────────────────
        bottom_bar = tk.Frame(self, bg=BG,
                              highlightthickness=1, highlightbackground=ENTRY_BD)
        bottom_bar.pack(fill="x", side="bottom")

        tk.Button(bottom_bar, text="← Torna alla schermata scrittore",
                  font=self.f_btn, bg=ENTRY_BG, fg=TEXT_MID,
                  activebackground=ENTRY_BD, activeforeground=TEXT_DARK,
                  relief="flat", bd=0, cursor="hand2",
                  pady=12, command=self._on_back).pack(fill="x", padx=24, pady=12)

    def _make_card(self, parent, item: dict):
        """Costruisce la card di un singolo ringraziamento."""
        outer = tk.Frame(parent, bg=CARD_BG,
                         highlightthickness=1, highlightbackground=ENTRY_BD,
                         cursor="hand2")
        outer.pack(fill="x", pady=(0, 10))

        inner = tk.Frame(outer, bg=CARD_BG)
        inner.pack(fill="x", padx=20, pady=16)

        # Riga superiore: nome + data
        top = tk.Frame(inner, bg=CARD_BG)
        top.pack(fill="x")

        tk.Label(top, text=f"✉  {item['destinatario']}",
                 font=self.f_card_name, bg=CARD_BG, fg=TEXT_DARK).pack(side="left")
        tk.Label(top, text=item["data"],
                 font=self.f_card_meta, bg=CARD_BG, fg=TEXT_LIGHT).pack(side="right")

        # Anteprima testo (max ~80 caratteri)
        anteprima = item["testo"][:82] + "…" if len(item["testo"]) > 82 else item["testo"]
        tk.Label(inner, text=anteprima,
                 font=tkfont.Font(family="Georgia", size=10, slant="italic"),
                 bg=CARD_BG, fg=TEXT_MID,
                 wraplength=360, justify="left", anchor="w").pack(fill="x", pady=(6, 8))

        # Riga inferiore: codice + freccia
        bottom = tk.Frame(inner, bg=CARD_BG)
        bottom.pack(fill="x")

        code_pill = tk.Frame(bottom, bg=ENTRY_BG,
                             highlightthickness=1, highlightbackground=ENTRY_BD)
        code_pill.pack(side="left")
        tk.Label(code_pill, text=item["codice"],
                 font=self.f_code, bg=ENTRY_BG, fg=ACCENT,
                 padx=8, pady=2).pack()

        tk.Label(bottom, text="Vedi dettagli  →",
                 font=self.f_card_meta, bg=CARD_BG, fg=ACCENT,
                 cursor="hand2").pack(side="right")

        # Linea separatrice decorativa
        tk.Frame(inner, bg=ENTRY_BD, height=1).pack(fill="x", pady=(10, 0))

        # Hover effect
        def on_enter(_):
            outer.config(highlightbackground=ACCENT)
        def on_leave(_):
            outer.config(highlightbackground=ENTRY_BD)
        def on_click(_):
            self.withdraw()
            DetailWindow(self, item)

        for widget in [outer, inner, top, bottom]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", on_click)
        for child in inner.winfo_children():
            child.bind("<Enter>", on_enter)
            child.bind("<Leave>", on_leave)
            child.bind("<Button-1>", on_click)

    def _on_back(self):
        self.destroy()
        self.writer_win.deiconify()


# ── Finestra Dettaglio Ringraziamento ─────────────────────────────────────────
class DetailWindow(tk.Toplevel):
    def __init__(self, list_win: "ListWindow", item: dict):
        super().__init__()
        self.list_win = list_win
        self.title("Ringraziamenti – Dettaglio")
        self.resizable(False, False)
        self.configure(bg=BG)
        self.geometry(list_win.geometry())

        self.f_title    = tkfont.Font(family="Georgia",   size=26, weight="bold")
        self.f_sub      = tkfont.Font(family="Georgia",   size=11, slant="italic")
        self.f_btn      = tkfont.Font(family="Helvetica", size=11, weight="bold")
        self.f_dest     = tkfont.Font(family="Georgia",   size=18, weight="bold")
        self.f_thanks   = tkfont.Font(family="Georgia",   size=13, slant="italic")
        self.f_meta     = tkfont.Font(family="Helvetica", size=9)
        self.f_code     = tkfont.Font(family="Courier",   size=18, weight="bold")

        self.protocol("WM_DELETE_WINDOW", self._on_back)
        self._build_ui(item)

    def _build_ui(self, item: dict):
        # ── Header fisso in cima ──────────────────────────────────────────────
        top_bar = tk.Frame(self, bg=CARD_BG,
                           highlightthickness=1, highlightbackground=ENTRY_BD)
        top_bar.pack(fill="x")

        top_inner = tk.Frame(top_bar, bg=CARD_BG)
        top_inner.pack(fill="x", padx=24, pady=16)

        tk.Label(top_inner, text="\u2709  Ringraziamenti",
                 font=self.f_title, bg=CARD_BG, fg=TEXT_DARK).pack(side="left")

        sub_bar = tk.Frame(self, bg=BG)
        sub_bar.pack(fill="x", padx=24, pady=(12, 6))
        tk.Label(sub_bar,
                 text=f"Per {item['destinatario']}  \u00b7  {item['data']}",
                 font=self.f_sub, bg=BG, fg=TEXT_MID).pack(side="left")

        # ── Area scorrevole centrale ──────────────────────────────────────────
        container = tk.Frame(self, bg=BG)
        container.pack(fill="both", expand=True, padx=24)

        scrollbar = tk.Scrollbar(container, orient="vertical")
        canvas = tk.Canvas(container, bg=BG, highlightthickness=0,
                           yscrollcommand=scrollbar.set)
        scrollbar.config(command=canvas.yview)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        scroll_frame = tk.Frame(canvas, bg=BG)

        def _on_canvas_resize(event):
            canvas.itemconfig(win_id, width=event.width)

        win_id = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.bind("<Configure>", _on_canvas_resize)
        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))

        # Card contenuto
        inner_pad = tk.Frame(scroll_frame, bg=BG)
        inner_pad.pack(fill="x", pady=12)

        card = tk.Frame(inner_pad, bg=CARD_BG,
                        highlightthickness=1, highlightbackground=ENTRY_BD)
        card.pack(fill="x")

        inner = tk.Frame(card, bg=CARD_BG)
        inner.pack(fill="both", expand=True, padx=28, pady=28)

        # Nome destinatario centrato
        tk.Label(inner, text=item["destinatario"],
                 font=self.f_dest, bg=CARD_BG, fg=ACCENT,
                 anchor="center", justify="center").pack(fill="x")

        tk.Frame(inner, bg=ENTRY_BD, height=1).pack(fill="x", pady=(10, 16))

        # Virgolette + testo centrato
        tk.Label(inner, text="\u201c",
                 font=tkfont.Font(family="Georgia", size=42),
                 bg=CARD_BG, fg=ACCENT_LIGHT, anchor="center").pack(fill="x")

        tk.Label(inner, text=item["testo"],
                 font=self.f_thanks, bg=CARD_BG, fg=TEXT_DARK,
                 wraplength=340, justify="center", anchor="center").pack(fill="x")

        tk.Frame(inner, bg=ENTRY_BD, height=1).pack(fill="x", pady=(20, 14))

        # Codice centrato
        code_row = tk.Frame(inner, bg=CARD_BG)
        code_row.pack(fill="x")
        tk.Label(code_row, text="CODICE DA CONDIVIDERE",
                 font=tkfont.Font(family="Helvetica", size=9, weight="bold"),
                 bg=CARD_BG, fg=TEXT_MID, anchor="center").pack(fill="x")
        code_pill = tk.Frame(code_row, bg=ENTRY_BG,
                             highlightthickness=1, highlightbackground=ACCENT_LIGHT)
        code_pill.pack(anchor="center", pady=(8, 0))
        tk.Label(code_pill, text=item["codice"],
                 font=self.f_code, bg=ENTRY_BG, fg=ACCENT,
                 padx=16, pady=8).pack()

        # ── Bottone indietro fisso in fondo ───────────────────────────────────
        bottom_bar = tk.Frame(self, bg=BG,
                              highlightthickness=1, highlightbackground=ENTRY_BD)
        bottom_bar.pack(fill="x", side="bottom")
        tk.Button(bottom_bar, text="\u2190 Torna alla lista",
                  font=self.f_btn, bg=ENTRY_BG, fg=TEXT_MID,
                  activebackground=ENTRY_BD, activeforeground=TEXT_DARK,
                  relief="flat", bd=0, cursor="hand2",
                  pady=12, command=self._on_back).pack(fill="x", padx=24, pady=12)


    def _on_back(self):
        self.destroy()
        self.list_win.deiconify()


# ── Finestra Nuovo Ringraziamento ─────────────────────────────────────────────
class NewThanksWindow(tk.Toplevel):
    def __init__(self, writer_win):
        super().__init__()
        self.writer_win = writer_win
        self.title("Ringraziamenti – Nuovo messaggio")
        self.resizable(False, False)
        self.configure(bg=BG)
        self.geometry(writer_win.geometry())

        self.f_title  = tkfont.Font(family="Georgia",   size=26, weight="bold")
        self.f_sub    = tkfont.Font(family="Georgia",   size=11, slant="italic")
        self.f_label  = tkfont.Font(family="Helvetica", size=10, weight="bold")
        self.f_entry  = tkfont.Font(family="Helvetica", size=11)
        self.f_btn    = tkfont.Font(family="Helvetica", size=11, weight="bold")
        self.f_small  = tkfont.Font(family="Helvetica", size=9)

        self.protocol("WM_DELETE_WINDOW", self._on_back)
        self._build_ui()

    def _build_ui(self):
        root = tk.Frame(self, bg=BG)
        root.pack(fill="both", expand=True, padx=30)

        tk.Frame(root, bg=BG).pack(fill="both", expand=True)

        tk.Label(root, text="\u270d",
                 font=tkfont.Font(size=36), bg=BG, fg=ACCENT).pack(pady=(0, 4))
        tk.Label(root, text="Ringraziamenti",
                 font=self.f_title, bg=BG, fg=TEXT_DARK).pack()
        tk.Label(root, text="Scrivi il tuo messaggio di ringraziamento",
                 font=self.f_sub, bg=BG, fg=TEXT_MID).pack(pady=(2, 20))

        card = tk.Frame(root, bg=CARD_BG,
                        highlightthickness=1, highlightbackground=ENTRY_BD)
        card.pack(fill="x")

        inner = tk.Frame(card, bg=CARD_BG)
        inner.pack(fill="both", expand=True, padx=28, pady=24)

        tk.Label(inner, text="Nuovo ringraziamento",
                 font=tkfont.Font(family="Helvetica", size=14, weight="bold"),
                 bg=CARD_BG, fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(0, 18))

        # Destinatario
        dest_block = tk.Frame(inner, bg=CARD_BG)
        dest_block.pack(fill="x", pady=(0, 14))
        tk.Label(dest_block, text="NOME DEL DESTINATARIO",
                 font=self.f_label, bg=CARD_BG, fg=TEXT_MID).pack(anchor="w")
        self.entry_dest = self._make_entry(dest_block, "Es. Luca Bianchi")

        # Messaggio
        msg_block = tk.Frame(inner, bg=CARD_BG)
        msg_block.pack(fill="x", pady=(0, 6))
        tk.Label(msg_block, text="MESSAGGIO",
                 font=self.f_label, bg=CARD_BG, fg=TEXT_MID).pack(anchor="w")

        self._text_frame = tk.Frame(msg_block, bg=ENTRY_BG,
                                    highlightthickness=1, highlightbackground=ENTRY_BD)
        self._text_frame.pack(fill="x", pady=(4, 0))

        self.text_msg = tk.Text(
            self._text_frame, font=self.f_entry,
            bg=ENTRY_BG, fg=TEXT_LIGHT,
            relief="flat", bd=0, insertbackground=TEXT_DARK,
            wrap="word", height=6, padx=10, pady=8)
        self.text_msg.pack(fill="x")
        self.text_msg.insert("1.0", "Scrivi qui il tuo messaggio\u2026")
        self._text_placeholder = True

        def text_focus_in(_):
            if self._text_placeholder:
                self.text_msg.delete("1.0", "end")
                self.text_msg.config(fg=TEXT_DARK)
                self._text_placeholder = False
            self._text_frame.config(highlightbackground=ACCENT)

        def text_focus_out(_):
            if self.text_msg.get("1.0", "end").strip() == "":
                self.text_msg.delete("1.0", "end")
                self.text_msg.insert("1.0", "Scrivi qui il tuo messaggio\u2026")
                self.text_msg.config(fg=TEXT_LIGHT)
                self._text_placeholder = True
            self._text_frame.config(highlightbackground=ENTRY_BD)

        self.text_msg.bind("<FocusIn>",  text_focus_in)
        self.text_msg.bind("<FocusOut>", text_focus_out)

        # Messaggio errore
        self.lbl_msg = tk.Label(inner, text="", font=self.f_small,
                                bg=CARD_BG, fg=RED_ERR, wraplength=360)
        self.lbl_msg.pack(fill="x", pady=(10, 8))

        tk.Button(inner, text="\u2709  Invia ringraziamento",
                  font=self.f_btn, bg=ACCENT, fg="white",
                  activebackground=ACCENT_DARK, activeforeground="white",
                  relief="flat", bd=0, cursor="hand2",
                  pady=10, command=self._on_confirm).pack(fill="x", pady=(0, 10))

        tk.Button(inner, text="\u2190 Torna alla schermata scrittore",
                  font=self.f_btn, bg=ENTRY_BG, fg=TEXT_MID,
                  activebackground=ENTRY_BD, activeforeground=TEXT_DARK,
                  relief="flat", bd=0, cursor="hand2",
                  pady=10, command=self._on_back).pack(fill="x")

        tk.Frame(root, bg=BG).pack(fill="both", expand=True)

    @staticmethod
    def _genera_codice() -> str:
        import random, string
        lettere = "".join(random.choices(string.ascii_uppercase, k=3))
        numeri  = "".join(random.choices(string.digits, k=5))
        return f"{lettere}-{numeri}"

    def _on_confirm(self):
        destinatario = self._get_entry(self.entry_dest)
        testo = "" if self._text_placeholder else self.text_msg.get("1.0", "end").strip()

        if not destinatario:
            self.lbl_msg.config(text="Inserisci il nome del destinatario.", fg=RED_ERR)
            return
        if not testo:
            self.lbl_msg.config(text="Scrivi il testo del messaggio.", fg=RED_ERR)
            return

        self.lbl_msg.config(text="")
        codice = self._genera_codice()
        # TODO: salvare destinatario, testo e codice nel database
        self._mostra_popup_codice(destinatario, codice)

    def _mostra_popup_codice(self, destinatario: str, codice: str):
        popup = tk.Toplevel(self)
        popup.title("Ringraziamento salvato!")
        popup.resizable(False, False)
        popup.configure(bg=CARD_BG)
        popup.grab_set()

        self.update_idletasks()
        pw, ph = 360, 300
        gx = self.winfo_x() + (self.winfo_width()  - pw) // 2
        gy = self.winfo_y() + (self.winfo_height() - ph) // 2
        popup.geometry(f"{pw}x{ph}+{gx}+{gy}")

        f_pop_title = tkfont.Font(family="Helvetica", size=13, weight="bold")
        f_pop_sub   = tkfont.Font(family="Helvetica", size=10)
        f_pop_code  = tkfont.Font(family="Courier",   size=22, weight="bold")
        f_pop_btn   = tkfont.Font(family="Helvetica", size=11, weight="bold")

        outer = tk.Frame(popup, bg=CARD_BG)
        outer.pack(fill="both", expand=True, padx=28, pady=24)

        tk.Label(outer, text="\u2705  Ringraziamento salvato!",
                 font=f_pop_title, bg=CARD_BG, fg=BTN_READER_FG).pack(pady=(0, 10))

        tk.Label(outer,
                 text=f"Il tuo messaggio per {destinatario} \u00e8 stato creato.\nCondividi questo codice con il destinatario:",
                 font=f_pop_sub, bg=CARD_BG, fg=TEXT_MID,
                 wraplength=300, justify="center").pack()

        code_frame = tk.Frame(outer, bg=ENTRY_BG,
                              highlightthickness=1, highlightbackground=ACCENT_LIGHT)
        code_frame.pack(pady=(16, 6))
        tk.Label(code_frame, text=codice,
                 font=f_pop_code, bg=ENTRY_BG, fg=ACCENT,
                 padx=24, pady=10).pack()

        tk.Label(outer,
                 text="Tienilo al sicuro: servirà al tuo amico per leggere il messaggio.",
                 font=tkfont.Font(family="Helvetica", size=8),
                 bg=CARD_BG, fg=TEXT_LIGHT,
                 wraplength=300, justify="center").pack(pady=(0, 16))

        def chiudi():
            popup.destroy()
            popup.destroy()
            self.destroy()
            self.writer_win.deiconify()
        tk.Button(outer, text="Chiudi",
                  font=f_pop_btn, bg=ACCENT, fg="white",
                  activebackground=ACCENT_DARK, activeforeground="white",
                  relief="flat", bd=0, cursor="hand2",
                  pady=8, padx=20, command=chiudi).pack()

        popup.protocol("WM_DELETE_WINDOW", chiudi)

    def _on_back(self):
        self.destroy()
        self.writer_win.deiconify()

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
                e.showing_placeholder = False
            frame.config(highlightbackground=ACCENT)

        def on_focus_out(_):
            if e.get() == "":
                e.insert(0, e.placeholder)
                e.config(fg=TEXT_LIGHT)
                e.showing_placeholder = True
            frame.config(highlightbackground=ENTRY_BD)

        e.bind("<FocusIn>",  on_focus_in)
        e.bind("<FocusOut>", on_focus_out)
        return e

    def _reset_entry(self, entry, placeholder, show):
        entry.config(show="")
        entry.delete(0, "end")
        entry.insert(0, placeholder)
        entry.config(fg=TEXT_LIGHT)
        entry.showing_placeholder = True
        entry.container_frame.config(highlightbackground=ENTRY_BD)

    def _get_entry(self, entry) -> str:
        return "" if entry.showing_placeholder else entry.get().strip()


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
        self.login_win.reset_login()
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
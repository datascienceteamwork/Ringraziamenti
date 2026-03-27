import tkinter as tk
from tkinter import font as tkfont
import threading
import os

# ── Firebase setup ────────────────────────────────────────────────────────────
try:
    import firebase_admin
    from firebase_admin import credentials, auth, firestore

    _CRED_PATH = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "progetto-data-science-genai-firebase-adminsdk-fbsvc-7527550776.json"
    )
    if not firebase_admin._apps:
        _cred = credentials.Certificate(_CRED_PATH)
        firebase_admin.initialize_app(_cred)
    _db = firestore.client()
    FIREBASE_OK = True
except Exception as _fb_err:
    FIREBASE_OK = False
    print(f"[Firebase] Inizializzazione fallita: {_fb_err}")

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


def _setup_smart_scroll(canvas):
    """
    Attiva lo scroll con rotellina solo quando il contenuto supera il viewport
    e solo quando il mouse è sopra il canvas. Rimuove il binding quando il
    canvas viene distrutto, evitando handler orfani.
    """
    def _on_mousewheel(event):
        # Scorri solo se il contenuto è più alto del viewport
        if canvas.bbox("all") and canvas.winfo_height() > 0:
            content_h = canvas.bbox("all")[3]
            view_h    = canvas.winfo_height()
            if content_h > view_h:
                canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def _bind_wheel(event=None):
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def _unbind_wheel(event=None):
        canvas.unbind_all("<MouseWheel>")

    def _on_destroy(event=None):
        canvas.unbind_all("<MouseWheel>")

    canvas.bind("<Enter>", _bind_wheel)
    canvas.bind("<Leave>", _unbind_wheel)
    canvas.bind("<Destroy>", _on_destroy)



def _readonly_text(parent, testo: str, font, bg=None, fg=None, justify="left"):
    """
    Crea un widget tk.Text in sola lettura che si espande esattamente quanto
    serve per mostrare tutto il contenuto, senza spazio extra e senza tagliare.
    Usa dlineinfo per misurare i pixel reali dell'ultima riga di testo.
    """
    if bg is None:
        bg = ENTRY_BG
    if fg is None:
        fg = TEXT_DARK

    txt = tk.Text(parent, font=font,
                  bg=bg, fg=fg,
                  relief="flat", bd=0,
                  wrap="word",
                  cursor="arrow",
                  spacing1=3, spacing3=3,
                  padx=12, pady=10,
                  highlightthickness=0,
                  height=1)
    txt.tag_configure("body", justify=justify)
    txt.insert("1.0", testo, "body")
    txt.config(state="disabled")

    def _fit_height(event=None):
        """
        Misura l'altezza reale in pixel dell'intero contenuto tramite dlineinfo,
        poi la converte nel numero esatto di righe da assegnare a height.
        """
        txt.update_idletasks()
        # Itera tutte le righe visualizzate e somma le loro altezze pixel
        total_px = 0
        idx = "1.0"
        while True:
            info = txt.dlineinfo(idx)
            if info is None:
                break
            total_px += info[3]          # info = (x, y, width, height, baseline)
            next_idx = txt.index(f"{idx} +1 display line")
            if next_idx == idx:          # nessun avanzamento → fine testo
                break
            idx = next_idx

        if total_px == 0:
            return

        # Ottieni l'altezza in pixel di una singola riga con la font corrente
        line_info = txt.dlineinfo("1.0")
        if line_info is None:
            return
        line_h = line_info[3]
        if line_h <= 0:
            return

        # Numero di righe = pixel totali / altezza singola riga (arrotondato su)
        import math
        n_lines = math.ceil(total_px / line_h)
        txt.config(height=max(n_lines, 1))

    txt.bind("<Configure>", _fit_height)
    return txt


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
            self._show_msg("Accesso in corso…", color=TEXT_MID)
            self.btn_main.config(state="disabled")
            threading.Thread(target=self._do_login,
                             args=(email, pwd), daemon=True).start()

        else:
            name    = self._get_value(self.entry_name)
            confirm = self._get_value(self.entry_confirm)
            if not name or not email or not pwd or not confirm:
                self._show_msg("Compila tutti i campi per registrarti.")
                return
            if pwd != confirm:
                self._show_msg("Le password non coincidono.")
                return
            self._show_msg("Registrazione in corso…", color=TEXT_MID)
            self.btn_main.config(state="disabled")
            threading.Thread(target=self._do_register,
                             args=(name, email, pwd), daemon=True).start()

    # ── Firebase: login ───────────────────────────────────────────────────────
    def _do_login(self, email: str, pwd: str):
        if not FIREBASE_OK:
            self.after(0, self._show_msg,
                       "Firebase non disponibile. Controlla la configurazione.")
            self.after(0, self.btn_main.config, {"state": "normal"})
            return
        try:
            # Verifica credenziali tramite Firebase Auth REST API
            import urllib.request, urllib.parse, json as _json

            api_key = self._get_api_key()
            url = (f"https://identitytoolkit.googleapis.com/v1/"
                   f"accounts:signInWithPassword?key={api_key}")
            payload = _json.dumps({
                "email": email,
                "password": pwd,
                "returnSecureToken": True
            }).encode()
            req = urllib.request.Request(url, data=payload,
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req) as resp:
                data = _json.loads(resp.read())
            uid = data["localId"]

            # Recupera il nome da Firestore
            doc = _db.collection("users").document(uid).get()
            nome = doc.to_dict().get("nome", email.split("@")[0].capitalize()) if doc.exists else email.split("@")[0].capitalize()

            self.after(0, self._login_success, uid, nome)

        except urllib.error.HTTPError as e:
            err_body = _json.loads(e.read())
            code = err_body.get("error", {}).get("message", "")
            if code in ("EMAIL_NOT_FOUND", "INVALID_PASSWORD", "INVALID_LOGIN_CREDENTIALS"):
                msg = "Email o password non corretti."
            elif code == "USER_DISABLED":
                msg = "Questo account è stato disabilitato."
            elif code == "TOO_MANY_ATTEMPTS_TRY_LATER":
                msg = "Troppi tentativi. Riprova più tardi."
            else:
                msg = f"Errore di accesso: {code}"
            self.after(0, self._show_msg, msg)
            self.after(0, self.btn_main.config, {"state": "normal"})
        except Exception as ex:
            self.after(0, self._show_msg, f"Errore: {ex}")
            self.after(0, self.btn_main.config, {"state": "normal"})

    def _login_success(self, uid: str, nome: str):
        self.btn_main.config(state="normal")
        self.lbl_msg.config(text="")
        self.withdraw()
        WriterWindow(self, uid=uid, nome_scrittore=nome)

    # ── Firebase: registrazione ───────────────────────────────────────────────
    def _do_register(self, name: str, email: str, pwd: str):
        if not FIREBASE_OK:
            self.after(0, self._show_msg,
                       "Firebase non disponibile. Controlla la configurazione.")
            self.after(0, self.btn_main.config, {"state": "normal"})
            return
        try:
            # Crea utente su Firebase Auth
            user = auth.create_user(email=email, password=pwd, display_name=name)
            uid  = user.uid

            # Salva su Firestore nella raccolta "users"
            _db.collection("users").document(uid).set({
                "email": email,
                "nome":  name,
            })

            self.after(0, self._register_success)

        except auth.EmailAlreadyExistsError:
            self.after(0, self._show_msg,
                       "Questa email è già registrata. Prova ad accedere.")
            self.after(0, self.btn_main.config, {"state": "normal"})
        except Exception as ex:
            self.after(0, self._show_msg, f"Errore durante la registrazione: {ex}")
            self.after(0, self.btn_main.config, {"state": "normal"})

    def _register_success(self):
        self.btn_main.config(state="normal")
        popup = tk.Toplevel(self)
        popup.title("Registrazione completata")
        popup.resizable(False, False)
        popup.configure(bg=CARD_BG)
        popup.grab_set()

        self.update_idletasks()
        pw, ph = 360, 220
        gx = self.winfo_x() + (self.winfo_width()  - pw) // 2
        gy = self.winfo_y() + (self.winfo_height() - ph) // 2
        popup.geometry(f"{pw}x{ph}+{gx}+{gy}")

        f_title = tkfont.Font(family="Helvetica", size=13, weight="bold")
        f_body  = tkfont.Font(family="Helvetica", size=10)
        f_btn   = tkfont.Font(family="Helvetica", size=11, weight="bold")

        outer = tk.Frame(popup, bg=CARD_BG)
        outer.pack(fill="both", expand=True, padx=28, pady=24)

        tk.Label(outer, text="\u2705  Registrazione completata!",
                 font=f_title, bg=CARD_BG, fg=BTN_READER_FG).pack(pady=(0, 10))
        tk.Label(outer,
                 text="Il tuo account è stato creato con successo.\nAdesso puoi accedere con le tue credenziali.",
                 font=f_body, bg=CARD_BG, fg=TEXT_MID,
                 wraplength=300, justify="center").pack(pady=(0, 20))

        def chiudi_e_torna():
            popup.destroy()
            self.reset_login()

        tk.Button(outer, text="Vai al login",
                  font=f_btn, bg=ACCENT, fg="white",
                  activebackground=ACCENT_DARK, activeforeground="white",
                  relief="flat", bd=0, cursor="hand2",
                  pady=8, padx=20, command=chiudi_e_torna).pack()

        popup.protocol("WM_DELETE_WINDOW", chiudi_e_torna)

    @staticmethod
    def _get_api_key() -> str:
        """Legge la Web API Key dal file delle credenziali Firebase."""
        import json as _json
        cred_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "progetto-data-science-genai-firebase-adminsdk-fbsvc-7527550776.json"
        )
        with open(cred_path, encoding="utf-8") as f:
            data = _json.load(f)
        # Il campo si chiama "api_key" nel service account
        # oppure può essere passato manualmente — adatta se necessario
        return data.get("api_key", data.get("web_api_key", ""))

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
    def __init__(self, login_win: "RingraziamentiApp", uid: str, nome_scrittore: str):
        super().__init__()
        self.login_win      = login_win
        self.uid            = uid
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
        NewThanksWindow(self, self.uid)

    def _on_list(self):
        self.withdraw()
        ListWindow(self, self.uid)

    def _on_logout(self):
        self.destroy()
        self.login_win.reset_login()
        self.login_win.deiconify()

# ── Finestra Lista Ringraziamenti ─────────────────────────────────────────────
class ListWindow(tk.Toplevel):
    def __init__(self, writer_win, uid: str):
        super().__init__()
        self.writer_win = writer_win
        self.uid        = uid
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
        # Avvia il caricamento dal DB in background
        threading.Thread(target=self._load_data, daemon=True).start()

    def _build_ui(self):
        # ── Barra superiore fissa ─────────────────────────────────────────────
        top_bar = tk.Frame(self, bg=CARD_BG,
                           highlightthickness=1, highlightbackground=ENTRY_BD)
        top_bar.pack(fill="x")

        top_inner = tk.Frame(top_bar, bg=CARD_BG)
        top_inner.pack(fill="x", padx=24, pady=16)

        tk.Label(top_inner, text="✍  Ringraziamenti",
                 font=self.f_title, bg=CARD_BG, fg=TEXT_DARK).pack(side="left")

        # Sottotitolo con contatore (aggiornato dopo il caricamento)
        sub_bar = tk.Frame(self, bg=BG)
        sub_bar.pack(fill="x", padx=24, pady=(12, 6))
        self._lbl_count = tk.Label(sub_bar, text="Caricamento in corso…",
                                   font=self.f_sub, bg=BG, fg=TEXT_MID)
        self._lbl_count.pack(side="left")

        # ── Bottone indietro fisso in fondo ───────────────────────────────────
        bottom_bar = tk.Frame(self, bg=BG,
                              highlightthickness=1, highlightbackground=ENTRY_BD)
        bottom_bar.pack(fill="x", side="bottom")
        tk.Button(bottom_bar, text="← Torna alla schermata scrittore",
                  font=self.f_btn, bg=ENTRY_BG, fg=TEXT_MID,
                  activebackground=ENTRY_BD, activeforeground=TEXT_DARK,
                  relief="flat", bd=0, cursor="hand2",
                  pady=12, command=self._on_back).pack(fill="x", padx=24, pady=12)

        # ── Area scrollabile ──────────────────────────────────────────────────
        container = tk.Frame(self, bg=BG)
        container.pack(fill="both", expand=True, padx=24, pady=(0, 0))

        scrollbar = tk.Scrollbar(container, orient="vertical")
        canvas = tk.Canvas(container, bg=BG, highlightthickness=0,
                           yscrollcommand=scrollbar.set)
        scrollbar.config(command=canvas.yview)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self._scroll_frame = tk.Frame(canvas, bg=BG)

        def _on_canvas_resize(event):
            canvas.itemconfig(win_id, width=event.width)

        win_id = canvas.create_window((0, 0), window=self._scroll_frame, anchor="nw")
        canvas.bind("<Configure>", _on_canvas_resize)

        self._scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        _setup_smart_scroll(canvas)

        # Placeholder visibile durante il caricamento
        self._lbl_loading = tk.Label(
            self._scroll_frame,
            text="Caricamento dei ringraziamenti…",
            font=self.f_sub, bg=BG, fg=TEXT_LIGHT)
        self._lbl_loading.pack(pady=40)

    def _load_data(self):
        """Recupera i ringraziamenti da Firestore in background."""
        if not FIREBASE_OK:
            self.after(0, self._lbl_count.config,
                       {"text": "Firebase non disponibile.", "fg": RED_ERR})
            self.after(0, self._lbl_loading.config,
                       {"text": "Impossibile connettersi al database."})
            return
        try:
            docs = (_db.collection("users")
                       .document(self.uid)
                       .collection("ringraziamenti")
                       .order_by("destinatario")
                       .get())
            items = []
            for doc in docs:
                d = doc.to_dict()
                # Converti timestamp Firestore in stringa leggibile, se presente
                ts = d.get("creato_il")
                if ts and hasattr(ts, "strftime"):
                    data_str = ts.strftime("%-d %b %Y")
                else:
                    data_str = ""
                items.append({
                    "id":           doc.id,
                    "destinatario": d.get("destinatario", ""),
                    "data":         data_str,
                    "codice":       d.get("codice", ""),
                    "testo":        d.get("testo", ""),
                    "risposta":     d.get("risposta", ""),
                    "visualizzato": d.get("visualizzato", False),
                })
            self.after(0, self._populate, items)
        except Exception as ex:
            self.after(0, self._lbl_count.config,
                       {"text": f"Errore: {ex}", "fg": RED_ERR})
            self.after(0, self._lbl_loading.config,
                       {"text": "Errore durante il caricamento."})

    def _populate(self, items: list):
        """Popola la lista nel thread UI dopo il caricamento."""
        # Rimuovi placeholder
        self._lbl_loading.destroy()

        n = len(items)
        testo_count = f"Hai scritto {n} ringraziamento" if n == 1 else f"Hai scritto {n} ringraziamenti"
        self._lbl_count.config(text=testo_count, fg=TEXT_MID)

        if not items:
            tk.Label(self._scroll_frame,
                     text="Non hai ancora scritto nessun ringraziamento.",
                     font=self.f_sub, bg=BG, fg=TEXT_LIGHT).pack(pady=40)
            return

        for item in items:
            self._make_card(self._scroll_frame, item)

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

        # Badge risposta ricevuta e/o visualizzato
        has_risposta    = bool(item.get("risposta", ""))
        has_visualizzato = item.get("visualizzato", False)

        if has_risposta or has_visualizzato:
            badge_row = tk.Frame(inner, bg=CARD_BG)
            badge_row.pack(fill="x", pady=(8, 0))

            if has_visualizzato:
                badge_v = tk.Frame(badge_row, bg="#EEF2FF",
                                   highlightthickness=1,
                                   highlightbackground="#B0B8E8")
                badge_v.pack(side="left")
                tk.Label(badge_v,
                         text="\U0001f441  Visualizzato",
                         font=tkfont.Font(family="Helvetica", size=8, weight="bold"),
                         bg="#EEF2FF", fg="#3A47A0",
                         padx=8, pady=3).pack()

            if has_risposta:
                badge_r = tk.Frame(badge_row, bg="#E8F0E9",
                                   highlightthickness=1,
                                   highlightbackground="#A8CCA9")
                badge_r.pack(side="left", padx=(6 if has_visualizzato else 0, 0))
                tk.Label(badge_r,
                         text="\U0001f4ac  Risposta ricevuta",
                         font=tkfont.Font(family="Helvetica", size=8, weight="bold"),
                         bg="#E8F0E9", fg=BTN_READER_FG,
                         padx=8, pady=3).pack()

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

    def refresh(self):
        """Svuota le card esistenti e ricarica i dati da Firestore."""
        for w in self._scroll_frame.winfo_children():
            w.destroy()
        self._lbl_count.config(text="Caricamento in corso…", fg=TEXT_MID)

        # Ricrea il placeholder di caricamento
        self._lbl_loading = tk.Label(
            self._scroll_frame,
            text="Aggiornamento in corso…",
            font=self.f_sub, bg=BG, fg=TEXT_LIGHT)
        self._lbl_loading.pack(pady=40)

        threading.Thread(target=self._load_data, daemon=True).start()


# ── Finestra Dettaglio Ringraziamento ─────────────────────────────────────────
class DetailWindow(tk.Toplevel):
    def __init__(self, list_win: "ListWindow", item: dict):
        super().__init__()
        self.list_win   = list_win
        self.item       = item          # dizionario corrente (mutabile)
        self.uid        = list_win.uid  # uid scrittore loggato
        self.title("Ringraziamenti – Dettaglio")
        self.resizable(False, False)
        self.configure(bg=BG)
        self.geometry(list_win.geometry())

        self.f_title    = tkfont.Font(family="Georgia",   size=26, weight="bold")
        self.f_sub      = tkfont.Font(family="Georgia",   size=11, slant="italic")
        self.f_btn      = tkfont.Font(family="Helvetica", size=11, weight="bold")
        self.f_label    = tkfont.Font(family="Helvetica", size=10, weight="bold")
        self.f_entry    = tkfont.Font(family="Helvetica", size=11)
        self.f_small    = tkfont.Font(family="Helvetica", size=9)
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
        _setup_smart_scroll(canvas)

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

        self._lbl_testo = tk.Label(inner, text=item["testo"],
                 font=self.f_thanks, bg=CARD_BG, fg=TEXT_DARK,
                 wraplength=340, justify="center", anchor="center")
        self._lbl_testo.pack(fill="x")

        # Bottone modifica testo (visibile solo se non ancora visualizzato)
        edit_row = tk.Frame(inner, bg=CARD_BG)
        edit_row.pack(fill="x", pady=(10, 0))

        if not item.get("visualizzato", False):
            self._btn_edit = tk.Button(
                edit_row,
                text="\u270f  Modifica testo",
                font=self.f_small,
                bg=ENTRY_BG, fg=TEXT_MID,
                activebackground=ENTRY_BD, activeforeground=TEXT_DARK,
                relief="flat", bd=0, cursor="hand2",
                padx=10, pady=5,
                command=self._on_edit_testo)
            self._btn_edit.pack(side="right")
        else:
            self._btn_edit = None   # non disponibile
            tk.Label(edit_row,
                     text="\U0001f512  Testo non modificabile: già visualizzato",
                     font=self.f_small, bg=CARD_BG, fg=TEXT_LIGHT).pack(side="right")

        # Contenitore form modifica (inizialmente nascosto)
        self._edit_frame = tk.Frame(inner, bg=CARD_BG)

        tk.Frame(inner, bg=ENTRY_BD, height=1).pack(fill="x", pady=(14, 14))

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

        # ── Sezione risposta del lettore ──────────────────────────────────────
        risposta = item.get("risposta", "")
        if risposta:
            resp_card = tk.Frame(inner_pad, bg=CARD_BG,
                                 highlightthickness=1, highlightbackground=ENTRY_BD)
            resp_card.pack(fill="x", pady=(14, 0))
            resp_inner = tk.Frame(resp_card, bg=CARD_BG)
            resp_inner.pack(fill="x", padx=28, pady=20)

            tk.Label(resp_inner,
                     text="\U0001f4ac  Risposta di " + item.get("destinatario", ""),
                     font=tkfont.Font(family="Helvetica", size=11, weight="bold"),
                     bg=CARD_BG, fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(0, 10))

            tk.Frame(resp_inner, bg=ENTRY_BD, height=1).pack(fill="x", pady=(0, 12))

            _readonly_text(resp_inner, risposta,
                          font=self.f_thanks, justify="center").pack(fill="x")

        # ── Bottone indietro fisso in fondo ───────────────────────────────────
        bottom_bar = tk.Frame(self, bg=BG,
                              highlightthickness=1, highlightbackground=ENTRY_BD)
        bottom_bar.pack(fill="x", side="bottom")
        tk.Button(bottom_bar, text="\u2190 Torna alla lista",
                  font=self.f_btn, bg=ENTRY_BG, fg=TEXT_MID,
                  activebackground=ENTRY_BD, activeforeground=TEXT_DARK,
                  relief="flat", bd=0, cursor="hand2",
                  pady=12, command=self._on_back).pack(fill="x", padx=24, pady=12)


    # ── Modifica testo ────────────────────────────────────────────────────────
    def _on_edit_testo(self):
        """Mostra la form inline di modifica sotto il testo."""
        # Svuota e ricostruisce la form ogni volta
        for w in self._edit_frame.winfo_children():
            w.destroy()
        self._edit_frame.pack(fill="x", pady=(8, 0))

        tk.Label(self._edit_frame, text="NUOVO TESTO",
                 font=self.f_label, bg=CARD_BG, fg=TEXT_MID).pack(anchor="w")

        text_frame = tk.Frame(self._edit_frame, bg=ENTRY_BG,
                              highlightthickness=1, highlightbackground=ENTRY_BD)
        text_frame.pack(fill="x", pady=(4, 0))
        self._txt_edit = tk.Text(
            text_frame,
            font=self.f_entry,
            bg=ENTRY_BG, fg=TEXT_DARK,
            relief="flat", bd=0, wrap="word",
            insertbackground=TEXT_DARK,
            height=5, padx=10, pady=8)
        self._txt_edit.pack(fill="x")
        self._txt_edit.insert("1.0", self.item["testo"])
        self._txt_edit.focus_set()

        self._lbl_edit_msg = tk.Label(
            self._edit_frame, text="",
            font=self.f_small, bg=CARD_BG, fg=RED_ERR, wraplength=340)
        self._lbl_edit_msg.pack(fill="x", pady=(6, 0))

        btn_row = tk.Frame(self._edit_frame, bg=CARD_BG)
        btn_row.pack(fill="x", pady=(8, 0))

        tk.Button(btn_row, text="Salva",
                  font=self.f_btn, bg=ACCENT, fg="white",
                  activebackground=ACCENT_DARK, activeforeground="white",
                  relief="flat", bd=0, cursor="hand2",
                  padx=18, pady=7,
                  command=self._on_salva_modifica).pack(side="left")

        tk.Button(btn_row, text="Annulla",
                  font=self.f_btn, bg=ENTRY_BG, fg=TEXT_MID,
                  activebackground=ENTRY_BD, activeforeground=TEXT_DARK,
                  relief="flat", bd=0, cursor="hand2",
                  padx=18, pady=7,
                  command=self._on_annulla_modifica).pack(side="left", padx=(10, 0))

        # Disabilita il bottone modifica mentre la form è aperta
        self._btn_edit.config(state="disabled")

    def _on_annulla_modifica(self):
        self._edit_frame.pack_forget()
        if self._btn_edit:
            self._btn_edit.config(state="normal")

    def _on_salva_modifica(self):
        nuovo_testo = self._txt_edit.get("1.0", "end").strip()
        if not nuovo_testo:
            self._lbl_edit_msg.config(text="Il testo non può essere vuoto.")
            return
        if nuovo_testo == self.item["testo"]:
            self._on_annulla_modifica()
            return
        self._lbl_edit_msg.config(text="Salvataggio in corso…", fg=TEXT_MID)
        self._txt_edit.config(state="disabled")
        if self._btn_edit:
            self._btn_edit.config(state="disabled")
        threading.Thread(
            target=self._do_salva_modifica,
            args=(nuovo_testo,), daemon=True).start()

    def _do_salva_modifica(self, nuovo_testo: str):
        if not FIREBASE_OK:
            self.after(0, self._lbl_edit_msg.config,
                       {"text": "Firebase non disponibile.", "fg": RED_ERR})
            self.after(0, self._txt_edit.config, {"state": "normal"})
            if self._btn_edit:
                self.after(0, self._btn_edit.config, {"state": "normal"})
            return
        try:
            (_db.collection("users")
                .document(self.uid)
                .collection("ringraziamenti")
                .document(self.item["id"])
                .update({"testo": nuovo_testo}))
            self.after(0, self._modifica_ok, nuovo_testo)
        except Exception as ex:
            self.after(0, self._lbl_edit_msg.config,
                       {"text": f"Errore: {ex}", "fg": RED_ERR})
            self.after(0, self._txt_edit.config, {"state": "normal"})
            self.after(0, self._btn_edit.config, {"state": "normal"})

    def _modifica_ok(self, nuovo_testo: str):
        # Aggiorna il dizionario locale e il label visibile
        self.item["testo"] = nuovo_testo
        self._lbl_testo.config(text=nuovo_testo)
        # Chiudi la form e riabilita il bottone
        self._on_annulla_modifica()

    def _on_back(self):
        self.destroy()
        self.list_win.deiconify()
        self.list_win.refresh()


# ── Finestra Nuovo Ringraziamento ─────────────────────────────────────────────
class NewThanksWindow(tk.Toplevel):
    def __init__(self, writer_win, uid: str):
        super().__init__()
        self.writer_win = writer_win
        self.uid = uid
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

        self.lbl_msg.config(text="Salvataggio in corso…", fg=TEXT_MID)
        self.focus_set()
        threading.Thread(
            target=self._do_salva,
            args=(destinatario, testo),
            daemon=True
        ).start()

    def _do_salva(self, destinatario: str, testo: str):
        """Genera un codice univoco per lo scrittore e salva su Firestore."""
        if not FIREBASE_OK:
            self.after(0, self.lbl_msg.config,
                       {"text": "Firebase non disponibile.", "fg": RED_ERR})
            return
        try:
            import random, string as _string

            ref = _db.collection("users").document(self.uid).collection("ringraziamenti")

            # Genera codice univoco tra quelli già presenti dello scrittore
            while True:
                lettere = "".join(random.choices(_string.ascii_uppercase, k=3))
                numeri  = "".join(random.choices(_string.digits, k=5))
                codice  = f"{lettere}-{numeri}"
                docs = ref.where("codice", "==", codice).limit(1).get()
                if not list(docs):
                    break

            ref.add({
                "codice":       codice,
                "destinatario": destinatario,
                "reazione":     "",
                "risposta":     "",
                "testo":        testo,
                "visualizzato": False,
            })

            self.after(0, self._salva_ok, destinatario, codice)

        except Exception as ex:
            self.after(0, self.lbl_msg.config,
                       {"text": f"Errore: {ex}", "fg": RED_ERR})

    def _salva_ok(self, destinatario: str, codice: str):
        self.lbl_msg.config(text="")
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
        self.btn_confirm = tk.Button(inner, text="Leggi i ringraziamenti",
                  font=self.f_btn,
                  bg=ACCENT, fg="white",
                  activebackground=ACCENT_DARK, activeforeground="white",
                  relief="flat", bd=0, cursor="hand2",
                  pady=10, command=self._on_confirm)
        self.btn_confirm.pack(fill="x", pady=(0, 10))

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

        self.lbl_msg.config(text="Ricerca in corso…", fg=TEXT_MID)
        self.btn_confirm.config(state="disabled")
        threading.Thread(
            target=self._do_cerca,
            args=(email.strip(), code.strip()),
            daemon=True
        ).start()

    def _do_cerca(self, email_scrittore: str, codice: str):
        """Cerca l'utente per email, poi il ringraziamento per codice."""
        if not FIREBASE_OK:
            self.after(0, self._cerca_errore, "Firebase non disponibile.")
            return
        try:
            # 1. Trova lo scrittore tramite email nella raccolta users
            users = _db.collection("users").where("email", "==", email_scrittore).limit(1).get()
            if not list(users):
                self.after(0, self._cerca_errore,
                           "Nessuno scrittore trovato con questa email.")
                return

            user_doc = list(users)[0]
            uid_scrittore = user_doc.id
            nome_scrittore = user_doc.to_dict().get("nome", email_scrittore)

            # 2. Cerca il ringraziamento con quel codice tra i suoi
            docs = (_db.collection("users")
                       .document(uid_scrittore)
                       .collection("ringraziamenti")
                       .where("codice", "==", codice)
                       .limit(1)
                       .get())
            docs_list = list(docs)
            if not docs_list:
                self.after(0, self._cerca_errore,
                           "Codice non trovato. Verifica i dati inseriti.")
                return

            ring = docs_list[0].to_dict()
            doc_id       = docs_list[0].id
            visualizzato = ring.get("visualizzato", False)

            # Segna come visualizzato se non lo era ancora
            if not visualizzato:
                try:
                    (_db.collection("users")
                        .document(uid_scrittore)
                        .collection("ringraziamenti")
                        .document(doc_id)
                        .update({"visualizzato": True}))
                except Exception:
                    pass   # non bloccare la lettura per un errore di aggiornamento

            self.after(0, self._cerca_ok,
                       ring.get("destinatario", ""),
                       ring.get("testo", ""),
                       ring.get("risposta", ""),
                       nome_scrittore,
                       uid_scrittore,
                       doc_id)

        except Exception as ex:
            self.after(0, self._cerca_errore, f"Errore: {ex}")

    def _cerca_ok(self, destinatario: str, testo: str, risposta: str,
                  autore: str, uid_scrittore: str, doc_id: str):
        self.btn_confirm.config(state="normal")
        self.lbl_msg.config(text="")
        self.withdraw()
        ThanksWindow(self, destinatario=destinatario, testo=testo,
                     risposta=risposta, autore=autore,
                     uid_scrittore=uid_scrittore, doc_id=doc_id)

    def _cerca_errore(self, msg: str):
        self.btn_confirm.config(state="normal")
        self.lbl_msg.config(text=msg, fg=RED_ERR)

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


# ── Finestra Ringraziamento (lettore) ────────────────────────────────────────
class ThanksWindow(tk.Toplevel):
    """
    Mostra il ringraziamento ricevuto dal lettore e permette di rispondere.
    Usa tk.Label con wraplength calcolato dopo il rendering: nessun Text
    asincrono, apertura istantanea, dimensioni esatte.
    """
    # Larghezza finestra fissa − padding orizzontale totale (30*2 padx + 28*2 card)
    _CARD_PAD  = 30   # padx esterno root
    _INNER_PAD = 28   # padx interno card
    _WRAP = 460 - 2 * _CARD_PAD - 2 * _INNER_PAD   # ≈ 344 px

    def __init__(self, reader_win, destinatario: str, testo: str,
                 risposta: str, autore: str, uid_scrittore: str, doc_id: str):
        super().__init__()
        self.reader_win    = reader_win
        self.uid_scrittore = uid_scrittore
        self.doc_id        = doc_id
        self.title("Ringraziamenti – Il tuo messaggio")
        self.resizable(False, False)
        self.configure(bg=BG)
        self.geometry(reader_win.geometry())

        self.f_title  = tkfont.Font(family="Georgia",   size=26, weight="bold")
        self.f_sub    = tkfont.Font(family="Georgia",   size=11, slant="italic")
        self.f_name   = tkfont.Font(family="Georgia",   size=20, weight="bold")
        self.f_btn    = tkfont.Font(family="Helvetica", size=11, weight="bold")
        self.f_label  = tkfont.Font(family="Helvetica", size=10, weight="bold")
        self.f_thanks = tkfont.Font(family="Georgia",   size=13, slant="italic")
        self.f_small  = tkfont.Font(family="Helvetica", size=9)

        self.protocol("WM_DELETE_WINDOW", self._on_back)
        self._risposta_corrente = risposta
        self._build_ui(destinatario, testo, risposta, autore)

    # ─────────────────────────────────────────────────────────────────────────
    def _build_ui(self, destinatario: str, testo: str, risposta: str, autore: str):
        W = self._WRAP

        # Bottone fisso in fondo
        bottom_bar = tk.Frame(self, bg=BG,
                              highlightthickness=1, highlightbackground=ENTRY_BD)
        bottom_bar.pack(fill="x", side="bottom")
        tk.Button(bottom_bar, text="\u2190 Torna all'inserimento del codice",
                  font=self.f_btn, bg=ENTRY_BG, fg=TEXT_MID,
                  activebackground=ENTRY_BD, activeforeground=TEXT_DARK,
                  relief="flat", bd=0, cursor="hand2",
                  pady=12, command=self._on_back).pack(fill="x", padx=24, pady=12)

        # Area scrollabile
        container = tk.Frame(self, bg=BG)
        container.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(container, orient="vertical")
        canvas    = tk.Canvas(container, bg=BG, highlightthickness=0,
                              yscrollcommand=scrollbar.set)
        scrollbar.config(command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        sf = tk.Frame(canvas, bg=BG)
        wid = canvas.create_window((0, 0), window=sf, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(wid, width=e.width))
        sf.bind("<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        _setup_smart_scroll(canvas)

        root = tk.Frame(sf, bg=BG)
        root.pack(fill="x", padx=self._CARD_PAD, pady=20)

        # Header
        tk.Label(root, text="\u2709",
                 font=tkfont.Font(size=36), bg=BG, fg=ACCENT).pack(pady=(0, 4))
        tk.Label(root, text="Ringraziamenti",
                 font=self.f_title, bg=BG, fg=TEXT_DARK).pack()
        tk.Label(root, text=f"Ciao, {destinatario}!",
                 font=self.f_name, bg=BG, fg=ACCENT).pack(pady=(14, 2))
        tk.Label(root, text="Hai ricevuto un messaggio di ringraziamento.",
                 font=self.f_sub, bg=BG, fg=TEXT_MID).pack(pady=(0, 20))

        # ── Card testo ────────────────────────────────────────────────────────
        card = tk.Frame(root, bg=CARD_BG,
                        highlightthickness=1, highlightbackground=ENTRY_BD)
        card.pack(fill="x")
        inner = tk.Frame(card, bg=CARD_BG)
        inner.pack(fill="x", padx=self._INNER_PAD, pady=24)

        tk.Label(inner, text="\u201c",
                 font=tkfont.Font(family="Georgia", size=48),
                 bg=CARD_BG, fg=ACCENT_LIGHT, anchor="w").pack(fill="x")
        tk.Label(inner, text=testo,
                 font=self.f_thanks, bg=CARD_BG, fg=TEXT_DARK,
                 wraplength=W, justify="center", anchor="center").pack(fill="x")
        tk.Frame(inner, bg=ENTRY_BD, height=1).pack(fill="x", pady=(16, 10))
        tk.Label(inner, text=f"\u2014 {autore}",
                 font=tkfont.Font(family="Helvetica", size=10, slant="italic"),
                 bg=CARD_BG, fg=TEXT_LIGHT, anchor="e").pack(fill="x")

        # ── Card risposta ─────────────────────────────────────────────────────
        resp_card = tk.Frame(root, bg=CARD_BG,
                             highlightthickness=1, highlightbackground=ENTRY_BD)
        resp_card.pack(fill="x", pady=(16, 0))
        self._resp_inner = tk.Frame(resp_card, bg=CARD_BG)
        self._resp_inner.pack(fill="x", padx=self._INNER_PAD, pady=24)

        tk.Label(self._resp_inner,
                 text="\U0001f4ac  La tua risposta",
                 font=tkfont.Font(family="Helvetica", size=12, weight="bold"),
                 bg=CARD_BG, fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(0, 12))

        if risposta:
            self._mostra_risposta_readonly(risposta)
        else:
            self._mostra_form_risposta()

    # ── Mostra risposta in sola lettura ───────────────────────────────────────
    def _mostra_risposta_readonly(self, testo_resp: str):
        W = self._WRAP
        tk.Label(self._resp_inner, text=testo_resp,
                 font=self.f_thanks, bg=ENTRY_BG, fg=TEXT_DARK,
                 wraplength=W, justify="center", anchor="center",
                 padx=12, pady=10).pack(fill="x")
        if self._risposta_corrente:
            tk.Label(self._resp_inner,
                     text="Hai già risposto a questo ringraziamento.",
                     font=self.f_small, bg=CARD_BG, fg=TEXT_LIGHT).pack(pady=(8, 0))

    # ── Mostra form per scrivere risposta ─────────────────────────────────────
    def _mostra_form_risposta(self):
        tk.Label(self._resp_inner, text="SCRIVI LA TUA RISPOSTA",
                 font=self.f_label, bg=CARD_BG, fg=TEXT_MID).pack(anchor="w")

        text_frame = tk.Frame(self._resp_inner, bg=ENTRY_BG,
                              highlightthickness=1, highlightbackground=ENTRY_BD)
        text_frame.pack(fill="x", pady=(6, 0))
        self._text_resp = tk.Text(
            text_frame,
            font=tkfont.Font(family="Helvetica", size=11),
            bg=ENTRY_BG, fg=TEXT_LIGHT,
            relief="flat", bd=0, wrap="word",
            insertbackground=TEXT_DARK,
            height=5, padx=10, pady=8)
        self._text_resp.pack(fill="x")
        self._text_resp.insert("1.0", "Scrivi qui la tua risposta\u2026")
        self._resp_placeholder = True

        def r_focus_in(_):
            if self._resp_placeholder:
                self._text_resp.delete("1.0", "end")
                self._text_resp.config(fg=TEXT_DARK)
                self._resp_placeholder = False
            text_frame.config(highlightbackground=ACCENT)

        def r_focus_out(_):
            if self._text_resp.get("1.0", "end").strip() == "":
                self._text_resp.delete("1.0", "end")
                self._text_resp.insert("1.0", "Scrivi qui la tua risposta\u2026")
                self._text_resp.config(fg=TEXT_LIGHT)
                self._resp_placeholder = True
            text_frame.config(highlightbackground=ENTRY_BD)

        self._text_resp.bind("<FocusIn>",  r_focus_in)
        self._text_resp.bind("<FocusOut>", r_focus_out)

        self._lbl_resp_msg = tk.Label(self._resp_inner, text="",
                                      font=self.f_small, bg=CARD_BG,
                                      fg=RED_ERR, wraplength=self._WRAP)
        self._lbl_resp_msg.pack(fill="x", pady=(6, 0))

        self._btn_invia = tk.Button(
            self._resp_inner,
            text="Invia risposta",
            font=self.f_btn, bg=ACCENT, fg="white",
            activebackground=ACCENT_DARK, activeforeground="white",
            relief="flat", bd=0, cursor="hand2",
            pady=9, command=self._on_invia_risposta)
        self._btn_invia.pack(fill="x", pady=(10, 0))

    # ── Invio risposta ────────────────────────────────────────────────────────
    def _on_invia_risposta(self):
        if self._resp_placeholder:
            self._lbl_resp_msg.config(text="Scrivi una risposta prima di inviare.")
            return
        testo_resp = self._text_resp.get("1.0", "end").strip()
        if not testo_resp:
            self._lbl_resp_msg.config(text="Scrivi una risposta prima di inviare.")
            return
        self._lbl_resp_msg.config(text="Invio in corso\u2026", fg=TEXT_MID)
        self._btn_invia.config(state="disabled")
        threading.Thread(target=self._do_invia_risposta,
                         args=(testo_resp,), daemon=True).start()

    def _do_invia_risposta(self, testo_resp: str):
        if not FIREBASE_OK:
            self.after(0, self._lbl_resp_msg.config,
                       {"text": "Firebase non disponibile.", "fg": RED_ERR})
            self.after(0, self._btn_invia.config, {"state": "normal"})
            return
        try:
            (_db.collection("users")
                .document(self.uid_scrittore)
                .collection("ringraziamenti")
                .document(self.doc_id)
                .update({"risposta": testo_resp}))
            self.after(0, self._risposta_inviata, testo_resp)
        except Exception as ex:
            self.after(0, self._lbl_resp_msg.config,
                       {"text": f"Errore: {ex}", "fg": RED_ERR})
            self.after(0, self._btn_invia.config, {"state": "normal"})

    def _risposta_inviata(self, testo_resp: str):
        """Sostituisce la form con il testo confermato."""
        for w in self._resp_inner.winfo_children():
            # Tieni solo il titolo (primo widget)
            if w != self._resp_inner.winfo_children()[0]:
                w.destroy()
        self._risposta_corrente = testo_resp
        self._mostra_risposta_readonly(testo_resp)
        tk.Label(self._resp_inner,
                 text="\u2705 Risposta inviata con successo!",
                 font=self.f_small, bg=CARD_BG, fg=BTN_READER_FG).pack(pady=(8, 0))

    def _on_back(self):
        self.destroy()
        self.reader_win.deiconify()


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = RingraziamentiApp()
    app.mainloop()
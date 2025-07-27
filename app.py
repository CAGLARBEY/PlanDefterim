import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import winsound

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PLAN DEFTERİM")
        self.root.geometry("1200x800")

        # Tema renk paletleri
        self.themes = {
            "Koyu": {
                "bg": "#2D2D2D",          # Ana arka plan
                "fg": "#E0E0E0",          # Ana metin rengi
                "entry_bg": "#3D3D3D",    # Giriş alanları arka plan
                "entry_fg": "#FFFFFF",    # Giriş alanları metin
                "button_bg": "#4A4A4A",   # Buton arka plan
                "button_fg": "#FFFFFF",   # Buton metin
                "button_active": "#5E5E5E", # Buton aktif durumu
                "high_priority": "#FF5252", # Yüksek öncelik
                "medium_priority": "#FFC107", # Orta öncelik
                "low_priority": "#4CAF50",   # Düşük öncelik
                "completed": "#757575",     # Tamamlanmış görevler
                "tab_bg": "#3D3D3D",       # Sekme arka plan
                "tab_active": "#2D2D2D",   # Aktif sekme
                "highlight": "#1976D2",    # Vurgu rengi
                "border": "#1E1E1E",       # Kenarlık rengi
                "canvas_bg": "#2D2D2D",    # Canvas arka plan
                "chart_bg": "#2D2D2D"      # Grafik arka plan
            },
            "Açık": {
                "bg": "#FFFFFF",
                "fg": "#000000",
                "entry_bg": "#F5F5F5",
                "entry_fg": "#000000",
                "button_bg": "#E0E0E0",
                "button_fg": "#000000",
                "button_active": "#BDBDBD",
                "high_priority": "#D32F2F",
                "medium_priority": "#FFA000",
                "low_priority": "#388E3C",
                "completed": "#9E9E9E",
                "tab_bg": "#F5F5F5",
                "tab_active": "#E0E0E0",
                "highlight": "#1976D2",
                "border": "#BDBDBD",
                "canvas_bg": "#FFFFFF",
                "chart_bg": "#FFFFFF"
            },
            "Mavi": {
                "bg": "#E3F2FD",
                "fg": "#0D47A1",
                "entry_bg": "#BBDEFB",
                "entry_fg": "#0D47A1",
                "button_bg": "#90CAF9",
                "button_fg": "#0D47A1",
                "button_active": "#64B5F6",
                "high_priority": "#D32F2F",
                "medium_priority": "#FFA000",
                "low_priority": "#388E3C",
                "completed": "#757575",
                "tab_bg": "#BBDEFB",
                "tab_active": "#90CAF9",
                "highlight": "#1565C0",
                "border": "#42A5F5",
                "canvas_bg": "#E3F2FD",
                "chart_bg": "#E3F2FD"
            },
            "Yeşil": {
                "bg": "#E8F5E9",
                "fg": "#1B5E20",
                "entry_bg": "#C8E6C9",
                "entry_fg": "#1B5E20",
                "button_bg": "#A5D6A7",
                "button_fg": "#1B5E20",
                "button_active": "#81C784",
                "high_priority": "#D32F2F",
                "medium_priority": "#FFA000",
                "low_priority": "#388E3C",
                "completed": "#757575",
                "tab_bg": "#C8E6C9",
                "tab_active": "#A5D6A7",
                "highlight": "#2E7D32",
                "border": "#66BB6A",
                "canvas_bg": "#E8F5E9",
                "chart_bg": "#E8F5E9"
            },
            "Mor": {
                "bg": "#F3E5F5",
                "fg": "#4A148C",
                "entry_bg": "#E1BEE7",
                "entry_fg": "#4A148C",
                "button_bg": "#CE93D8",
                "button_fg": "#4A148C",
                "button_active": "#BA68C8",
                "high_priority": "#D32F2F",
                "medium_priority": "#FFA000",
                "low_priority": "#388E3C",
                "completed": "#757575",
                "tab_bg": "#E1BEE7",
                "tab_active": "#CE93D8",
                "highlight": "#7B1FA2",
                "border": "#AB47BC",
                "canvas_bg": "#F3E5F5",
                "chart_bg": "#F3E5F5"
            },
            "Kırmızı": {
                "bg": "#FFEBEE",
                "fg": "#B71C1C",
                "entry_bg": "#FFCDD2",
                "entry_fg": "#B71C1C",
                "button_bg": "#EF9A9A",
                "button_fg": "#B71C1C",
                "button_active": "#E57373",
                "high_priority": "#D32F2F",
                "medium_priority": "#FFA000",
                "low_priority": "#388E3C",
                "completed": "#757575",
                "tab_bg": "#FFCDD2",
                "tab_active": "#EF9A9A",
                "highlight": "#C62828",
                "border": "#EF5350",
                "canvas_bg": "#FFEBEE",
                "chart_bg": "#FFEBEE"
            }
        }
        
        # Varsayılan tema
        self.current_theme = "Koyu"
        self.colors = self.themes[self.current_theme]
        self.root.configure(bg=self.colors["bg"])
        
        # Veritabanı dosyası
        self.db_file = "todo_data.json"
        self.data = self.load_data()
        
        # Kategoriler ve öncelikler
        self.categories = ["İş", "Kişisel", "Alışveriş", "Diğer"]
        self.priorities = ["Yüksek", "Orta", "Düşük"]
        
        # Pomodoro ayarları
        self.pomodoro_settings = {
            "work": 25,
            "short_break": 5,
            "long_break": 15,
            "pomodoros_before_long_break": 4
        }
        self.pomodoro_running = False
        self.pomodoro_count = 0
        self.current_pomodoro_phase = "work"
        
        # Arayüzü oluştur
        self.setup_ui()
        
        # Hatırlatıcı kontrolü başlat
        self.check_reminders()
    
    def change_theme(self, theme_name):
        self.current_theme = theme_name
        self.colors = self.themes[theme_name]
        self.refresh_ui()
    
    def setup_ui(self):
        # Ana çerçeve oluştur
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sol panel (tema butonları için)
        left_panel = tk.Frame(main_frame, width=150, bg=self.colors["bg"])
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        left_panel.pack_propagate(False)  # Genişliği sabit tut
        
        # Tema seçici başlık
        theme_label = tk.Label(
            left_panel,
            text="Tema Seçiniz",
            font=("Arial", 10, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        )
        theme_label.pack(pady=10)
        
        # Tema butonları
        for theme_name in self.themes.keys():
            btn = ttk.Button(
                left_panel,
                text=theme_name,
                command=lambda name=theme_name: self.change_theme(name),
                style="TButton"
            )
            btn.pack(fill=tk.X, padx=5, pady=2)
        
        # Ana içerik alanı
        content_frame = tk.Frame(main_frame, bg=self.colors["bg"])
        content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Ana notebook (sekmeler)
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Stil ayarları
        self.configure_styles()
        
        # Sekmeleri oluştur
        self.create_daily_tab()
        self.create_weekly_tab()
        self.create_monthly_tab()
        self.create_stats_tab()
        self.create_pomodoro_tab()
        
        # Menü çubuğu
        self.create_menu_bar()

    # ... (diğer metodlar aynen kalacak, sadece setup_ui metodu değişti)
    
    def configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Genel stil ayarları
        style.configure(".", 
                       background=self.colors["bg"],
                       foreground=self.colors["fg"],
                       fieldbackground=self.colors["entry_bg"],
                       selectbackground=self.colors["highlight"],
                       selectforeground=self.colors["fg"],
                       insertcolor=self.colors["fg"])
        
        # Notebook stili
        style.configure("TNotebook", background=self.colors["tab_bg"], borderwidth=0)
        style.configure("TNotebook.Tab", 
                       background=self.colors["tab_bg"],
                       foreground=self.colors["fg"],
                       padding=[10, 5],
                       font=('Arial', 10, 'bold'))
        style.map("TNotebook.Tab",
                  background=[("selected", self.colors["tab_active"])],
                  foreground=[("selected", self.colors["fg"])])
        
        # Buton stili
        style.configure("TButton",
                       background=self.colors["button_bg"],
                       foreground=self.colors["button_fg"],
                       borderwidth=0,
                       font=('Arial', 9))
        style.map("TButton",
                 background=[("active", self.colors["button_active"]),
                            ("pressed", self.colors["button_active"])])
        
        # Entry stili
        style.configure("TEntry",
                       fieldbackground=self.colors["entry_bg"],
                       foreground=self.colors["entry_fg"],
                       insertcolor=self.colors["fg"],
                       borderwidth=0)
        
        # Combobox stili
        style.configure("TCombobox",
                       fieldbackground=self.colors["entry_bg"],
                       foreground=self.colors["entry_fg"],
                       background=self.colors["bg"],
                       selectbackground=self.colors["highlight"])
        
        # Scrollbar stili
        style.configure("Vertical.TScrollbar",
                        background=self.colors["button_bg"],
                        arrowcolor=self.colors["fg"],
                        troughcolor=self.colors["bg"])
    
    def create_menu_bar(self):
        menubar = tk.Menu(self.root, bg=self.colors["bg"], fg=self.colors["fg"])
        
        # Dosya menüsü
        file_menu = tk.Menu(menubar, tearoff=0, bg=self.colors["bg"], fg=self.colors["fg"])
        file_menu.add_command(label="Dışa Aktar (CSV)", command=self.export_to_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Çıkış", command=self.root.quit)
        menubar.add_cascade(label="Dosya", menu=file_menu)
        
        # Yardım menüsü
        help_menu = tk.Menu(menubar, tearoff=0, bg=self.colors["bg"], fg=self.colors["fg"])
        help_menu.add_command(label="Kullanım Kılavuzu")
        help_menu.add_command(label="Hakkında")
        menubar.add_cascade(label="Yardım", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def create_daily_tab(self):
        daily_tab = ttk.Frame(self.notebook)
        self.notebook.add(daily_tab, text="Günlük")
        
        daily_notebook = ttk.Notebook(daily_tab)
        daily_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Bugün sekmesi
        today_tab = ttk.Frame(daily_notebook)
        daily_notebook.add(today_tab, text="Bugün")
        self.create_daily_task_list(today_tab, "today")
        
        # Yarın sekmesi
        tomorrow_tab = ttk.Frame(daily_notebook)
        daily_notebook.add(tomorrow_tab, text="Yarın")
        self.create_daily_task_list(tomorrow_tab, "tomorrow")
        
        add_button = ttk.Button(
            daily_tab, 
            text="+ Yeni Görev Ekle", 
            command=self.add_new_task,
            style="TButton"
        )
        add_button.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
    
    def create_daily_task_list(self, parent, day_type):
        task_frame = tk.Frame(parent, bg=self.colors["bg"])
        task_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(task_frame, bg=self.colors["canvas_bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(task_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors["bg"])
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.load_tasks_for_day(scrollable_frame, day_type)
    
    def load_tasks_for_day(self, parent, day_type):
        for widget in parent.winfo_children():
            widget.destroy()
        
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        target_date = today if day_type == "today" else tomorrow
        
        tasks_for_day = []
        for task in self.data["tasks"]:
            task_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
            if task_date == target_date:
                tasks_for_day.append(task)
        
        tasks_for_day.sort(key=lambda x: self.priorities.index(x["priority"]))
        
        if not tasks_for_day:
            empty_label = tk.Label(
                parent, 
                text="Henüz görev eklenmedi", 
                bg=self.colors["bg"], 
                fg=self.colors["fg"]
            )
            empty_label.pack(pady=20)
            return
        
        for task in tasks_for_day:
            self.create_task_widget(parent, task)
    
    def create_task_widget(self, parent, task):
        task_frame = tk.Frame(
            parent, 
            bg=self.colors["entry_bg"],
            padx=10,
            pady=10,
            highlightbackground=self.get_priority_color(task["priority"]),
            highlightthickness=2
        )
        task_frame.pack(fill=tk.X, pady=5, padx=5)
        
        completed_var = tk.BooleanVar(value=task["completed"])
        check_button = tk.Checkbutton(
            task_frame,
            variable=completed_var,
            command=lambda: self.toggle_task_completion(task["id"], completed_var.get()),
            bg=self.colors["entry_bg"],
            activebackground=self.colors["entry_bg"],
            selectcolor=self.colors["entry_bg"]
        )
        check_button.grid(row=0, column=0, rowspan=2, sticky="n")
        
        title_label = tk.Label(
            task_frame,
            text=task["title"],
            font=("Arial", 12, "bold"),
            bg=self.colors["entry_bg"],
            fg=self.colors["fg"] if not task["completed"] else self.colors["completed"],
            wraplength=800,
            justify="left"
        )
        if task["completed"]:
            title_label.config(font=("Arial", 12, "bold", "overstrike"))
        title_label.grid(row=0, column=1, sticky="w")
        
        details_text = f"Kategori: {task['category']} | Öncelik: {task['priority']} | Tarih: {task['due_date']}"
        details_label = tk.Label(
            task_frame,
            text=details_text,
            font=("Arial", 9),
            bg=self.colors["entry_bg"],
            fg=self.colors["fg"] if not task["completed"] else self.colors["completed"],
            wraplength=800,
            justify="left"
        )
        details_label.grid(row=1, column=1, sticky="w")
        
        if task["notes"]:
            notes_label = tk.Label(
                task_frame,
                text=f"Notlar: {task['notes']}",
                font=("Arial", 9, "italic"),
                bg=self.colors["entry_bg"],
                fg=self.colors["fg"] if not task["completed"] else self.colors["completed"],
                wraplength=800,
                justify="left"
            )
            notes_label.grid(row=2, column=1, sticky="w", pady=(5, 0))
        
        if task["subtasks"]:
            subtasks_frame = tk.Frame(task_frame, bg=self.colors["entry_bg"])
            subtasks_frame.grid(row=3, column=1, sticky="w", pady=(5, 0))
            
            for subtask in task["subtasks"]:
                subtask_var = tk.BooleanVar(value=subtask["completed"])
                subtask_check = tk.Checkbutton(
                    subtasks_frame,
                    text=subtask["title"],
                    variable=subtask_var,
                    onvalue=True,
                    offvalue=False,
                    command=lambda t=task, s=subtask, v=subtask_var: self.update_subtask(t, s, v.get()),
                    bg=self.colors["entry_bg"],
                    fg=self.colors["fg"],
                    activebackground=self.colors["entry_bg"],
                    activeforeground=self.colors["fg"],
                    selectcolor=self.colors["entry_bg"]
                )
                subtask_check.pack(anchor="w")
        
        buttons_frame = tk.Frame(task_frame, bg=self.colors["entry_bg"])
        buttons_frame.grid(row=0, column=2, rowspan=4, sticky="e")
        
        edit_button = ttk.Button(
            buttons_frame,
            text="Düzenle",
            command=lambda: self.edit_task(task["id"]),
            style="TButton"
        )
        edit_button.pack(side=tk.LEFT, padx=5)
        
        delete_button = ttk.Button(
            buttons_frame,
            text="Sil",
            command=lambda: self.delete_task(task["id"]),
            style="TButton"
        )
        delete_button.pack(side=tk.LEFT, padx=5)
        
        if "today" in str(parent.master.master):
            move_button = ttk.Button(
                buttons_frame,
                text="Yarına Taşı",
                command=lambda: self.move_task_to_tomorrow(task["id"]),
                style="TButton"
            )
            move_button.pack(side=tk.LEFT, padx=5)
    
    def create_weekly_tab(self):
        weekly_tab = ttk.Frame(self.notebook)
        self.notebook.add(weekly_tab, text="Haftalık")
        
        weekly_frame = tk.Frame(weekly_tab, bg=self.colors["bg"])
        weekly_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        
        week_title = f"Haftalık Görünüm: {start_of_week.strftime('%d.%m.%Y')} - {end_of_week.strftime('%d.%m.%Y')}"
        title_label = tk.Label(
            weekly_frame,
            text=week_title,
            font=("Arial", 14, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        )
        title_label.pack(pady=10)
        
        weekly_notebook = ttk.Notebook(weekly_frame)
        weekly_notebook.pack(fill=tk.BOTH, expand=True)
        
        days = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
        for i, day in enumerate(days):
            day_date = start_of_week + timedelta(days=i)
            day_tab = ttk.Frame(weekly_notebook)
            weekly_notebook.add(day_tab, text=f"{day} ({day_date.strftime('%d.%m')})")
            
            day_frame = tk.Frame(day_tab, bg=self.colors["bg"])
            day_frame.pack(fill=tk.BOTH, expand=True)
            
            canvas = tk.Canvas(day_frame, bg=self.colors["canvas_bg"], highlightthickness=0)
            scrollbar = ttk.Scrollbar(day_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=self.colors["bg"])
            
            scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            self.load_tasks_for_weekly_day(scrollable_frame, day_date.date())
    
    def load_tasks_for_weekly_day(self, parent, date):
        for widget in parent.winfo_children():
            widget.destroy()
        
        tasks_for_day = []
        for task in self.data["tasks"]:
            task_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
            if task_date == date:
                tasks_for_day.append(task)
        
        tasks_for_day.sort(key=lambda x: self.priorities.index(x["priority"]))
        
        if not tasks_for_day:
            empty_label = tk.Label(
                parent, 
                text="Bu gün için görev yok", 
                bg=self.colors["bg"], 
                fg=self.colors["fg"]
            )
            empty_label.pack(pady=20)
            return
        
        for task in tasks_for_day:
            self.create_task_widget(parent, task)
    
    def create_monthly_tab(self):
        monthly_tab = ttk.Frame(self.notebook)
        self.notebook.add(monthly_tab, text="Aylık")
        
        monthly_frame = tk.Frame(monthly_tab, bg=self.colors["bg"])
        monthly_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        today = datetime.now()
        month_title = today.strftime("%B %Y")
        title_label = tk.Label(
            monthly_frame,
            text=month_title,
            font=("Arial", 14, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        )
        title_label.pack(pady=10)
        
        weeks_frame = tk.Frame(monthly_frame, bg=self.colors["bg"])
        weeks_frame.pack(fill=tk.BOTH, expand=True)
        
        for week_num in range(4):
            week_frame = tk.Frame(
                weeks_frame,
                bg=self.colors["tab_bg"],
                padx=10,
                pady=10,
                relief=tk.RAISED,
                borderwidth=1
            )
            week_frame.grid(row=week_num // 2, column=week_num % 2, padx=5, pady=5, sticky="nsew")
            
            start_date = today.replace(day=1) + timedelta(weeks=week_num)
            end_date = start_date + timedelta(days=6)
            week_title = f"Hafta {week_num+1}: {start_date.strftime('%d.%m')} - {end_date.strftime('%d.%m')}"
            week_label = tk.Label(
                week_frame,
                text=week_title,
                font=("Arial", 10, "bold"),
                bg=self.colors["tab_bg"],
                fg=self.colors["fg"]
            )
            week_label.pack(anchor="w")
            
            week_tasks = self.get_tasks_for_week(start_date.date(), end_date.date())
            
            if not week_tasks:
                empty_label = tk.Label(
                    week_frame,
                    text="Bu hafta için görev yok",
                    bg=self.colors["tab_bg"],
                    fg=self.colors["fg"]
                )
                empty_label.pack(pady=10)
            else:
                for task in week_tasks[:5]:
                    task_label = tk.Label(
                        week_frame,
                        text=f"- {task['title']} ({task['priority']})",
                        bg=self.colors["tab_bg"],
                        fg=self.get_priority_color(task["priority"]),
                        anchor="w",
                        wraplength=250
                    )
                    task_label.pack(anchor="w", padx=5)
                
                if len(week_tasks) > 5:
                    more_label = tk.Label(
                        week_frame,
                        text=f"+ {len(week_tasks)-5} daha...",
                        bg=self.colors["tab_bg"],
                        fg=self.colors["fg"],
                        anchor="w"
                    )
                    more_label.pack(anchor="w", padx=5)
            
            add_button = ttk.Button(
                week_frame,
                text="Görev Ekle",
                command=lambda s=start_date.date(), e=end_date.date(): self.add_weekly_task(s, e),
                style="TButton"
            )
            add_button.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        
        for i in range(2):
            weeks_frame.grid_rowconfigure(i, weight=1)
            weeks_frame.grid_columnconfigure(i, weight=1)
    
    def get_tasks_for_week(self, start_date, end_date):
        tasks_for_week = []
        for task in self.data["tasks"]:
            task_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
            if start_date <= task_date <= end_date:
                tasks_for_week.append(task)
        
        tasks_for_week.sort(key=lambda x: self.priorities.index(x["priority"]))
        return tasks_for_week
    
    def create_stats_tab(self):
        stats_tab = ttk.Frame(self.notebook)
        self.notebook.add(stats_tab, text="İstatistikler")
        
        stats_frame = tk.Frame(stats_tab, bg=self.colors["bg"])
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        title_label = tk.Label(
            stats_frame,
            text="Üretkenlik İstatistikleri",
            font=("Arial", 14, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        )
        title_label.pack(pady=10)
        
        stats_notebook = ttk.Notebook(stats_frame)
        stats_notebook.pack(fill=tk.BOTH, expand=True)
        
        cat_tab = ttk.Frame(stats_notebook)
        stats_notebook.add(cat_tab, text="Kategori Dağılımı")
        self.create_category_chart(cat_tab)
        
        prio_tab = ttk.Frame(stats_notebook)
        stats_notebook.add(prio_tab, text="Öncelik Dağılımı")
        self.create_priority_chart(prio_tab)
        
        comp_tab = ttk.Frame(stats_notebook)
        stats_notebook.add(comp_tab, text="Tamamlanma Oranları")
        self.create_completion_chart(comp_tab)
    
    def create_category_chart(self, parent):
        categories = defaultdict(int)
        for task in self.data["tasks"]:
            categories[task["category"]] += 1
        
        if not categories:
            empty_label = tk.Label(
                parent, 
                text="Henüz yeterli veri yok", 
                bg=self.colors["bg"], 
                fg=self.colors["fg"]
            )
            empty_label.pack(pady=50)
            return
        
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        fig.patch.set_facecolor(self.colors["chart_bg"])
        ax.set_facecolor(self.colors["chart_bg"])
        
        labels = list(categories.keys())
        sizes = list(categories.values())
        
        colors = ["#4285F4", "#EA4335", "#FBBC05", "#34A853", "#9B59B6"]
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors[:len(labels)], 
               textprops={'color': self.colors["fg"]})
        ax.set_title('Görevlerin Kategori Dağılımı', color=self.colors["fg"])
        
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def create_priority_chart(self, parent):
        priorities = defaultdict(int)
        for task in self.data["tasks"]:
            priorities[task["priority"]] += 1
        
        if not priorities:
            empty_label = tk.Label(
                parent, 
                text="Henüz yeterli veri yok", 
                bg=self.colors["bg"], 
                fg=self.colors["fg"]
            )
            empty_label.pack(pady=50)
            return
        
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        fig.patch.set_facecolor(self.colors["chart_bg"])
        ax.set_facecolor(self.colors["chart_bg"])
        
        labels = list(priorities.keys())
        sizes = list(priorities.values())
        
        colors = [self.colors["high_priority"], self.colors["medium_priority"], self.colors["low_priority"]]
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, 
               textprops={'color': self.colors["fg"]})
        ax.set_title('Görevlerin Öncelik Dağılımı', color=self.colors["fg"])
        
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def create_completion_chart(self, parent):
        completed = 0
        total = len(self.data["tasks"])
        
        if total == 0:
            empty_label = tk.Label(
                parent, 
                text="Henüz yeterli veri yok", 
                bg=self.colors["bg"], 
                fg=self.colors["fg"]
            )
            empty_label.pack(pady=50)
            return
        
        for task in self.data["tasks"]:
            if task["completed"]:
                completed += 1
        
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        fig.patch.set_facecolor(self.colors["chart_bg"])
        ax.set_facecolor(self.colors["chart_bg"])
        
        labels = ["Tamamlanan", "Tamamlanmayan"]
        sizes = [completed, total - completed]
        
        colors = [self.colors["low_priority"], self.colors["high_priority"]]
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, 
               textprops={'color': self.colors["fg"]})
        ax.set_title('Görev Tamamlanma Oranları', color=self.colors["fg"])
        
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def create_pomodoro_tab(self):
        pomodoro_tab = ttk.Frame(self.notebook)
        self.notebook.add(pomodoro_tab, text="Pomodoro")
        
        pomodoro_frame = tk.Frame(pomodoro_tab, bg=self.colors["bg"])
        pomodoro_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.timer_label = tk.Label(
            pomodoro_frame,
            text="25:00",
            font=("Arial", 48, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        )
        self.timer_label.pack(pady=20)
        
        self.phase_label = tk.Label(
            pomodoro_frame,
            text="Çalışma Zamanı",
            font=("Arial", 14),
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        )
        self.phase_label.pack(pady=5)
        
        buttons_frame = tk.Frame(pomodoro_frame, bg=self.colors["bg"])
        buttons_frame.pack(pady=20)
        
        self.start_button = ttk.Button(
            buttons_frame,
            text="Başlat",
            command=self.start_pomodoro,
            style="TButton"
        )
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.reset_button = ttk.Button(
            buttons_frame,
            text="Sıfırla",
            command=self.reset_pomodoro,
            style="TButton"
        )
        self.reset_button.config(state=tk.DISABLED)
        self.reset_button.pack(side=tk.LEFT, padx=10)
        
        counter_frame = tk.Frame(pomodoro_frame, bg=self.colors["bg"])
        counter_frame.pack(pady=10)
        
        tk.Label(
            counter_frame,
            text="Tamamlanan Pomodorolar:",
            font=("Arial", 10),
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        ).pack(side=tk.LEFT)
        
        self.counter_label = tk.Label(
            counter_frame,
            text="0",
            font=("Arial", 10, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        )
        self.counter_label.pack(side=tk.LEFT, padx=5)
        
        settings_frame = tk.Frame(pomodoro_frame, bg=self.colors["bg"])
        settings_frame.pack(pady=20)
        
        tk.Label(
            settings_frame,
            text="Çalışma Süresi (dk):",
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        ).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        
        self.work_entry = ttk.Entry(
            settings_frame,
            width=5
        )
        self.work_entry.insert(0, str(self.pomodoro_settings["work"]))
        self.work_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(
            settings_frame,
            text="Kısa Mola (dk):",
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        
        self.short_break_entry = ttk.Entry(
            settings_frame,
            width=5
        )
        self.short_break_entry.insert(0, str(self.pomodoro_settings["short_break"]))
        self.short_break_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(
            settings_frame,
            text="Uzun Mola (dk):",
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        ).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        
        self.long_break_entry = ttk.Entry(
            settings_frame,
            width=5
        )
        self.long_break_entry.insert(0, str(self.pomodoro_settings["long_break"]))
        self.long_break_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(
            settings_frame,
            text="Uzun Moladan Önce:",
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        ).grid(row=3, column=0, padx=5, pady=5, sticky="e")
        
        self.long_break_after_entry = ttk.Entry(
            settings_frame,
            width=5
        )
        self.long_break_after_entry.insert(0, str(self.pomodoro_settings["pomodoros_before_long_break"]))
        self.long_break_after_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        save_button = ttk.Button(
            settings_frame,
            text="Ayarları Kaydet",
            command=self.save_pomodoro_settings,
            style="TButton"
        )
        save_button.grid(row=4, column=0, columnspan=2, pady=10)
    
    def start_pomodoro(self):
        if not self.pomodoro_running:
            self.pomodoro_running = True
            self.start_button.config(text="Duraklat")
            self.reset_button.config(state=tk.NORMAL)
            
            if self.current_pomodoro_phase == "work":
                self.remaining_time = self.pomodoro_settings["work"] * 60
                self.phase_label.config(text="Çalışma Zamanı")
                self.timer_label.config(fg="#4285F4")
            elif self.current_pomodoro_phase == "short_break":
                self.remaining_time = self.pomodoro_settings["short_break"] * 60
                self.phase_label.config(text="Kısa Mola")
                self.timer_label.config(fg="#34A853")
            elif self.current_pomodoro_phase == "long_break":
                self.remaining_time = self.pomodoro_settings["long_break"] * 60
                self.phase_label.config(text="Uzun Mola")
                self.timer_label.config(fg="#EA4335")
            
            self.update_timer()
        else:
            self.pomodoro_running = False
            self.start_button.config(text="Devam Et")
    
    def reset_pomodoro(self):
        self.pomodoro_running = False
        self.start_button.config(text="Başlat")
        self.reset_button.config(state=tk.DISABLED)
        
        if self.current_pomodoro_phase == "work":
            self.timer_label.config(text=f"{self.pomodoro_settings['work']:02d}:00", fg=self.colors["fg"])
        elif self.current_pomodoro_phase == "short_break":
            self.timer_label.config(text=f"{self.pomodoro_settings['short_break']:02d}:00", fg=self.colors["fg"])
        elif self.current_pomodoro_phase == "long_break":
            self.timer_label.config(text=f"{self.pomodoro_settings['long_break']:02d}:00", fg=self.colors["fg"])
    
    def update_timer(self):
        if self.pomodoro_running and self.remaining_time > 0:
            minutes, seconds = divmod(self.remaining_time, 60)
            self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
            self.remaining_time -= 1
            self.root.after(1000, self.update_timer)
        elif self.remaining_time == 0:
            self.pomodoro_complete()
    
    def pomodoro_complete(self):
        self.pomodoro_running = False
        
        try:
            winsound.Beep(1000, 500)
        except:
            pass
        
        if self.current_pomodoro_phase == "work":
            self.pomodoro_count += 1
            self.counter_label.config(text=str(self.pomodoro_count))
            
            if self.pomodoro_count % self.pomodoro_settings["pomodoros_before_long_break"] == 0:
                self.current_pomodoro_phase = "long_break"
                messagebox.showinfo("Pomodoro Tamamlandı", "Uzun molaya çıkma zamanı!")
            else:
                self.current_pomodoro_phase = "short_break"
                messagebox.showinfo("Pomodoro Tamamlandı", "Kısa molaya çıkma zamanı!")
        else:
            self.current_pomodoro_phase = "work"
            messagebox.showinfo("Mola Bitti", "Çalışmaya devam etme zamanı!")
        
        self.reset_pomodoro()
    
    def save_pomodoro_settings(self):
        try:
            self.pomodoro_settings["work"] = int(self.work_entry.get())
            self.pomodoro_settings["short_break"] = int(self.short_break_entry.get())
            self.pomodoro_settings["long_break"] = int(self.long_break_entry.get())
            self.pomodoro_settings["pomodoros_before_long_break"] = int(self.long_break_after_entry.get())
            
            messagebox.showinfo("Başarılı", "Pomodoro ayarları kaydedildi!")
            self.reset_pomodoro()
        except ValueError:
            messagebox.showerror("Hata", "Lütfen geçerli sayılar girin!")
    
    def add_new_task(self, date=None):
        add_window = tk.Toplevel(self.root)
        add_window.title("Yeni Görev Ekle")
        add_window.geometry("500x600")
        add_window.configure(bg=self.colors["bg"])
        add_window.resizable(False, False)
        
        title_label = tk.Label(
            add_window,
            text="Yeni Görev Ekle",
            font=("Arial", 14, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        )
        title_label.pack(pady=10)
        
        form_frame = tk.Frame(add_window, bg=self.colors["bg"])
        form_frame.pack(fill=tk.BOTH, padx=20, pady=10)
        
        tk.Label(
            form_frame,
            text="Görev Başlığı:",
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        ).grid(row=0, column=0, sticky="w", pady=5)
        
        title_entry = ttk.Entry(
            form_frame
        )
        title_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
        
        tk.Label(
            form_frame,
            text="Kategori:",
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        ).grid(row=1, column=0, sticky="w", pady=5)
        
        category_var = tk.StringVar(value=self.categories[0])
        category_menu = ttk.Combobox(
            form_frame,
            textvariable=category_var,
            values=self.categories,
            state="readonly"
        )
        category_menu.grid(row=1, column=1, sticky="ew", pady=5, padx=5)
        
        tk.Label(
            form_frame,
            text="Öncelik:",
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        ).grid(row=2, column=0, sticky="w", pady=5)
        
        priority_var = tk.StringVar(value=self.priorities[1])
        priority_menu = ttk.Combobox(
            form_frame,
            textvariable=priority_var,
            values=self.priorities,
            state="readonly"
        )
        priority_menu.grid(row=2, column=1, sticky="ew", pady=5, padx=5)
        
        tk.Label(
            form_frame,
            text="Son Tarih:",
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        ).grid(row=3, column=0, sticky="w", pady=5)
        
        default_date = datetime.now().strftime("%Y-%m-%d") if date is None else date.strftime("%Y-%m-%d")
        
        date_entry = ttk.Entry(
            form_frame
        )
        date_entry.insert(0, default_date)
        date_entry.grid(row=3, column=1, sticky="ew", pady=5, padx=5)
        
        tk.Label(
            form_frame,
            text="Saat:",
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        ).grid(row=4, column=0, sticky="w", pady=5)
        
        time_entry = ttk.Entry(
            form_frame
        )
        time_entry.insert(0, "12:00")
        time_entry.grid(row=4, column=1, sticky="ew", pady=5, padx=5)
        
        tk.Label(
            form_frame,
            text="Notlar:",
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        ).grid(row=5, column=0, sticky="nw", pady=5)
        
        notes_text = tk.Text(
            form_frame,
            bg=self.colors["entry_bg"],
            fg=self.colors["entry_fg"],
            height=5,
            width=30,
            wrap=tk.WORD,
            borderwidth=0
        )
        notes_text.grid(row=5, column=1, sticky="ew", pady=5, padx=5)
        
        tk.Label(
            form_frame,
            text="Alt Görevler:",
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        ).grid(row=6, column=0, sticky="nw", pady=5)
        
        subtasks_frame = tk.Frame(form_frame, bg=self.colors["bg"])
        subtasks_frame.grid(row=6, column=1, sticky="ew", pady=5, padx=5)
        
        subtask_entries = []
        
        def add_subtask_entry():
            entry = ttk.Entry(
                subtasks_frame
            )
            entry.pack(fill=tk.X, pady=2)
            subtask_entries.append(entry)
        
        add_subtask_entry()
        
        add_subtask_button = ttk.Button(
            subtasks_frame,
            text="+ Alt Görev Ekle",
            command=add_subtask_entry,
            style="TButton"
        )
        add_subtask_button.pack(fill=tk.X, pady=5)
        
        tk.Label(
            form_frame,
            text="Tekrarlama:",
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        ).grid(row=7, column=0, sticky="w", pady=5)
        
        repeat_var = tk.StringVar(value="Yok")
        repeat_menu = ttk.Combobox(
            form_frame,
            textvariable=repeat_var,
            values=["Yok", "Günlük", "Haftalık", "Aylık"],
            state="readonly"
        )
        repeat_menu.grid(row=7, column=1, sticky="ew", pady=5, padx=5)
        
        buttons_frame = tk.Frame(add_window, bg=self.colors["bg"])
        buttons_frame.pack(fill=tk.X, padx=20, pady=10)
        
        cancel_button = ttk.Button(
            buttons_frame,
            text="İptal",
            command=add_window.destroy,
            style="TButton"
        )
        cancel_button.pack(side=tk.LEFT, padx=5, expand=True)
        
        save_button = ttk.Button(
            buttons_frame,
            text="Kaydet",
            command=lambda: self.save_new_task(
                add_window,
                title_entry.get(),
                category_var.get(),
                priority_var.get(),
                date_entry.get(),
                time_entry.get(),
                notes_text.get("1.0", tk.END).strip(),
                [entry.get() for entry in subtask_entries if entry.get()],
                repeat_var.get()
            ),
            style="TButton"
        )
        save_button.pack(side=tk.RIGHT, padx=5, expand=True)
        
        form_frame.grid_columnconfigure(1, weight=1)
    
    def save_new_task(self, window, title, category, priority, date_str, time_str, notes, subtasks, repeat):
        if not title:
            messagebox.showerror("Hata", "Görev başlığı boş olamaz!")
            return
        
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            if time_str:
                datetime.strptime(time_str, "%H:%M")
        except ValueError:
            messagebox.showerror("Hata", "Geçersiz tarih veya saat formatı!")
            return
        
        new_task = {
            "id": len(self.data["tasks"]) + 1,
            "title": title,
            "category": category,
            "priority": priority,
            "due_date": date_str,
            "due_time": time_str,
            "notes": notes,
            "subtasks": [{"title": st, "completed": False} for st in subtasks],
            "completed": False,
            "repeat": repeat,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.data["tasks"].append(new_task)
        self.save_data()
        
        messagebox.showinfo("Başarılı", "Görev başarıyla eklendi!")
        window.destroy()
        self.refresh_ui()
    
    def edit_task(self, task_id):
        task = next((t for t in self.data["tasks"] if t["id"] == task_id), None)
        if not task:
            return
        
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Görevi Düzenle")
        edit_window.geometry("500x600")
        edit_window.configure(bg=self.colors["bg"])
        edit_window.resizable(False, False)
        
        title_label = tk.Label(
            edit_window,
            text="Görevi Düzenle",
            font=("Arial", 14, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        )
        title_label.pack(pady=10)
        
        form_frame = tk.Frame(edit_window, bg=self.colors["bg"])
        form_frame.pack(fill=tk.BOTH, padx=20, pady=10)
        
        tk.Label(
            form_frame,
            text="Görev Başlığı:",
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        ).grid(row=0, column=0, sticky="w", pady=5)
        
        title_entry = ttk.Entry(
            form_frame
        )
        title_entry.insert(0, task["title"])
        title_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
        
        tk.Label(
            form_frame,
            text="Kategori:",
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        ).grid(row=1, column=0, sticky="w", pady=5)
        
        category_var = tk.StringVar(value=task["category"])
        category_menu = ttk.Combobox(
            form_frame,
            textvariable=category_var,
            values=self.categories,
            state="readonly"
        )
        category_menu.grid(row=1, column=1, sticky="ew", pady=5, padx=5)
        
        tk.Label(
            form_frame,
            text="Öncelik:",
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        ).grid(row=2, column=0, sticky="w", pady=5)
        
        priority_var = tk.StringVar(value=task["priority"])
        priority_menu = ttk.Combobox(
            form_frame,
            textvariable=priority_var,
            values=self.priorities,
            state="readonly"
        )
        priority_menu.grid(row=2, column=1, sticky="ew", pady=5, padx=5)
        
        tk.Label(
            form_frame,
            text="Son Tarih:",
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        ).grid(row=3, column=0, sticky="w", pady=5)
        
        date_entry = ttk.Entry(
            form_frame
        )
        date_entry.insert(0, task["due_date"])
        date_entry.grid(row=3, column=1, sticky="ew", pady=5, padx=5)
        
        tk.Label(
            form_frame,
            text="Saat:",
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        ).grid(row=4, column=0, sticky="w", pady=5)
        
        time_entry = ttk.Entry(
            form_frame
        )
        time_entry.insert(0, task["due_time"])
        time_entry.grid(row=4, column=1, sticky="ew", pady=5, padx=5)
        
        tk.Label(
            form_frame,
            text="Notlar:",
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        ).grid(row=5, column=0, sticky="nw", pady=5)
        
        notes_text = tk.Text(
            form_frame,
            bg=self.colors["entry_bg"],
            fg=self.colors["entry_fg"],
            height=5,
            width=30,
            wrap=tk.WORD,
            borderwidth=0
        )
        notes_text.insert("1.0", task["notes"])
        notes_text.grid(row=5, column=1, sticky="ew", pady=5, padx=5)
        
        tk.Label(
            form_frame,
            text="Alt Görevler:",
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        ).grid(row=6, column=0, sticky="nw", pady=5)
        
        subtasks_frame = tk.Frame(form_frame, bg=self.colors["bg"])
        subtasks_frame.grid(row=6, column=1, sticky="ew", pady=5, padx=5)
        
        subtask_entries = []
        subtask_vars = []
        
        def add_subtask_entry(subtask=None):
            frame = tk.Frame(subtasks_frame, bg=self.colors["bg"])
            frame.pack(fill=tk.X, pady=2)
            
            var = tk.BooleanVar(value=subtask["completed"] if subtask else False)
            check = tk.Checkbutton(
                frame,
                variable=var,
                bg=self.colors["bg"],
                activebackground=self.colors["bg"],
                selectcolor=self.colors["entry_bg"]
            )
            check.pack(side=tk.LEFT)
            
            entry = ttk.Entry(
                frame
            )
            if subtask:
                entry.insert(0, subtask["title"])
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            
            subtask_entries.append(entry)
            subtask_vars.append(var)
        
        for subtask in task["subtasks"]:
            add_subtask_entry(subtask)
        
        add_subtask_button = ttk.Button(
            subtasks_frame,
            text="+ Alt Görev Ekle",
            command=lambda: add_subtask_entry(),
            style="TButton"
        )
        add_subtask_button.pack(fill=tk.X, pady=5)
        
        tk.Label(
            form_frame,
            text="Tekrarlama:",
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        ).grid(row=7, column=0, sticky="w", pady=5)
        
        repeat_var = tk.StringVar(value=task["repeat"])
        repeat_menu = ttk.Combobox(
            form_frame,
            textvariable=repeat_var,
            values=["Yok", "Günlük", "Haftalık", "Aylık"],
            state="readonly"
        )
        repeat_menu.grid(row=7, column=1, sticky="ew", pady=5, padx=5)
        
        buttons_frame = tk.Frame(edit_window, bg=self.colors["bg"])
        buttons_frame.pack(fill=tk.X, padx=20, pady=10)
        
        cancel_button = ttk.Button(
            buttons_frame,
            text="İptal",
            command=edit_window.destroy,
            style="TButton"
        )
        cancel_button.pack(side=tk.LEFT, padx=5, expand=True)
        
        save_button = ttk.Button(
            buttons_frame,
            text="Kaydet",
            command=lambda: self.update_task(
                task_id,
                edit_window,
                title_entry.get(),
                category_var.get(),
                priority_var.get(),
                date_entry.get(),
                time_entry.get(),
                notes_text.get("1.0", tk.END).strip(),
                [(entry.get(), var.get()) for entry, var in zip(subtask_entries, subtask_vars)],
                repeat_var.get()
            ),
            style="TButton"
        )
        save_button.pack(side=tk.RIGHT, padx=5, expand=True)
        
        delete_button = ttk.Button(
            buttons_frame,
            text="Sil",
            command=lambda: self.delete_task(task_id, edit_window),
            style="TButton"
        )
        delete_button.pack(side=tk.RIGHT, padx=5, expand=True)
        
        form_frame.grid_columnconfigure(1, weight=1)
    
    def update_task(self, task_id, window, title, category, priority, date_str, time_str, notes, subtasks, repeat):
        if not title:
            messagebox.showerror("Hata", "Görev başlığı boş olamaz!")
            return
        
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            if time_str:
                datetime.strptime(time_str, "%H:%M")
        except ValueError:
            messagebox.showerror("Hata", "Geçersiz tarih veya saat formatı!")
            return
        
        task = next((t for t in self.data["tasks"] if t["id"] == task_id), None)
        if task:
            task["title"] = title
            task["category"] = category
            task["priority"] = priority
            task["due_date"] = date_str
            task["due_time"] = time_str
            task["notes"] = notes
            task["subtasks"] = [{"title": st[0], "completed": st[1]} for st in subtasks if st[0]]
            task["repeat"] = repeat
            
            self.save_data()
            messagebox.showinfo("Başarılı", "Görev başarıyla güncellendi!")
            window.destroy()
            self.refresh_ui()
    
    def delete_task(self, task_id, window=None):
        if not messagebox.askyesno("Onay", "Bu görevi silmek istediğinize emin misiniz?"):
            return
        
        self.data["tasks"] = [t for t in self.data["tasks"] if t["id"] != task_id]
        self.save_data()
        
        if window:
            window.destroy()
        self.refresh_ui()
    
    def move_task_to_tomorrow(self, task_id):
        task = next((t for t in self.data["tasks"] if t["id"] == task_id), None)
        if task:
            today = datetime.now().date()
            tomorrow = today + timedelta(days=1)
            task["due_date"] = tomorrow.strftime("%Y-%m-%d")
            self.save_data()
            self.refresh_ui()
    
    def toggle_task_completion(self, task_id, completed):
        task = next((t for t in self.data["tasks"] if t["id"] == task_id), None)
        if task:
            task["completed"] = completed
            self.save_data()
            self.refresh_ui()
    
    def update_subtask(self, task, subtask, completed):
        for t in self.data["tasks"]:
            if t["id"] == task["id"]:
                for st in t["subtasks"]:
                    if st["title"] == subtask["title"]:
                        st["completed"] = completed
                        break
                break
        self.save_data()
    
    def add_weekly_task(self, start_date, end_date):
        self.add_new_task(start_date)
    
    def check_reminders(self):
        now = datetime.now()
        today = now.date()
        current_time = now.strftime("%H:%M")
        
        for task in self.data["tasks"]:
            if not task["completed"] and task["due_time"]:
                task_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
                if task_date == today and task["due_time"] == current_time:
                    self.show_reminder(task)
        
        self.root.after(60000, self.check_reminders)
    
    def show_reminder(self, task):
        reminder_window = tk.Toplevel(self.root)
        reminder_window.title("Hatırlatıcı")
        reminder_window.geometry("400x300")
        reminder_window.configure(bg=self.colors["bg"])
        reminder_window.resizable(False, False)
        
        try:
            winsound.Beep(1000, 500)
        except:
            pass
        
        title_label = tk.Label(
            reminder_window,
            text="Görev Hatırlatıcı",
            font=("Arial", 14, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        )
        title_label.pack(pady=10)
        
        task_frame = tk.Frame(reminder_window, bg=self.colors["entry_bg"], padx=10, pady=10)
        task_frame.pack(fill=tk.BOTH, padx=20, pady=10)
        
        tk.Label(
            task_frame,
            text=f"Görev: {task['title']}",
            font=("Arial", 12),
            bg=self.colors["entry_bg"],
            fg=self.colors["fg"],
            wraplength=350,
            justify="left"
        ).pack(anchor="w")
        
        tk.Label(
            task_frame,
            text=f"Kategori: {task['category']}",
            font=("Arial", 10),
            bg=self.colors["entry_bg"],
            fg=self.colors["fg"],
            wraplength=350,
            justify="left"
        ).pack(anchor="w", pady=(5, 0))
        
        tk.Label(
            task_frame,
            text=f"Öncelik: {task['priority']}",
            font=("Arial", 10),
            bg=self.colors["entry_bg"],
            fg=self.get_priority_color(task["priority"]),
            wraplength=350,
            justify="left"
        ).pack(anchor="w", pady=(5, 0))
        
        tk.Label(
            task_frame,
            text=f"Zaman: {task['due_time']}",
            font=("Arial", 10),
            bg=self.colors["entry_bg"],
            fg=self.colors["fg"],
            wraplength=350,
            justify="left"
        ).pack(anchor="w", pady=(5, 0))
        
        if task["notes"]:
            tk.Label(
                task_frame,
                text=f"Notlar: {task['notes']}",
                font=("Arial", 10, "italic"),
                bg=self.colors["entry_bg"],
                fg=self.colors["fg"],
                wraplength=350,
                justify="left"
            ).pack(anchor="w", pady=(5, 0))
        
        buttons_frame = tk.Frame(reminder_window, bg=self.colors["bg"])
        buttons_frame.pack(fill=tk.X, padx=20, pady=10)
        
        close_button = ttk.Button(
            buttons_frame,
            text="Kapat",
            command=reminder_window.destroy,
            style="TButton"
        )
        close_button.pack(side=tk.LEFT, padx=5, expand=True)
        
        complete_button = ttk.Button(
            buttons_frame,
            text="Tamamlandı Olarak İşaretle",
            command=lambda: self.complete_task_with_reminder(task["id"], reminder_window),
            style="TButton"
        )
        complete_button.pack(side=tk.RIGHT, padx=5, expand=True)
    
    def complete_task_with_reminder(self, task_id, window):
        self.toggle_task_completion(task_id, True)
        window.destroy()
    
    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Dosyaları", "*.csv"), ("Tüm Dosyalar", "*.*")],
            title="Görevleri CSV Olarak Kaydet"
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("ID,Başlık,Kategori,Öncelik,Tarih,Saat,Notlar,Tamamlandı,Alt Görevler,Oluşturulma Tarihi,Tekrarlama\n")
                
                for task in self.data["tasks"]:
                    subtasks = " | ".join([f"{st['title']} ({'Tamamlandı' if st['completed'] else 'Bekliyor'})" for st in task["subtasks"]])
                    
                    f.write(
                        f"{task['id']},"
                        f"\"{task['title']}\","
                        f"{task['category']},"
                        f"{task['priority']},"
                        f"{task['due_date']},"
                        f"{task['due_time']},"
                        f"\"{task['notes']}\","
                        f"{'Evet' if task['completed'] else 'Hayır'},"
                        f"\"{subtasks}\","
                        f"{task['created_at']},"
                        f"{task['repeat']}\n"
                    )
            
            messagebox.showinfo("Başarılı", f"Görevler başarıyla {file_path} dosyasına kaydedildi!")
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya kaydedilirken bir hata oluştu: {str(e)}")
    
    def refresh_ui(self):
        # Tüm arayüzü yenile
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.setup_ui()
    
    def get_priority_color(self, priority):
        if priority == "Yüksek":
            return self.colors["high_priority"]
        elif priority == "Orta":
            return self.colors["medium_priority"]
        else:
            return self.colors["low_priority"]
    
    def load_data(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if "tasks" not in data:
                        data["tasks"] = []
                    return data
                except json.JSONDecodeError:
                    return {"tasks": []}
        else:
            return {"tasks": []}
    
    def save_data(self):
        with open(self.db_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

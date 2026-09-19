import customtkinter as ctk
from app.services.statistics import StatisticsService


class DashboardView(ctk.CTkFrame):
    """
    A high-fidelity modern dashboard view showing live summary metrics cards
    queried directly from SQLite records, recent history, and contextual quick actions.
    """

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#1A1A1A", corner_radius=0)
        self.controller = controller
        self.stats_service = StatisticsService()

        # Configure stretching layout columns
        self.grid_columnconfigure(0, weight=3)  # Primary data panel space
        self.grid_columnconfigure(1, weight=1)  # Side quick-action column
        self.grid_rowconfigure(2, weight=1)  # Main workspace area row

        self._build_header_banner()
        self._build_metric_grid()
        self._build_detailed_workspace()
        self.refresh_dashboard_data()

    def _build_header_banner(self):
        """Assembles the header context greeting zone."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=2, padx=30, pady=(25, 15), sticky="ew")

        title = ctk.CTkLabel(
            header_frame,
            text="Welcome Back, Athlete!",
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            text_color="#FFFFFF"
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header_frame,
            text="Here is your fitness overview for today. Stay consistent!",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#A1A1AA"
        )
        subtitle.pack(anchor="w", pady=(2, 0))

    def _build_metric_grid(self):
        """Assembles the container space for the summary statistics metrics."""
        self.metrics_container = ctk.CTkFrame(self, fg_color="transparent")
        self.metrics_container.grid(row=1, column=0, padx=(30, 15), pady=10, sticky="nsew")
        for i in range(4):
            self.metrics_container.grid_columnconfigure(i, weight=1)

    def _build_detailed_workspace(self):
        """Assembles the main historical logs display split and quick command deck."""
        # Left Panel: Today's historical listings layout card
        self.logs_panel = ctk.CTkFrame(self, fg_color="#2E2E2E", corner_radius=12)
        self.logs_panel.grid(row=2, column=0, padx=(30, 15), pady=(15, 30), sticky="nsew")

        logs_title = ctk.CTkLabel(
            self.logs_panel,
            text="Recent Activity Performance History",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color="#FFFFFF"
        )
        logs_title.pack(anchor="w", padx=20, pady=(20, 10))

        self.scroll_logs = ctk.CTkScrollableFrame(self.logs_panel, fg_color="transparent")
        self.scroll_logs.pack(fill="both", expand=True, padx=10, pady=(0, 15))

        # Right Panel: Quick Action Palette
        actions_panel = ctk.CTkFrame(self, fg_color="#2E2E2E", corner_radius=12)
        actions_panel.grid(row=1, column=1, rowspan=2, padx=(15, 30), pady=(10, 30), sticky="nsew")

        actions_title = ctk.CTkLabel(
            actions_panel,
            text="Quick Actions",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color="#FFFFFF"
        )
        actions_title.pack(anchor="w", padx=20, pady=(20, 15))

        buttons_config = [
            ("🚀  Start Routine", "#0EA5E9", lambda: self.controller._select_navigation_view("track")),
            ("➕  Quick Add Log", "#22C55E", lambda: self.controller._select_navigation_view("activities")),
            ("🛠️  Create Routine", "transparent", lambda: self.controller._select_navigation_view("routines")),
            ("📈  View Progress", "transparent", lambda: self.controller._select_navigation_view("progress"))
        ]

        for label, bg_color, command_func in buttons_config:
            btn = ctk.CTkButton(
                actions_panel,
                text=label,
                height=42,
                corner_radius=8,
                fg_color=bg_color if bg_color != "transparent" else "transparent",
                border_color="#A1A1AA" if bg_color == "transparent" else None,
                border_width=1 if bg_color == "transparent" else 0,
                text_color="#FFFFFF",
                font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                command=command_func
            )
            btn.pack(fill="x", padx=20, pady=8)

    def refresh_dashboard_data(self):
        """Queries statistical data layers and maps true values into telemetry targets."""
        # 1. Clear old metric widgets out
        for w in self.metrics_container.winfo_children():
            w.destroy()

        # Extract live totals out of SQLite
        data = self.stats_service.get_lifetime_summary()

        cards_data = [
            ("🔥 Lifetime Calories", f"{int(data['total_calories'])} kcal", "Target: 500/day", 0),
            ("⏱️ Total Active Mins", f"{data['total_minutes']} mins", "Goal: 45/day", 1),
            ("👣 Cumulative Steps", f"{data['total_steps']} steps", "Goal: 10,000", 2),
            ("🏆 Active Sessions", f"{data['total_workouts']} logs", "Streak Tier: Normal", 3)
        ]

        for title, val, target, col_idx in cards_data:
            card = ctk.CTkFrame(self.metrics_container, fg_color="#2E2E2E", corner_radius=12)
            card.grid(row=0, column=col_idx, padx=6, pady=5, sticky="nsew")

            lbl_title = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(family="Segoe UI", size=13),
                                     text_color="#A1A1AA")
            lbl_title.pack(anchor="w", padx=15, pady=(15, 2))

            lbl_val = ctk.CTkLabel(card, text=val, font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
                                   text_color="#FFFFFF")
            lbl_val.pack(anchor="w", padx=15, pady=2)

            lbl_tgt = ctk.CTkLabel(card, text=target, font=ctk.CTkFont(family="Segoe UI", size=11, slant="italic"),
                                   text_color="#A3E635")
            lbl_tgt.pack(anchor="w", padx=15, pady=(2, 15))

        # 2. Render localized historical history feed streams below
        for w in self.scroll_logs.winfo_children():
            w.destroy()

        try:
            recent_logs = self.stats_service.db.execute_read("SELECT * FROM activities ORDER BY id DESC LIMIT 4")
        except Exception:
            recent_logs = []

        if not recent_logs:
            empty_lbl = ctk.CTkLabel(
                self.scroll_logs,
                text="No fitness entries completed yet.\nClick 'Quick Add Log' to start recording metrics!",
                font=ctk.CTkFont(family="Segoe UI", size=13),
                text_color="#A1A1AA"
            )
            empty_lbl.pack(pady=50)
        else:
            for row in recent_logs:
                row_strip = ctk.CTkFrame(self.scroll_logs, fg_color="#1A1A1A", corner_radius=8)
                row_strip.pack(fill="x", padx=10, pady=5)

                txt = f"🏃‍♂️ {row['activity_type']} — {row['duration_minutes']} mins spent ({row['log_date']})"
                lbl = ctk.CTkLabel(row_strip, text=txt, font=ctk.CTkFont(size=12), text_color="#FFFFFF")
                lbl.pack(side="left", padx=15, pady=10)

                cal_lbl = ctk.CTkLabel(row_strip, text=f"+{int(row['calories_burned'])} Kcal",
                                       font=ctk.CTkFont(size=12, weight="bold"), text_color="#A3E635")
                cal_lbl.pack(side="right", padx=15)
import customtkinter as ctk


class DashboardView(ctk.CTkFrame):
    """
    A high-fidelity modern dashboard view showing summary telemetry cards,
    today's active logs summary list, and contextual quick-action buttons.
    """

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#1A1A1A", corner_radius=0)
        self.controller = controller

        # Configure stretching layout columns
        self.grid_columnconfigure(0, weight=3)  # Primary data panel space
        self.grid_columnconfigure(1, weight=1)  # Side quick-action column
        self.grid_rowconfigure(1, weight=1)  # Main workspace area row

        self._build_header_banner()
        self._build_metric_grid()
        self._build_detailed_workspace()

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
        """Assembles the row of premium summary statistics metric cards."""
        metrics_container = ctk.CTkFrame(self, fg_color="transparent")
        metrics_container.grid(row=1, column=0, padx=(30, 15), pady=10, sticky="nsew")

        # 4 Columns for our summary statistics metrics
        for i in range(4):
            metrics_container.grid_columnconfigure(i, weight=1)

        cards_data = [
            ("🔥 Calories Burned", "0 kcal", "Today's Target: 500", 0),
            ("⏱️ Active Minutes", "0 mins", "Goal: 45 mins", 1),
            ("👣 Step Counter", "0 steps", "Goal: 10,000", 2),
            ("🔥 Active Streak", "0 days", "Personal Best: 5", 3)
        ]

        for title, val, target, col_idx in cards_data:
            card = ctk.CTkFrame(metrics_container, fg_color="#2E2E2E", corner_radius=12)
            card.grid(row=0, column=col_idx, padx=6, pady=5, sticky="nsew")

            # Internal layout spacing inside the card
            lbl_title = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(family="Segoe UI", size=13),
                                     text_color="#A1A1AA")
            lbl_title.pack(anchor="w", padx=15, pady=(15, 2))

            lbl_val = ctk.CTkLabel(card, text=val, font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
                                   text_color="#FFFFFF")
            lbl_val.pack(anchor="w", padx=15, pady=2)

            lbl_tgt = ctk.CTkLabel(card, text=target, font=ctk.CTkFont(family="Segoe UI", size=11, slant="italic"),
                                   text_color="#A3E635")
            lbl_tgt.pack(anchor="w", padx=15, pady=(2, 15))

    def _build_detailed_workspace(self):
        """Assembles the main data log layout split and the quick action side panel."""
        # Left Side panel: Today's detailed fitness logs
        self.logs_panel = ctk.CTkFrame(self, fg_color="#2E2E2E", corner_radius=12)
        self.logs_panel.grid(row=2, column=0, padx=(30, 15), pady=(15, 30), sticky="nsew")

        logs_title = ctk.CTkLabel(
            self.logs_panel,
            text="Today's Logged Activities",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color="#FFFFFF"
        )
        logs_title.pack(anchor="w", padx=20, pady=(20, 10))

        # Modern empty slate placeholder text
        self.empty_label = ctk.CTkLabel(
            self.logs_panel,
            text="No activities completed today yet.\nClick 'Quick Add Log' to record a workout!",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#A1A1AA",
            justify="center"
        )
        self.empty_label.pack(expand=True, pady=40)

        # Right Side panel: Quick Actions Command Palette
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
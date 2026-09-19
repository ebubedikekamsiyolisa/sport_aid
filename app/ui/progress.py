import customtkinter as ctk
import matplotlib

matplotlib.use("TkAgg")  # Assign matching background drawing engine
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from app.services.statistics import StatisticsService


class ProgressView(ctk.CTkFrame):
    """
    Renders analytics reporting dashboards utilizing Matplotlib.
    Displays lifetime summary cards alongside visual performance tracking charts.
    """

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#1A1A1A", corner_radius=0)
        self.controller = controller
        self.stats_service = StatisticsService()

        # Grid Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=0)  # Summary Cards
        self.grid_rowconfigure(2, weight=1)  # Charts Canvas

        # FIX: Build the charts panel framework first so left_chart_card exists immediately!
        self._build_stats_header()
        self._build_charts_canvas()
        self._build_summary_cards()  # This safely triggers refresh_statistics_metrics now

    def _build_stats_header(self):
        """Assembles title text banner updates."""
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, padx=30, pady=(20, 10), sticky="ew")

        title = ctk.CTkLabel(header, text="📈 Performance Analytics & Progress Tracker",
                             font=ctk.CTkFont(size=22, weight="bold"), text_color="#FFFFFF")
        title.pack(anchor="w")

    def _build_summary_cards(self):
        """Fetches aggregate database counts and constructs a layout row of summary metrics cards."""
        self.summary_container = ctk.CTkFrame(self, fg_color="transparent")
        self.summary_container.grid(row=1, column=0, padx=30, pady=10, sticky="ew")

        for i in range(4):
            self.summary_container.grid_columnconfigure(i, weight=1)

        self.refresh_statistics_metrics()

    def _build_charts_canvas(self):
        """Assembles bottom container frames where graphical vector data charts will generate."""
        self.charts_container = ctk.CTkFrame(self, fg_color="transparent")
        self.charts_container.grid(row=2, column=0, padx=30, pady=(10, 30), sticky="nsew")

        self.charts_container.grid_columnconfigure(0, weight=1)
        self.charts_container.grid_columnconfigure(1, weight=1)
        self.charts_container.grid_rowconfigure(0, weight=1)

        # Left Chart Container: Calories Burned Curve Plot
        self.left_chart_card = ctk.CTkFrame(self.charts_container, fg_color="#2E2E2E", corner_radius=12)
        self.left_chart_card.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="nsew")

        # Right Chart Container: Workout Type Breakdown Distribution
        self.right_chart_card = ctk.CTkFrame(self.charts_container, fg_color="#2E2E2E", corner_radius=12)
        self.right_chart_card.grid(row=0, column=1, padx=(10, 0), pady=5, sticky="nsew")

    def refresh_statistics_metrics(self):
        """Forces an active database reload query to update counters and clear/re-render vector canvas frames."""
        # 1. Re-render individual layout rows of text counters
        for w in self.summary_container.winfo_children():
            w.destroy()

        data = self.stats_service.get_lifetime_summary()

        cards = [
            ("🏆 Total Workouts", f"{data['total_workouts']} sessions", "#0EA5E9"),
            ("⏱️ Total Minutes", f"{data['total_minutes']} mins", "#FFFFFF"),
            ("🔥 Lifetime Calories", f"{int(data['total_calories'])} kcal", "#A3E635"),
            ("📍 Total Distance", f"{round(data['total_distance'], 1)} km", "#22C55E")
        ]

        for idx, (title, value, color) in enumerate(cards):
            card = ctk.CTkFrame(self.summary_container, fg_color="#2E2E2E", corner_radius=10)
            card.grid(row=0, column=idx, padx=5, pady=5, sticky="ew")

            lbl_t = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=12), text_color="#A1A1AA")
            lbl_t.pack(padx=15, pady=(12, 2), anchor="w")
            lbl_v = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=20, weight="bold"), text_color=color)
            lbl_v.pack(padx=15, pady=(0, 12), anchor="w")

        # 2. Clear old embedded charts and inject updated Matplotlib graphs
        for w in self.left_chart_card.winfo_children():
            if not isinstance(w, ctk.CTkLabel):  # Preserve our panel header titles
                w.destroy()
        for w in self.right_chart_card.winfo_children():
            if not isinstance(w, ctk.CTkLabel):
                w.destroy()

        self._render_calories_trend_chart()
        self._render_distribution_pie_chart()

    def _render_calories_trend_chart(self):
        """Plots an elegant trending timeline curve matching our charcoal dark-mode design tokens."""
        cal_data = self.stats_service.get_weekly_calories_burned()

        # Check if title label already exists, if not create it
        title_exists = any(isinstance(w, ctk.CTkLabel) and w.cget("text") == "Recent Energy Expenditure Trend" for w in self.left_chart_card.winfo_children())
        if not title_exists:
            lbl_title = ctk.CTkLabel(self.left_chart_card, text="Recent Energy Expenditure Trend",
                                     font=ctk.CTkFont(size=14, weight="bold"), text_color="#FFFFFF")
            lbl_title.pack(anchor="w", padx=20, pady=(15, 0))

        if not cal_data:
            self._draw_empty_state_label(self.left_chart_card)
            return

        dates = [row[0][5:] for row in cal_data]  # Slice 'YYYY-MM-DD' down to shorter 'MM-DD' format
        burns = [row[1] for row in cal_data]

        # Setup explicit figure mapping layout properties
        fig, ax = plt.subplots(figsize=(4.5, 2.8), facecolor="#2E2E2E")
        ax.set_facecolor("#2E2E2E")

        # Draw the line plot matching our design tokens
        ax.plot(dates, burns, color="#A3E635", marker="o", linewidth=2.5, markersize=6)
        ax.fill_between(dates, burns, color="#A3E635", alpha=0.15)  # Shaded region under the curve

        # Polish text labels alignment, colors, ticks, and spine visibilities
        ax.tick_params(colors="#A1A1AA", labelsize=9)
        ax.grid(True, color="#1A1A1A", linestyle="--", alpha=0.5)
        for spine in ax.spines.values():
            spine.set_color("#1A1A1A")

        fig.tight_layout()

        # Connect the canvas widget to CustomTkinter hierarchy
        canvas = FigureCanvasTkAgg(fig, master=self.left_chart_card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        plt.close(fig)  # Liberate memory allocation loops immediately

    def _render_distribution_pie_chart(self):
        """Plots a polished distribution pie chart showing favorite exercises matching design tokens."""
        dist_data = self.stats_service.get_activity_distribution()

        # Check if title label already exists, if not create it
        title_exists = any(isinstance(w, ctk.CTkLabel) and w.cget("text") == "Activity Volume Breakdown" for w in self.right_chart_card.winfo_children())
        if not title_exists:
            lbl_title = ctk.CTkLabel(self.right_chart_card, text="Activity Volume Breakdown",
                                     font=ctk.CTkFont(size=14, weight="bold"), text_color="#FFFFFF")
            lbl_title.pack(anchor="w", padx=20, pady=(15, 0))

        if not dist_data:
            self._draw_empty_state_label(self.right_chart_card)
            return

        labels = [row[0] for row in dist_data[:5]]  # Capture top 5 items
        volumes = [row[1] for row in dist_data[:5]]

        fig, ax = plt.subplots(figsize=(4.5, 2.8), facecolor="#2E2E2E")
        ax.set_facecolor("#2E2E2E")

        theme_colors = ["#0EA5E9", "#A3E635", "#22C55E", "#EAB308", "#EF4444"]

        # Plot the distribution pie chart matching our design tokens
        wedges, texts, autotexts = ax.pie(
            volumes, labels=labels, autopct="%1.0f%%", startangle=90,
            colors=theme_colors[:len(labels)], textprops=dict(color="#FFFFFF", size=9)
        )

        # Clean up labels text visibility colors
        for text in texts:
            text.set_color("#A1A1AA")
        for autotext in autotexts:
            autotext.set_weight("bold")

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.right_chart_card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        plt.close(fig)

    def _draw_empty_state_label(self, frame_container):
        """Draws a clean, centered text string placeholder layout when logs map empty rows."""
        lbl = ctk.CTkLabel(frame_container,
                           text="Insufficient logging tracking data available.\nRecord multiple entries to unlock visual graphics.",
                           text_color="#A1A1AA", justify="center")
        lbl.pack(expand=True, pady=40)  # Corrected with pady=40 as specified

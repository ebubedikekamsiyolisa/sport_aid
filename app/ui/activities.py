import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from app.database.database import DatabaseManager


class ActivitiesView(ctk.CTkFrame):
    """
    Manages historical sport logs via a dual-pane interface layout:
    Left: An validated entry form to manually log new training logs.
    Right: A scrollable, interactive list showing historical logs with delete capabilities.
    """

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#1A1A1A", corner_radius=0)
        self.controller = controller
        self.db = DatabaseManager()

        # Grid Configuration (Split layout: 45% form panel, 55% history tracking list)
        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=5)
        self.grid_rowconfigure(0, weight=1)

        self._build_input_form_panel()
        self._build_history_display_panel()
        self.refresh_logs_display()

    def _build_input_form_panel(self):
        """Assembles the input form fields inside a premium Slate container card."""
        form_card = ctk.CTkFrame(self, fg_color="#2E2E2E", corner_radius=12)
        form_card.grid(row=0, column=0, padx=(30, 15), pady=30, sticky="nsew")

        title = ctk.CTkLabel(
            form_card,
            text="Log New Activity",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color="#FFFFFF"
        )
        title.pack(anchor="w", padx=25, pady=(25, 15))

        # Field A: Activity Selector Dropdown Choice
        lbl_type = ctk.CTkLabel(form_card, text="Activity Type *", font=ctk.CTkFont(size=12), text_color="#A1A1AA")
        lbl_type.pack(anchor="w", padx=25, pady=(5, 2))
        self.combo_type = ctk.CTkComboBox(
            form_card,
            values=["Running", "Walking", "Cycling", "Skipping", "Swimming", "Jogging", "Push-ups", "Sit-ups", "Squats",
                    "Planks", "Stretching", "Custom Routine"],
            height=35, fg_color="#1A1A1A", border_color="#A1A1AA", text_color="#FFFFFF"
        )
        self.combo_type.pack(fill="x", padx=25, pady=(0, 12))

        # Field B: Duration Input
        lbl_dur = ctk.CTkLabel(form_card, text="Duration (minutes) *", font=ctk.CTkFont(size=12), text_color="#A1A1AA")
        lbl_dur.pack(anchor="w", padx=25, pady=(5, 2))
        self.entry_duration = ctk.CTkEntry(form_card, placeholder_text="e.g. 30", height=35, fg_color="#1A1A1A",
                                           border_color="#A1A1AA", text_color="#FFFFFF")
        self.entry_duration.pack(fill="x", padx=25, pady=(0, 12))

        # Field C: Distance Input
        lbl_dist = ctk.CTkLabel(form_card, text="Distance (Optional km)", font=ctk.CTkFont(size=12),
                                text_color="#A1A1AA")
        lbl_dist.pack(anchor="w", padx=25, pady=(5, 2))
        self.entry_distance = ctk.CTkEntry(form_card, placeholder_text="e.g. 4.2 (Leave 0 if not applicable)",
                                           height=35, fg_color="#1A1A1A", border_color="#A1A1AA", text_color="#FFFFFF")
        self.entry_distance.pack(fill="x", padx=25, pady=(0, 12))

        # Field D: Steps Input
        lbl_steps = ctk.CTkLabel(form_card, text="Steps (Optional)", font=ctk.CTkFont(size=12), text_color="#A1A1AA")
        lbl_steps.pack(anchor="w", padx=25, pady=(5, 2))
        self.entry_steps = ctk.CTkEntry(form_card, placeholder_text="e.g. 6000", height=35, fg_color="#1A1A1A",
                                        border_color="#A1A1AA", text_color="#FFFFFF")
        self.entry_steps.pack(fill="x", padx=25, pady=(0, 12))

        # Field E: Notes Input
        lbl_notes = ctk.CTkLabel(form_card, text="Notes / Commentary", font=ctk.CTkFont(size=12), text_color="#A1A1AA")
        lbl_notes.pack(anchor="w", padx=25, pady=(5, 2))
        self.entry_notes = ctk.CTkEntry(form_card, placeholder_text="How did it feel?", height=35, fg_color="#1A1A1A",
                                        border_color="#A1A1AA", text_color="#FFFFFF")
        self.entry_notes.pack(fill="x", padx=25, pady=(0, 20))

        # Submit Call Action Button
        btn_submit = ctk.CTkButton(
            form_card, text="💾 Save Activity Record", height=42, corner_radius=8,
            fg_color="#22C55E", hover_color="#16A34A", text_color="#FFFFFF",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            command=self._handle_activity_submission
        )
        btn_submit.pack(fill="x", padx=25, pady=5)

    def _build_history_display_panel(self):
        """Assembles the layout framework hosting historical entry listings."""
        self.right_container = ctk.CTkFrame(self, fg_color="transparent")
        self.right_container.grid(row=0, column=1, padx=(15, 30), pady=30, sticky="nsew")
        self.right_container.grid_columnconfigure(0, weight=1)
        self.right_container.grid_rowconfigure(1, weight=1)

        history_title = ctk.CTkLabel(
            self.right_container, text="Workout Activity History Log",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"), text_color="#FFFFFF"
        )
        history_title.grid(row=0, column=0, padx=5, pady=(0, 15), sticky="w")

        # Scrollable container list frame instantiation
        self.scroll_frame = ctk.CTkScrollableFrame(self.right_container, fg_color="#2E2E2E", corner_radius=12)
        self.scroll_frame.grid(row=1, column=0, sticky="nsew")

    def _handle_activity_submission(self):
        """Processes input fields, applies rigorous schema validation, calculations, and saves to database."""
        activity_type = self.combo_type.get()
        raw_duration = self.entry_duration.get().strip()
        raw_distance = self.entry_distance.get().strip() or "0"
        raw_steps = self.entry_steps.get().strip() or "0"
        notes = self.entry_notes.get().strip()
        today_str = datetime.now().strftime("%Y-%m-%d")

        # --- RIGOROUS CORE INPUT VALIDATION PATHS ---
        if not raw_duration:
            messagebox.showerror("Validation Error", "Duration field is mandatory.")
            return

        try:
            duration_minutes = int(raw_duration)
            if duration_minutes <= 0 or duration_minutes > 1440:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Validation Error",
                                 "Duration must be a positive whole number (between 1 and 1440 minutes).")
            return

        try:
            distance_km = float(raw_distance)
            if distance_km < 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Validation Error", "Distance cannot be a negative value.")
            return

        try:
            steps = int(raw_steps)
            if steps < 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Validation Error", "Step counter values must be a positive whole number.")
            return

        # Temporary placeholder logic formula for estimated calorie expenditures
        # (This will be upgraded in Phase 9 with advanced weight-based MET code)
        estimated_calories = duration_minutes * 7.5
        if activity_type in ["Running", "Cycling"]:
            estimated_calories += (distance_km * 45)

        # Write safely to DB using fully parameterized inputs to prevent SQL Injection
        query = """
            INSERT INTO activities (activity_type, duration_minutes, distance_km, steps, calories_burned, log_date, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        try:
            self.db.execute_write(query,
                                  (activity_type, duration_minutes, distance_km, steps, estimated_calories, today_str,
                                   notes))
            messagebox.showinfo("Success", f"{activity_type} activity successfully recorded!")

            # Reset Entry Inputs gracefully
            self.entry_duration.delete(0, 'end')
            self.entry_distance.delete(0, 'end')
            self.entry_steps.delete(0, 'end')
            self.entry_notes.delete(0, 'end')

            # Refresh history component layout updates immediately
            self.refresh_logs_display()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to preserve workout: {e}")

    def refresh_logs_display(self):
        """Extracts history files from storage and builds rows inside our scrollable container frame."""
        # Wipe out active widgets drawn in scroll container
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        try:
            logs = self.db.execute_read("SELECT * FROM activities ORDER BY id DESC")
        except Exception as e:
            error_lbl = ctk.CTkLabel(self.scroll_frame, text=f"Failed to query log registry: {e}", text_color="#EF4444")
            error_lbl.pack(pady=20)
            return

        if not logs:
            empty_lbl = ctk.CTkLabel(
                self.scroll_frame,
                text="No workout activities tracked yet.\nFill out the entry form to log your first exercise record!",
                font=ctk.CTkFont(size=13), text_color="#A1A1AA", justify="center"
            )
            empty_lbl.pack(expand=True, pady=100)
            return

        # Loop and generate styled card elements for every row returned from database
        for index, row in enumerate(logs):
            item_frame = ctk.CTkFrame(self.scroll_frame, fg_color="#1A1A1A", corner_radius=8)
            item_frame.pack(fill="x", padx=10, pady=6)

            # Left sub-info layout block
            info_text = f"🏃‍♂️ {row['activity_type']} — {row['duration_minutes']} mins\n📅 Date: {row['log_date']}"
            if row['distance_km'] > 0:
                info_text += f"  |  📍 {row['distance_km']} km"
            if row['steps'] > 0:
                info_text += f"  |  👣 {row['steps']} steps"
            if row['notes']:
                info_text += f"\n📝 Note: {row['notes']}"

            lbl_info = ctk.CTkLabel(item_frame, text=info_text, font=ctk.CTkFont(size=12), text_color="#FFFFFF",
                                    justify="left", anchor="w")
            lbl_info.pack(side="left", padx=15, pady=12)

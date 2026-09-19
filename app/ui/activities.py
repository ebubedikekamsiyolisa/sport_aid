import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from app.database.database import DatabaseManager
from app.services.calorie_calculator import CalorieCalculator


class ActivitiesView(ctk.CTkFrame):
    """
    Manages historical sport logs via a dual-pane interface layout:
    Left: An input form with robust data checking to manually log new workouts.
    Right: A scrollable, interactive history timeline list.
    """

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#1A1A1A", corner_radius=0)
        self.controller = controller
        self.db = DatabaseManager()

        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=5)
        self.grid_rowconfigure(0, weight=1)

        self._build_input_form_panel()
        self._build_history_display_panel()
        self.refresh_logs_display()

    def _build_input_form_panel(self):
        """Assembles the validated entry inputs."""
        form_card = ctk.CTkFrame(self, fg_color="#2E2E2E", corner_radius=12)
        form_card.grid(row=0, column=0, padx=(30, 15), pady=30, sticky="nsew")

        title = ctk.CTkLabel(form_card, text="Log New Activity", font=ctk.CTkFont(size=18, weight="bold"),
                             text_color="#FFFFFF")
        title.pack(anchor="w", padx=25, pady=(25, 15))

        lbl_type = ctk.CTkLabel(form_card, text="Activity Type *", font=ctk.CTkFont(size=12), text_color="#A1A1AA")
        lbl_type.pack(anchor="w", padx=25, pady=(5, 2))
        self.combo_type = ctk.CTkComboBox(
            form_card,
            values=["Running", "Walking", "Cycling", "Skipping", "Swimming", "Jogging", "Push-ups", "Sit-ups", "Squats",
                    "Planks", "Stretching", "Custom Routine"],
            height=35, fg_color="#1A1A1A", border_color="#A1A1AA"
        )
        self.combo_type.pack(fill="x", padx=25, pady=(0, 12))

        lbl_dur = ctk.CTkLabel(form_card, text="Duration (minutes) *", font=ctk.CTkFont(size=12), text_color="#A1A1AA")
        lbl_dur.pack(anchor="w", padx=25, pady=(5, 2))
        self.entry_duration = ctk.CTkEntry(form_card, placeholder_text="e.g. 30", height=35, fg_color="#1A1A1A",
                                           border_color="#A1A1AA")
        self.entry_duration.pack(fill="x", padx=25, pady=(0, 12))

        lbl_dist = ctk.CTkLabel(form_card, text="Distance (Optional km)", font=ctk.CTkFont(size=12),
                                text_color="#A1A1AA")
        lbl_dist.pack(anchor="w", padx=25, pady=(5, 2))
        self.entry_distance = ctk.CTkEntry(form_card, placeholder_text="e.g. 4.2", height=35, fg_color="#1A1A1A",
                                           border_color="#A1A1AA")
        self.entry_distance.pack(fill="x", padx=25, pady=(0, 12))

        lbl_steps = ctk.CTkLabel(form_card, text="Steps (Optional)", font=ctk.CTkFont(size=12), text_color="#A1A1AA")
        lbl_steps.pack(anchor="w", padx=25, pady=(5, 2))
        self.entry_steps = ctk.CTkEntry(form_card, placeholder_text="e.g. 6000", height=35, fg_color="#1A1A1A",
                                        border_color="#A1A1AA")
        self.entry_steps.pack(fill="x", padx=25, pady=(0, 12))

        lbl_notes = ctk.CTkLabel(form_card, text="Notes", font=ctk.CTkFont(size=12), text_color="#A1A1AA")
        lbl_notes.pack(anchor="w", padx=25, pady=(5, 2))
        self.entry_notes = ctk.CTkEntry(form_card, placeholder_text="How did it feel?", height=35, fg_color="#1A1A1A",
                                        border_color="#A1A1AA")
        self.entry_notes.pack(fill="x", padx=25, pady=(0, 20))

        btn_submit = ctk.CTkButton(
            form_card, text="💾 Save Activity Record", height=42, corner_radius=8,
            fg_color="#22C55E", hover_color="#16A34A", text_color="#FFFFFF", font=ctk.CTkFont(weight="bold"),
            command=self._handle_activity_submission
        )
        btn_submit.pack(fill="x", padx=25, pady=5)

    def _build_history_display_panel(self):
        """Assembles the framework display canvas."""
        self.right_container = ctk.CTkFrame(self, fg_color="transparent")
        self.right_container.grid(row=0, column=1, padx=(15, 30), pady=30, sticky="nsew")
        self.right_container.grid_columnconfigure(0, weight=1)
        self.right_container.grid_rowconfigure(1, weight=1)

        history_title = ctk.CTkLabel(self.right_container, text="Workout Activity History Log",
                                     font=ctk.CTkFont(size=18, weight="bold"), text_color="#FFFFFF")
        history_title.grid(row=0, column=0, padx=5, pady=(0, 15), sticky="w")

        self.scroll_frame = ctk.CTkScrollableFrame(self.right_container, fg_color="#2E2E2E", corner_radius=12)
        self.scroll_frame.grid(row=1, column=0, sticky="nsew")

    def _handle_activity_submission(self):
        """Processes input logs, performs scientific computations, and logs safely to database."""
        activity_type = self.combo_type.get()
        raw_duration = self.entry_duration.get().strip()
        raw_distance = self.entry_distance.get().strip() or "0"
        raw_steps = self.entry_steps.get().strip() or "0"
        notes = self.entry_notes.get().strip()
        today_str = datetime.now().strftime("%Y-%m-%d")

        if not raw_duration:
            messagebox.showerror("Validation Error", "Duration field is mandatory.")
            return

        try:
            duration_minutes = int(raw_duration)
            distance_km = float(raw_distance)
            steps = int(raw_steps)
            if duration_minutes <= 0 or distance_km < 0 or steps < 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Validation Error", "Please provide valid positive numbers for form targets.")
            return

        # --- DYNAMIC MET BIOMETRICS ESTIMATION LOOKUP ---
        user_weight = 70.0  # Secure fallback constant if profile isn't saved yet
        try:
            prof = self.db.execute_read("SELECT weight_kg FROM user_profile LIMIT 1")
            if prof:
                user_weight = prof[0]['weight_kg']
        except Exception:
            pass

        # Calculate using our new scientific service module
        estimated_calories = CalorieCalculator.calculate(activity_type, duration_minutes, user_weight)

        query = """
            INSERT INTO activities (activity_type, duration_minutes, distance_km, steps, calories_burned, log_date, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        try:
            self.db.execute_write(query,
                                  (activity_type, duration_minutes, distance_km, steps, estimated_calories, today_str,
                                   notes))
            messagebox.showinfo("Success", f"{activity_type} activity successfully recorded!")

            self.entry_duration.delete(0, 'end')
            self.entry_distance.delete(0, 'end')
            self.entry_steps.delete(0, 'end')
            self.entry_notes.delete(0, 'end')
            self.refresh_logs_display()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to preserve workout: {e}")

    def refresh_logs_display(self):
        """Extracts files and renders rows cleanly inside our scroll container."""
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        try:
            logs = self.db.execute_read("SELECT * FROM activities ORDER BY id DESC")
        except Exception as e:
            return

        if not logs:
            empty_lbl = ctk.CTkLabel(self.scroll_frame, text="No workout activities tracked yet.", text_color="#A1A1AA")
            empty_lbl.pack(expand=True, pady=100)
            return

        for row in logs:
            item_frame = ctk.CTkFrame(self.scroll_frame, fg_color="#1A1A1A", corner_radius=8)
            item_frame.pack(fill="x", padx=10, pady=6)

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

            cal_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
            cal_frame.pack(side="right", padx=15)

            lbl_cal = ctk.CTkLabel(cal_frame, text=f"{int(row['calories_burned'])} kcal",
                                   font=ctk.CTkFont(size=14, weight="bold"), text_color="#A3E635")
            lbl_cal.pack(side="top")

            lbl_est = ctk.CTkLabel(cal_frame, text="Estimated Calories", font=ctk.CTkFont(size=9, slant="italic"),
                                   text_color="#A1A1AA")
            lbl_est.pack(side="top")

            btn_delete = ctk.CTkButton(
                cal_frame, text="🗑️ Delete", width=60, height=20, corner_radius=4, fg_color="#EF4444",
                hover_color="#DC2626",
                command=lambda lid=row['id']: self._delete_activity_record(lid)
            )
            btn_delete.pack(side="bottom", pady=(4, 0))

    def _delete_activity_record(self, log_id: int):
        if messagebox.askyesno("Confirm Deletion", "Delete this log?"):
            self.db.execute_write("DELETE FROM activities WHERE id = ?", (log_id,))
            self.refresh_logs_display()
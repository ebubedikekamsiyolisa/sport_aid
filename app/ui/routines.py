import customtkinter as ctk
from tkinter import messagebox
from app.database.database import DatabaseManager


class RoutinesView(ctk.CTkFrame):
    """
    Manages structured workout regimes. Allows users to create a routine container shell,
    systematically append individual exercises to specific routines, and view an explicit overview map.
    """

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#1A1A1A", corner_radius=0)
        self.controller = controller
        self.db = DatabaseManager()

        # Grid Configuration (Split canvas: Left for composition, Right for active structural overview mapping)
        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=5)
        self.grid_rowconfigure(0, weight=1)

        self._build_composition_control_panel()
        self._build_overview_display_panel()
        self.reload_routines_context()

    def _build_composition_control_panel(self):
        """Assembles distinct sub-form segments for generating routine names and adding internal exercises."""
        self.left_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.left_scroll.grid(row=0, column=0, padx=(30, 15), pady=20, sticky="nsew")

        # --- SECTION A: CONTAINER GENERATOR ---
        box_container = ctk.CTkFrame(self.left_scroll, fg_color="#2E2E2E", corner_radius=12)
        box_container.pack(fill="x", pady=(0, 15))

        lbl_sec1 = ctk.CTkLabel(box_container, text="✨ Create New Routine Shell",
                                font=ctk.CTkFont(size=16, weight="bold"), text_color="#FFFFFF")
        lbl_sec1.pack(anchor="w", padx=20, pady=(20, 12))

        lbl_name = ctk.CTkLabel(box_container, text="Routine Name *", font=ctk.CTkFont(size=12), text_color="#A1A1AA")
        lbl_name.pack(anchor="w", padx=20, pady=(2, 2))
        self.entry_rname = ctk.CTkEntry(box_container, placeholder_text="e.g. Morning Cardio, Leg Day", height=35,
                                        fg_color="#1A1A1A", border_color="#A1A1AA")
        self.entry_rname.pack(fill="x", padx=20, pady=(0, 15))

        btn_make_r = ctk.CTkButton(
            box_container, text="🏗️ Initialize Routine Shell", height=38, corner_radius=8,
            fg_color="#0EA5E9", hover_color="#0284C7", text_color="#FFFFFF", font=ctk.CTkFont(weight="bold"),
            command=self._handle_routine_creation
        )
        btn_make_r.pack(fill="x", padx=20, pady=(0, 20))

        # --- SECTION B: EXERCISE INJECTOR ---
        box_exercises = ctk.CTkFrame(self.left_scroll, fg_color="#2E2E2E", corner_radius=12)
        box_exercises.pack(fill="x", pady=10)

        lbl_sec2 = ctk.CTkLabel(box_exercises, text="🏋️‍♂️ Append Exercise to Routine",
                                font=ctk.CTkFont(size=16, weight="bold"), text_color="#FFFFFF")
        lbl_sec2.pack(anchor="w", padx=20, pady=(20, 12))

        lbl_target = ctk.CTkLabel(box_exercises, text="Select Target Routine Container *", font=ctk.CTkFont(size=12),
                                  text_color="#A1A1AA")
        lbl_target.pack(anchor="w", padx=20, pady=(2, 2))
        self.combo_target_routine = ctk.CTkComboBox(box_exercises, values=[], height=35, fg_color="#1A1A1A",
                                                    border_color="#A1A1AA")
        self.combo_target_routine.pack(fill="x", padx=20, pady=(0, 12))

        lbl_ex_name = ctk.CTkLabel(box_exercises, text="Exercise Name *", font=ctk.CTkFont(size=12),
                                   text_color="#A1A1AA")
        lbl_ex_name.pack(anchor="w", padx=20, pady=(2, 2))
        self.combo_ex_name = ctk.CTkComboBox(
            box_exercises,
            values=["Jumping Jacks", "Skipping", "Jogging", "Squats", "Plank", "Push-ups", "Sit-ups", "Stretching",
                    "Lunges", "Burpees"],
            height=35, fg_color="#1A1A1A", border_color="#A1A1AA"
        )
        self.combo_ex_name.pack(fill="x", padx=20, pady=(0, 12))

        # Targets grid subsplit rows
        targets_frame = ctk.CTkFrame(box_exercises, fg_color="transparent")
        targets_frame.pack(fill="x", padx=20, pady=(0, 15))
        targets_frame.grid_columnconfigure(0, weight=1)
        targets_frame.grid_columnconfigure(1, weight=1)

        lbl_dur = ctk.CTkLabel(targets_frame, text="Duration (seconds)", font=ctk.CTkFont(size=12),
                               text_color="#A1A1AA")
        lbl_dur.grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.entry_ex_dur = ctk.CTkEntry(targets_frame, placeholder_text="e.g. 60 (or 0)", height=35,
                                         fg_color="#1A1A1A", border_color="#A1A1AA")
        self.entry_ex_dur.grid(row=1, column=0, sticky="ew", padx=(0, 5))

        lbl_reps = ctk.CTkLabel(targets_frame, text="Reps Target", font=ctk.CTkFont(size=12), text_color="#A1A1AA")
        lbl_reps.grid(row=0, column=1, sticky="w", padx=(5, 0))
        self.entry_ex_reps = ctk.CTkEntry(targets_frame, placeholder_text="e.g. 20 (or 0)", height=35,
                                          fg_color="#1A1A1A", border_color="#A1A1AA")
        self.grid_rowconfigure(0, weight=0)
        self.entry_ex_reps.grid(row=1, column=1, sticky="ew", padx=(5, 0))

        btn_add_ex = ctk.CTkButton(
            box_exercises, text="➕ Add Exercise Item", height=38, corner_radius=8,
            fg_color="#22C55E", hover_color="#16A34A", text_color="#FFFFFF", font=ctk.CTkFont(weight="bold"),
            command=self._handle_exercise_addition
        )
        btn_add_ex.pack(fill="x", padx=20, pady=(5, 20))

    def _build_overview_display_panel(self):
        """Assembles the visual workspace showing structured routines and nested maps."""
        self.right_container = ctk.CTkFrame(self, fg_color="transparent")
        self.right_container.grid(row=0, column=1, padx=(15, 30), pady=20, sticky="nsew")
        self.right_container.grid_columnconfigure(0, weight=1)
        self.right_container.grid_rowconfigure(1, weight=1)

        lbl_title = ctk.CTkLabel(self.right_container, text="My Reusable Routine Blueprints",
                                 font=ctk.CTkFont(size=18, weight="bold"), text_color="#FFFFFF")
        lbl_title.grid(row=0, column=0, padx=5, pady=(0, 15), sticky="w")

        self.scroll_routines = ctk.CTkScrollableFrame(self.right_container, fg_color="#2E2E2E", corner_radius=12)
        self.scroll_routines.grid(row=1, column=0, sticky="nsew")

    def _handle_routine_creation(self):
        """Validates shell input and posts container shell into SQLite."""
        name = self.entry_rname.get().strip()
        if not name:
            messagebox.showerror("Validation Error", "Routine Name field cannot be left blank.")
            return

        try:
            self.db.execute_write("INSERT INTO routines (name) VALUES (?)", (name,))
            messagebox.showinfo("Success", f"Routine shell '{name}' successfully created!")
            self.entry_rname.delete(0, 'end')
            self.reload_routines_context()
        except Exception:
            messagebox.showerror("Error", f"A routine blueprint named '{name}' already exists.")

    def _handle_exercise_addition(self):
        """Extracts fields, validates numeric constraints, and appends a record to the target routine mapping."""
        target_routine_name = self.combo_target_routine.get()
        exercise_name = self.combo_ex_name.get()
        raw_dur = self.entry_ex_dur.get().strip() or "0"
        raw_reps = self.entry_ex_reps.get().strip() or "0"

        if not target_routine_name:
            messagebox.showerror("Validation Error", "You must select a target routine container first.")
            return

        try:
            duration = int(raw_dur)
            reps = int(raw_reps)
            if duration < 0 or reps < 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Validation Error", "Targets must be valid positive numbers.")
            return

        try:
            routine_row = self.db.execute_read("SELECT id FROM routines WHERE name = ?", (target_routine_name,))
            if not routine_row:
                return
            routine_id = routine_row[0]['id']

            count_row = self.db.execute_read("SELECT COUNT(*) as total FROM routine_exercises WHERE routine_id = ?",
                                             (routine_id,))
            next_idx = count_row[0]['total'] + 1

            self.db.execute_write(
                "INSERT INTO routine_exercises (routine_id, exercise_name, order_index, target_duration_seconds, target_reps) VALUES (?, ?, ?, ?, ?)",
                (routine_id, exercise_name, next_idx, duration, reps)
            )
            messagebox.showinfo("Success", f"Appended '{exercise_name}' to '{target_routine_name}'!")
            self.entry_ex_dur.delete(0, 'end')
            self.entry_ex_reps.delete(0, 'end')
            self.reload_routines_context()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to map exercise configuration: {e}")

    def reload_routines_context(self):
        """Queries relational records and visually binds elements together inside layout tree blocks."""
        try:
            routines_data = self.db.execute_read("SELECT name FROM routines ORDER BY name ASC")
            r_names = [row['name'] for row in routines_data]
            self.combo_target_routine.configure(values=r_names)
            if r_names and not self.combo_target_routine.get():
                self.combo_target_routine.set(r_names[0])
        except Exception:
            pass

        for widget in self.scroll_routines.winfo_children():
            widget.destroy()

        try:
            all_routines = self.db.execute_read("SELECT * FROM routines ORDER BY id DESC")
        except Exception:
            return

        if not all_routines:
            empty_lbl = ctk.CTkLabel(self.scroll_routines,
                                     text="No workout routines compiled yet.\nUse the left layout tools to initialize blueprints!",
                                     text_color="#A1A1AA")
            empty_lbl.pack(pady=100)
            return

        for r_row in all_routines:
            r_card = ctk.CTkFrame(self.scroll_routines, fg_color="#1A1A1A", corner_radius=10)
            r_card.pack(fill="x", padx=10, pady=8)

        header_strip = ctk.CTkFrame(r_card, fg_color="transparent")

            # --- This section lives inside the 'for r_row in all_routines:' loop of reload_routines_context ---
        header_strip.pack(fill="x", padx=15, pady=(10, 5))

        lbl_r_title = ctk.CTkLabel(
            header_strip,
                text=f"📋 {r_row['name']}",
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color="#A3E635"
        )
        lbl_r_title.pack(side="left")

        btn_del_r = ctk.CTkButton(
                header_strip,
                text="🗑️ Delete Routine",
                width=100,
                height=24,
                fg_color="#EF4444",
                hover_color="#DC2626",
                text_color="#FFFFFF",
                font=ctk.CTkFont(size=11, weight="bold"),
                command=lambda rid=r_row['id']: self._delete_entire_routine(rid)
            )
        btn_del_r.pack(side="right")

         # Extract child exercise models via relational database links
        ex_rows = self.db.execute_read(
                "SELECT * FROM routine_exercises WHERE routine_id = ? ORDER BY order_index ASC",
                (r_row['id'],)
            )

        if not ex_rows:
            lbl_none = ctk.CTkLabel(
                    r_card,
                    text="   (No exercises appended to this blueprint yet)",
                    font=ctk.CTkFont(size=11,italic = True),
                    text_color="#A1A1AA"
                )
            lbl_none.pack(anchor="w", padx=15, pady=(2, 10))
        else:
            for e_row in ex_rows:
                ex_line = ctk.CTkFrame(r_card, fg_color="#2E2E2E", corner_radius=4)
                ex_line.pack(fill="x", padx=20, pady=3)

                details = f"{e_row['order_index']}. {e_row['exercise_name']}"
                spec = []

                if e_row['target_duration_seconds'] > 0:
                    spec.append(f"⏱️ {e_row['target_duration_seconds']}s")
                if e_row['target_reps'] > 0:
                    spec.append(f"🔢 {e_row['target_reps']} reps")

                details_spec = f" — {', '.join(spec)}" if spec else " — Standard Set"

                lbl_ex = ctk.CTkLabel(
                    ex_line,
                    text=details + details_spec,
                    font=ctk.CTkFont(size=12),
                    text_color="#FFFFFF"
                )
                lbl_ex.pack(side="left", padx=10, pady=5)

        def _delete_entire_routine(self, routine_id: int):
            """Removes the matching container shell row from database. Cascades adjustments down via relational links."""
            if messagebox.askyesno("Confirm Drop Action",
                                   "Are you sure you want to permanently erase this routine plan?\nAll child exercises will be purged automatically!"):
                try:
                    self.db.execute_write("DELETE FROM routines WHERE id = ?", (routine_id,))
                    self.reload_routines_context()
                except Exception as e:
                    messagebox.showerror("Error", f"Purge transaction failure: {e}")
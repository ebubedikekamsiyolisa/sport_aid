from app.database.database import DatabaseManager


class StatisticsService:
    """
    Queries historical database log entries to aggregate data metrics,
    lifetime metrics, and structured chart coordinates.
    """

    def __init__(self):
        self.db = DatabaseManager()

    def get_lifetime_summary(self) -> dict:
        """Computes system-wide totals across historical activity logs."""
        query = """
            SELECT 
                COUNT(*) as total_workouts,
                COALESCE(SUM(duration_minutes), 0) as total_minutes,
                COALESCE(SUM(calories_burned), 0) as total_calories,
                COALESCE(SUM(distance_km), 0) as total_distance,
                COALESCE(SUM(steps), 0) as total_steps
            FROM activities
        """
        try:
            rows = self.db.execute_read(query)
            if rows:
                return dict(rows[0])
        except Exception:
            pass

        return {"total_workouts": 0, "total_minutes": 0, "total_calories": 0, "total_distance": 0, "total_steps": 0}

    def get_activity_distribution(self) -> list:
        """Extracts frequency counts grouped by activity types for plotting charts."""
        query = """
            SELECT activity_type, COUNT(*) as volume 
            FROM activities 
            GROUP BY activity_type 
            ORDER BY volume DESC
        """
        try:
            rows = self.db.execute_read(query)
            return [(r["activity_type"], r["volume"]) for r in rows]
        except Exception:
            return []

    def get_weekly_calories_burned(self) -> list:
        """Extracts chronological energy expenditures across the 7 most recent active dates."""
        query = """
            SELECT log_date, SUM(calories_burned) as daily_burn
            FROM activities 
            GROUP BY log_date 
            ORDER BY log_date DESC 
            LIMIT 7
        """
        try:
            rows = self.db.execute_read(query)
            # Reverse data elements to preserve chronological order (Left-to-Right)
            return [(r["log_date"], r["daily_burn"]) for r in reversed(rows)]
        except Exception:
            return []
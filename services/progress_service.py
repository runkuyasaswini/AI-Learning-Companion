from database.db import get_connection
from datetime import datetime, timedelta

class ProgressService:

    @staticmethod
    def get_completed_count(user_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM learning_history
            WHERE user_id = ?
        """, (user_id,))

        count = cursor.fetchone()[0]

        conn.close()

        return count

    @staticmethod
    def get_recent_learning(user_id, limit=5):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                domain,
                topic,
                completed_at
            FROM learning_history
            WHERE user_id = ?
            ORDER BY completed_at DESC
            LIMIT ?
        """, (user_id, limit))

        rows = cursor.fetchall()

        conn.close()

        return rows

    @staticmethod
    def get_domain_progress(user_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                domain,
                COUNT(*) as completed
            FROM learning_history
            WHERE user_id = ?
            GROUP BY domain
        """, (user_id,))

        rows = cursor.fetchall()

        conn.close()

        return rows

    @staticmethod
    def get_average_quiz_score(user_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT AVG(percentage)
            FROM quiz_history
            WHERE user_id = ?
        """, (user_id,))

        avg = cursor.fetchone()[0]

        conn.close()

        if avg is None:
            return 0

        return round(avg, 2)

    @staticmethod
    def get_learning_statistics(user_id):

            return {

                # ---------------- Dashboard ----------------

                "completed_topics":
                    ProgressService.get_completed_count(user_id),

                "average_quiz_score":
                    ProgressService.get_average_quiz_score(user_id),

                "quiz_count":
                    ProgressService.get_quiz_attempt_count(user_id),

                "quiz_attempts":
                    ProgressService.get_quiz_attempt_count(user_id),

                "learning_streak":
                    ProgressService.get_learning_streak(user_id),

                "overall_progress":
                    ProgressService.get_overall_progress(user_id),

                "current_learning":
                    ProgressService.get_current_learning(user_id),

                "recent_learning":
                    ProgressService.get_recent_learning(user_id),

                "domain_progress":
                    ProgressService.get_domain_progress(user_id),

                "total_topics":
                    ProgressService.get_total_topics_by_domain(),

                "achievements":
                    ProgressService.get_achievements(user_id),

                "weak_topics":
                    ProgressService.get_weak_topics(user_id),

                # ---------------- Progress Page ----------------

                "quiz_history":
                    ProgressService.get_quiz_history(user_id),

                "learning_distribution":
                    ProgressService.get_learning_distribution(user_id),

                "learning_insights":
                    ProgressService.get_learning_insights(user_id),

            }
    @staticmethod
    def get_quiz_count(user_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM quiz_history
            WHERE user_id = ?
        """, (user_id,))

        count = cursor.fetchone()[0]

        conn.close()

        return count
    
    @staticmethod
    def get_current_learning(user_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                domain,
                topic,
                completed_at
            FROM learning_history
            WHERE user_id = ?
            ORDER BY completed_at DESC
            LIMIT 1
        """, (user_id,))

        row = cursor.fetchone()

        conn.close()

        return row

    
    @staticmethod
    def get_weak_topics(user_id, limit=3):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                topic,
                AVG(percentage) as avg_score
            FROM quiz_history
            WHERE user_id = ?
            GROUP BY topic
            HAVING avg_score < 70
            ORDER BY avg_score
            LIMIT ?
        """, (user_id, limit))

        rows = cursor.fetchall()

        conn.close()

        return rows
    
    @staticmethod
    def get_achievements(user_id):

        achievements = []

        completed = ProgressService.get_completed_count(
            user_id
        )

        quizzes = ProgressService.get_quiz_count(
            user_id
        )

        average = ProgressService.get_average_quiz_score(
            user_id
        )

        if completed >= 10:
            achievements.append("🎯 10 Topics Completed")

        if quizzes >= 5:
            achievements.append("📝 Quiz Explorer")

        if average >= 80:
            achievements.append("⭐ High Performer")

        if completed >= 1:
            achievements.append("🚀 Learning Started")

        return achievements
    
    @staticmethod
    def get_total_topics_by_domain():

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                course_name,
                COUNT(topics.id) AS total_topics
            FROM courses
            LEFT JOIN topics
                ON topics.course_id = courses.id
            WHERE
                courses.is_active = 1
                AND topics.is_active = 1
            GROUP BY courses.id
        """)

        rows = cursor.fetchall()

        conn.close()

        return {
            row["course_name"]: row["total_topics"]
            for row in rows
        }
    
    # ==========================================================
    # QUIZ ATTEMPTS
    # ==========================================================

    @staticmethod
    def get_quiz_attempt_count(user_id):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM quiz_history
            WHERE user_id = ?
            """,
            (user_id,),
        )

        count = cursor.fetchone()[0]

        conn.close()

        return count
    
    # ==========================================================
    # QUIZ HISTORY
    # ==========================================================

    @staticmethod
    def get_quiz_history(
        user_id,
        limit=10,
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                percentage,
                attempted_at
            FROM quiz_history
            WHERE user_id = ?
            ORDER BY attempted_at
            LIMIT ?
            """,
            (
                user_id,
                limit,
            ),
        )

        rows = cursor.fetchall()

        conn.close()

        return rows
    
    # ==========================================================
    # LEARNING DISTRIBUTION
    # ==========================================================

    @staticmethod
    def get_learning_distribution(
        user_id,
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                domain,
                COUNT(*) AS completed
            FROM learning_history
            WHERE user_id = ?
            GROUP BY domain
            """,
            (user_id,),
        )

        rows = cursor.fetchall()

        conn.close()

        return rows
    
    # ==========================================================
    # LEARNING INSIGHTS
    # ==========================================================

    @staticmethod
    def get_learning_insights(
        user_id,
    ):

        distribution = ProgressService.get_learning_distribution(
            user_id,
        )

        if not distribution:

            return {
                "strongest": "-",
                "needs_focus": "-",
            }

        strongest = max(
            distribution,
            key=lambda x: x["completed"],
        )

        weakest = min(
            distribution,
            key=lambda x: x["completed"],
        )

        return {

            "strongest": strongest["domain"],

            "needs_focus": weakest["domain"],

        }
    
    # ==========================================================
    # LEARNING STREAK
    # ==========================================================

    @staticmethod
    def get_learning_streak(user_id):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT DISTINCT DATE(completed_at) AS learning_date
            FROM learning_history
            WHERE user_id = ?
            ORDER BY learning_date DESC
            """,
            (user_id,),
        )

        rows = cursor.fetchall()

        conn.close()

        if not rows:

            return {
                "current_streak": 0,
                "longest_streak": 0,
                "dates": [],
            }

        dates = [
            datetime.strptime(
                row["learning_date"],
                "%Y-%m-%d",
            ).date()
            for row in rows
        ]

        # -----------------------------
        # Current streak
        # -----------------------------

        today = datetime.today().date()

        if dates[0] == today:
            expected = today

        elif dates[0] == today - timedelta(days=1):
            expected = today - timedelta(days=1)

        else:
            return {
                "current_streak": 0,
                "longest_streak": 1,
                "dates": dates,
            }

        current = 0

        for day in dates:

            if day == expected:

                current += 1

                expected -= timedelta(days=1)

            else:

                break

        # -----------------------------
        # Longest streak
        # -----------------------------

        longest = 1
        streak = 1

        for i in range(1, len(dates)):

            if dates[i - 1] - dates[i] == timedelta(days=1):

                streak += 1

                longest = max(
                    longest,
                    streak,
                )

            else:

                streak = 1

        return {

            "current_streak": current,

            "longest_streak": longest,

            "dates": dates,

        }
    
    # ==========================================================
    # OVERALL PROGRESS
    # ==========================================================

    @staticmethod
    def get_overall_progress(user_id):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM topics
            """
        )

        total_topics = cursor.fetchone()[0]

        completed = ProgressService.get_completed_count(
            user_id
        )

        conn.close()

        if total_topics == 0:

            return 0

        return round(
            completed * 100 / total_topics,
            1,
        )
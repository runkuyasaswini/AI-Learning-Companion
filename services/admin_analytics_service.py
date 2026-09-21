from database.db import get_connection


class AdminAnalyticsService:

    # ======================================================
    # PLATFORM SUMMARY
    # ======================================================

    @staticmethod
    def get_platform_summary():

        conn = get_connection()
        cursor = conn.cursor()

        # Users
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM users
            WHERE role='learner'
            """
        )
        users = cursor.fetchone()[0]

        # Courses
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM courses
            WHERE is_active=1
            """
        )
        courses = cursor.fetchone()[0]

        # Topics
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM topics
            """
        )
        topics = cursor.fetchone()[0]

        # Materials
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM learning_materials
            """
        )
        materials = cursor.fetchone()[0]

        # Quiz Attempts
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM quiz_history
            """
        )
        quiz_attempts = cursor.fetchone()[0]

        # Average Quiz Score
        cursor.execute(
            """
            SELECT AVG(percentage)
            FROM quiz_history
            """
        )

        avg_score = cursor.fetchone()[0]

        if avg_score is None:
            avg_score = 0

        # Topics Completed

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM learning_history
            """
        )

        completed = cursor.fetchone()[0]

        conn.close()

        return {

            "users": users,

            "courses": courses,

            "topics": topics,

            "materials": materials,

            "quiz_attempts": quiz_attempts,

            "average_score": round(avg_score, 2),

            "completed_topics": completed,

        }

    # ======================================================
    # COURSE POPULARITY
    # ======================================================

    @staticmethod
    def get_course_popularity():

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                domain,
                COUNT(*) AS learners
            FROM learning_history
            GROUP BY domain
            ORDER BY learners DESC
            """
        )

        rows = cursor.fetchall()

        conn.close()

        return [dict(row) for row in rows]
    
    # ======================================================
    # MOST LEARNED TOPICS
    # ======================================================

    @staticmethod
    def get_popular_topics(limit=10):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                topic,
                COUNT(*) AS completed
            FROM learning_history
            GROUP BY topic
            ORDER BY completed DESC
            LIMIT ?
            """,
            (limit,),
        )

        rows = cursor.fetchall()

        conn.close()

        return [dict(row) for row in rows]


    # ======================================================
    # WEAKEST TOPICS
    # ======================================================

    @staticmethod
    def get_weak_topics(limit=10):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                topic,
                AVG(percentage) AS avg_score
            FROM quiz_history
            GROUP BY topic
            ORDER BY avg_score ASC
            LIMIT ?
            """,
            (limit,),
        )

        rows = cursor.fetchall()

        conn.close()

        return [dict(row) for row in rows]
    
    # ======================================================
    # TOP LEARNERS
    # ======================================================

    @staticmethod
    def get_top_learners(limit=10):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT

                users.full_name,

                AVG(quiz_history.percentage) AS average_score

            FROM quiz_history

            JOIN users

                ON users.id = quiz_history.user_id

            GROUP BY users.id

            ORDER BY average_score DESC

            LIMIT ?
            """,
            (limit,),
        )

        rows = cursor.fetchall()

        conn.close()

        return [dict(row) for row in rows]
    
    # ======================================================
    # QUIZ PERFORMANCE DISTRIBUTION
    # ======================================================

    @staticmethod
    def get_quiz_distribution():

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT percentage
            FROM quiz_history
            """
        )

        scores = cursor.fetchall()

        conn.close()

        distribution = {

            "Excellent": 0,

            "Good": 0,

            "Average": 0,

            "Needs Improvement": 0,

        }

        for row in scores:

            score = row["percentage"]

            if score >= 90:

                distribution["Excellent"] += 1

            elif score >= 75:

                distribution["Good"] += 1

            elif score >= 50:

                distribution["Average"] += 1

            else:

                distribution["Needs Improvement"] += 1

        return distribution
    

if __name__ == "__main__":

    print()

    print(AdminAnalyticsService.get_platform_summary())

    print()

    print(AdminAnalyticsService.get_course_popularity())

    print()

    print(AdminAnalyticsService.get_popular_topics())

    print()

    print(AdminAnalyticsService.get_top_learners())

    print()

    print(AdminAnalyticsService.get_weak_topics())

    print()

    print(AdminAnalyticsService.get_quiz_distribution())
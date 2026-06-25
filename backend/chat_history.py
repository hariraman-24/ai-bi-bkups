from db_connection import connect_db
import json


class ChatHistory:

    def create_session(self):
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO chat_sessions () VALUES ()")
        conn.commit()

        session_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return session_id

    def save_message(self, session_id, question, sql, response):
        conn = connect_db()
        cursor = conn.cursor()

        query = """
        INSERT INTO chat_messages (session_id, user_question, sql_query, response)
        VALUES (%s, %s, %s, %s)
        """

        # ✅ store JSON safely
        cursor.execute(query, (session_id, question, sql, json.dumps(response)))
        conn.commit()

        cursor.close()
        conn.close()

    def get_last_response(self, session_id):
        conn = connect_db()
        cursor = conn.cursor()

        query = """
        SELECT response
        FROM chat_messages
        WHERE session_id = %s
        ORDER BY message_id DESC
        LIMIT 1
        """

        cursor.execute(query, (session_id,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result and result[0]:
            try:
                return json.loads(result[0])  # ✅ safe parse
            except:
                return None

        return None
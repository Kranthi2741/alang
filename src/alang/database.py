"""
Database management for Alang using SQLite
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any


class Database:
    """SQLite database for storing sessions and messages"""
    
    def __init__(self, db_path: Path):
        """Initialize database
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        self._initialize()
    
    def _initialize(self):
        """Initialize database and create tables"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Enable dict-like access
        
        self._create_tables()
    
    def _create_tables(self):
        """Create necessary tables"""
        cursor = self.conn.cursor()
        
        # Create sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions (id) ON DELETE CASCADE
            )
        """)
        
        # Create tools table (for tool execution history)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tool_executions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                tool_name TEXT NOT NULL,
                arguments TEXT,
                result TEXT,
                success BOOLEAN,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions (id) ON DELETE CASCADE
            )
        """)
        
        # Create indexes for better performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_session_id ON messages(session_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tool_executions_session_id ON tool_executions(session_id)")
        
        self.conn.commit()
    
    def create_session(self, name: str) -> int:
        """Create a new session
        
        Args:
            name: Session name
            
        Returns:
            Session ID
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO sessions (name) VALUES (?)",
            (name,)
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def get_sessions(self) -> List[Dict[str, Any]]:
        """Get all sessions
        
        Returns:
            List of session dictionaries
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, name, created_at, updated_at 
            FROM sessions 
            ORDER BY updated_at DESC
        """)
        
        sessions = []
        for row in cursor.fetchall():
            sessions.append({
                "id": row["id"],
                "name": row["name"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            })
        
        return sessions
    
    def get_session(self, session_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific session
        
        Args:
            session_id: Session ID
            
        Returns:
            Session dictionary or None
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, name, created_at, updated_at FROM sessions WHERE id = ?",
            (session_id,)
        )
        
        row = cursor.fetchone()
        if row:
            return {
                "id": row["id"],
                "name": row["name"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            }
        return None
    
    def update_session(self, session_id: int, name: str) -> bool:
        """Update session name
        
        Args:
            session_id: Session ID
            name: New session name
            
        Returns:
            True if successful, False otherwise
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE sessions SET name = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (name, session_id)
        )
        self.conn.commit()
        return cursor.rowcount > 0
    
    def delete_session(self, session_id: int) -> bool:
        """Delete a session and all its messages
        
        Args:
            session_id: Session ID
            
        Returns:
            True if successful, False otherwise
        """
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def save_message(self, session_id: int, role: str, content: str) -> int:
        """Save a message
        
        Args:
            session_id: Session ID
            role: Message role (user/assistant/system)
            content: Message content
            
        Returns:
            Message ID
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
            (session_id, role, content)
        )
        
        # Update session timestamp
        cursor.execute(
            "UPDATE sessions SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (session_id,)
        )
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_messages(self, session_id: int, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get messages for a session
        
        Args:
            session_id: Session ID
            limit: Optional limit on number of messages
            
        Returns:
            List of message dictionaries
        """
        cursor = self.conn.cursor()
        
        query = """
            SELECT id, role, content, timestamp 
            FROM messages 
            WHERE session_id = ? 
            ORDER BY timestamp ASC
        """
        
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query, (session_id,))
        
        messages = []
        for row in cursor.fetchall():
            messages.append({
                "id": row["id"],
                "role": row["role"],
                "content": row["content"],
                "timestamp": row["timestamp"]
            })
        
        return messages
    
    def save_tool_execution(self, session_id: int, tool_name: str, arguments: Dict, result: Dict, success: bool) -> int:
        """Save a tool execution record
        
        Args:
            session_id: Session ID
            tool_name: Name of the tool
            arguments: Tool arguments
            result: Tool execution result
            success: Whether the execution was successful
            
        Returns:
            Tool execution ID
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT INTO tool_executions 
               (session_id, tool_name, arguments, result, success) 
               VALUES (?, ?, ?, ?, ?)""",
            (
                session_id,
                tool_name,
                json.dumps(arguments),
                json.dumps(result),
                success
            )
        )
        
        # Update session timestamp
        cursor.execute(
            "UPDATE sessions SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (session_id,)
        )
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_tool_executions(self, session_id: int, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get tool executions for a session
        
        Args:
            session_id: Session ID
            limit: Optional limit on number of executions
            
        Returns:
            List of tool execution dictionaries
        """
        cursor = self.conn.cursor()
        
        query = """
            SELECT id, tool_name, arguments, result, success, timestamp 
            FROM tool_executions 
            WHERE session_id = ? 
            ORDER BY timestamp DESC
        """
        
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query, (session_id,))
        
        executions = []
        for row in cursor.fetchall():
            executions.append({
                "id": row["id"],
                "tool_name": row["tool_name"],
                "arguments": json.loads(row["arguments"]),
                "result": json.loads(row["result"]),
                "success": row["success"],
                "timestamp": row["timestamp"]
            })
        
        return executions
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics
        
        Returns:
            Dictionary with statistics
        """
        cursor = self.conn.cursor()
        
        # Session count
        cursor.execute("SELECT COUNT(*) as count FROM sessions")
        session_count = cursor.fetchone()["count"]
        
        # Message count
        cursor.execute("SELECT COUNT(*) as count FROM messages")
        message_count = cursor.fetchone()["count"]
        
        # Tool execution count
        cursor.execute("SELECT COUNT(*) as count FROM tool_executions")
        tool_execution_count = cursor.fetchone()["count"]
        
        # Most recent session
        cursor.execute("""
            SELECT name, updated_at 
            FROM sessions 
            ORDER BY updated_at DESC 
            LIMIT 1
        """)
        recent_session = cursor.fetchone()
        
        return {
            "sessions": session_count,
            "messages": message_count,
            "tool_executions": tool_execution_count,
            "recent_session": {
                "name": recent_session["name"] if recent_session else None,
                "updated_at": recent_session["updated_at"] if recent_session else None
            }
        }
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def __del__(self):
        """Cleanup on deletion"""
        self.close()

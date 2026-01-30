"""
Zen Voice Assistant - Daily Task Management Module
Manages daily tasks with JSON persistence and voice integration.
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import uuid
from logger import get_logger

logger = get_logger(__name__)


class DailyTaskManager:
    """Manages daily tasks with persistent storage."""
    
    def __init__(self, data_file: str = "tasks_data.json"):
        """
        Initialize the task manager.
        
        Args:
            data_file: Path to JSON file for task storage
        """
        self.data_file = data_file
        self.tasks = []
        self._load_tasks()
    
    def _load_tasks(self):
        """Load tasks from JSON file."""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = data.get('tasks', [])
                logger.info(f"Loaded {len(self.tasks)} tasks from {self.data_file}")
            else:
                self.tasks = []
                self._save_tasks()
                logger.info(f"Created new task file: {self.data_file}")
        except Exception as e:
            logger.error(f"Failed to load tasks: {e}")
            self.tasks = []
    
    def _save_tasks(self):
        """Save tasks to JSON file."""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump({'tasks': self.tasks}, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(self.tasks)} tasks to {self.data_file}")
        except Exception as e:
            logger.error(f"Failed to save tasks: {e}")
    
    def add_task(self, title: str, description: str = "", due_date: str = None, 
                 priority: str = "medium") -> Dict:
        """
        Add a new task.
        
        Args:
            title: Task title
            description: Task description (optional)
            due_date: Due date in YYYY-MM-DD format (optional, defaults to today)
            priority: Priority level (high, medium, low)
            
        Returns:
            Created task dictionary
        """
        if due_date is None:
            due_date = datetime.now().strftime("%Y-%m-%d")
        
        task = {
            'id': str(uuid.uuid4()),
            'title': title,
            'description': description,
            'due_date': due_date,
            'priority': priority.lower(),
            'completed': False,
            'created_at': datetime.now().isoformat()
        }
        
        self.tasks.append(task)
        self._save_tasks()
        logger.info(f"Added task: {title}")
        return task
    
    def get_task_by_id(self, task_id: str) -> Optional[Dict]:
        """Get a task by ID."""
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None
    
    def update_task(self, task_id: str, **kwargs) -> bool:
        """
        Update task fields.
        
        Args:
            task_id: Task ID
            **kwargs: Fields to update (title, description, due_date, priority, completed)
            
        Returns:
            True if updated, False if task not found
        """
        task = self.get_task_by_id(task_id)
        if task:
            for key, value in kwargs.items():
                if key in task:
                    task[key] = value
            self._save_tasks()
            logger.info(f"Updated task: {task_id}")
            return True
        return False
    
    def complete_task(self, task_id: str) -> bool:
        """Mark a task as complete."""
        return self.update_task(task_id, completed=True)
    
    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task.
        
        Args:
            task_id: Task ID
            
        Returns:
            True if deleted, False if task not found
        """
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self._save_tasks()
            logger.info(f"Deleted task: {task_id}")
            return True
        return False
    
    def get_tasks_for_today(self) -> List[Dict]:
        """Get all tasks due today."""
        today = datetime.now().strftime("%Y-%m-%d")
        return [task for task in self.tasks if task['due_date'] == today]
    
    def get_tasks_for_week(self) -> List[Dict]:
        """Get all tasks due this week."""
        today = datetime.now()
        week_end = today + timedelta(days=7)
        
        tasks_this_week = []
        for task in self.tasks:
            try:
                task_date = datetime.strptime(task['due_date'], "%Y-%m-%d")
                if today <= task_date <= week_end:
                    tasks_this_week.append(task)
            except ValueError:
                continue
        
        return tasks_this_week
    
    def get_overdue_tasks(self) -> List[Dict]:
        """Get all overdue tasks."""
        today = datetime.now().strftime("%Y-%m-%d")
        overdue = []
        
        for task in self.tasks:
            if not task['completed'] and task['due_date'] < today:
                overdue.append(task)
        
        return overdue
    
    def get_tasks_by_priority(self, priority: str) -> List[Dict]:
        """Get tasks by priority level."""
        return [task for task in self.tasks if task['priority'] == priority.lower()]
    
    def get_pending_tasks(self) -> List[Dict]:
        """Get all pending (not completed) tasks."""
        return [task for task in self.tasks if not task['completed']]
    
    def get_completed_tasks(self) -> List[Dict]:
        """Get all completed tasks."""
        return [task for task in self.tasks if task['completed']]
    
    def get_all_tasks(self) -> List[Dict]:
        """Get all tasks."""
        return self.tasks.copy()
    
    def search_tasks(self, query: str) -> List[Dict]:
        """
        Search tasks by title or description.
        
        Args:
            query: Search query
            
        Returns:
            List of matching tasks
        """
        query_lower = query.lower()
        results = []
        
        for task in self.tasks:
            if (query_lower in task['title'].lower() or 
                query_lower in task['description'].lower()):
                results.append(task)
        
        return results
    
    def get_task_summary(self) -> str:
        """
        Get a summary of tasks for voice announcement.
        
        Returns:
            Summary string
        """
        today_tasks = self.get_tasks_for_today()
        overdue = self.get_overdue_tasks()
        pending = self.get_pending_tasks()
        
        summary_parts = []
        
        if overdue:
            summary_parts.append(f"{len(overdue)} overdue task{'s' if len(overdue) != 1 else ''}")
        
        if today_tasks:
            pending_today = [t for t in today_tasks if not t['completed']]
            if pending_today:
                summary_parts.append(f"{len(pending_today)} task{'s' if len(pending_today) != 1 else ''} for today")
        
        if not summary_parts:
            return "You have no tasks for today. You're all clear!"
        
        summary = "You have " + " and ".join(summary_parts) + "."
        
        # Add details for today's tasks
        if today_tasks:
            pending_today = [t for t in today_tasks if not t['completed']]
            if pending_today and len(pending_today) <= 5:  # Only detail if 5 or fewer
                task_list = []
                for i, task in enumerate(pending_today, 1):
                    priority_marker = "🔴" if task['priority'] == 'high' else "🟡" if task['priority'] == 'medium' else "🟢"
                    task_list.append(f"{i}. {task['title']}")
                
                summary += " Here they are: " + ", ".join(task_list)
        
        return summary
    
    def format_task_for_display(self, task: Dict) -> str:
        """
        Format a task for console/GUI display.
        
        Args:
            task: Task dictionary
            
        Returns:
            Formatted task string
        """
        status = "✓" if task['completed'] else "○"
        priority_emoji = "🔴" if task['priority'] == 'high' else "🟡" if task['priority'] == 'medium' else "🟢"
        
        formatted = f"{status} {priority_emoji} [{task['due_date']}] {task['title']}"
        if task['description']:
            formatted += f"\n   └─ {task['description']}"
        
        return formatted


# Standalone test
if __name__ == "__main__":
    print("=== Zen Daily Task Manager Test ===\n")
    
    # Initialize manager
    manager = DailyTaskManager("test_tasks.json")
    
    # Add some test tasks
    print("Adding test tasks...")
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    task1 = manager.add_task("Morning workout", "30 minutes cardio", today, "high")
    task2 = manager.add_task("Team meeting", "Discuss project updates", today, "medium")
    task3 = manager.add_task("Code review", "Review pull requests", tomorrow, "medium")
    task4 = manager.add_task("Read documentation", "", today, "low")
    
    print(f"✓ Added {len(manager.get_all_tasks())} tasks\n")
    
    # Get today's tasks
    print("Today's tasks:")
    for task in manager.get_tasks_for_today():
        print(f"  {manager.format_task_for_display(task)}")
    print()
    
    # Get task summary
    print("Task summary:")
    print(f"  {manager.get_task_summary()}\n")
    
    # Complete a task
    print("Completing 'Morning workout'...")
    manager.complete_task(task1['id'])
    print(f"✓ Task completed\n")
    
    # Updated summary
    print("Updated task summary:")
    print(f"  {manager.get_task_summary()}\n")
    
    # Search tasks
    print("Searching for 'meeting':")
    results = manager.search_tasks("meeting")
    for task in results:
        print(f"  {manager.format_task_for_display(task)}")
    print()
    
    # Clean up test file
    if os.path.exists("test_tasks.json"):
        os.remove("test_tasks.json")
        print("✓ Test complete! Cleaned up test file.")

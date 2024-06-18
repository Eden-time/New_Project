import json
from datetime import datetime

class Task:
    def __init__(self, title, description, deadline, importance, completed=False):
        self.title = title
        self.description = description
        self.deadline = datetime.strptime(deadline, '%Y-%m-%d')
        self.importance = importance
        self.completed = completed

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'deadline': self.deadline.strftime('%Y-%m-%d'),
            'importance': self.importance,
            'completed': self.completed
        }

class TaskManager:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.filename, 'r') as file:
                self.tasks = [Task(**task) for task in json.load(file)]
        except FileNotFoundError:
            self.tasks = []

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4)

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def list_tasks(self):
        for i, task in enumerate(self.tasks, 1):
            print(f"{i}. {task.title} (Due: {task.deadline.date()}, Importance: {task.importance}, Completed: {task.completed})")

    def complete_task(self, index):
        self.tasks[index - 1].completed = True
        self.save_tasks()

    def delete_task(self, index):
        del self.tasks[index - 1]
        self.save_tasks()

    def prioritize_tasks(self):
        self.tasks.sort(key=lambda x: (x.completed, x.deadline, -x.importance))

    def recommend_tasks(self):
        self.prioritize_tasks()
        recommended = [task for task in self.tasks if not task.completed][:5]
        print("Recommended tasks to focus on:")
        for task in recommended:
            print(f"{task.title} (Due: {task.deadline.date()}, Importance: {task.importance})")

def main():
    manager = TaskManager()

    while True:
        print("\nTask Manager:")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Recommend Tasks")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            title = input("Title: ")
            description = input("Description: ")
            deadline = input("Deadline (YYYY-MM-DD): ")
            importance = int(input("Importance (1-5): "))
            task = Task(title, description, deadline, importance)
            manager.add_task(task)
        elif choice == '2':
            manager.list_tasks()
        elif choice == '3':
            manager.list_tasks()
            index = int(input("Task number to complete: "))
            manager.complete_task(index)
        elif choice == '4':
            manager.list_tasks()
            index = int(input("Task number to delete: "))
            manager.delete_task(index)
        elif choice == '5':
            manager.recommend_tasks()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

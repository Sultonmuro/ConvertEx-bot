from operator import index
from os import remove

toDoList = [
    "Wash dishes", "Clean room", "Start SAT preparations", "Complete Python project"
]
dishes = {
    "Plates", "Cups", "Glasses", "Cutlery"
}

user = input("Enter your name:").capitalize()


total_amount = 15
unwashed_dishes = 10
task_actions ={
    "wash dishes": {
        "message": f"You have {unwashed_dishes} dishes to wash out of {total_amount} including: {dishes}\nPress Enter if you have finished washing dishes.",
        "success": "Great job! You have washed all the dishes.",
        "remove": "Wash dishes"
    },
    "clean room": {
        "message": "To fully clean your room, you have to:\n1. Make your bed\n2. Dust the furniture\n3. Vacuum the floor",
        "success": "Great job! You have cleaned your room.",
        "remove": "Clean room"
    },
    "start sat preparations": {
        "message": "To start your SAT preparations, you have to:\n1. Get a study guide\n2. Create a study schedule\n3. Start with the basics",
        "success": "Great job! You have started your SAT preparations.",
        "remove": "Start SAT preparations"
    },
    "complete python project": {
        "message": "To complete your Python project, you have to:\n1. Understand the project requirements\n2. Create a project plan\n3. Start coding",
        "success": "Great job! You have completed your Python project.",
        "remove": "Complete Python project"
    }
}



print(f"Hello, {user}! Here are the sask you need to complete for today {toDoList}")

while len(toDoList) > 0:
    for i in toDoList:
        print(i)

    task = input("Enter your task: ").strip().lower()

    if task in [t.lower() for t in toDoList]:
        print(f"Great! You have chosen to {task}, good luck!")
        action = task_actions.get(task)

        if action:
            input(action["message"])
            print(action["success"])
            toDoList.remove(action["remove"])

        if len(toDoList) == 0:
            print("Congratulations! You have completed all your tasks for today.")
            break
        else:
            print(f"Now you have {toDoList} tasks to complete.")

    elif task not in [t.lower() for t in toDoList]:
        print("You have your own task? That's fine, I will add it to your list.")
        toDoList.append(task.strip().capitalize())

    else:
        print("Looks like you have entered an invalid task, please try again.")




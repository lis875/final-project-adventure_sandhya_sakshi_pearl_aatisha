import tkinter as tk
from tkinter import messagebox

class StoryNode:
    def __init__(self, text, choices=None):
        self.text = text
        self.choices = choices or []

    def add_choice(self, choice_text, next_node):
        self.choices.append((choice_text, next_node))

class CYOAGame:
    def __init__(self, root, start_node):
        self.root = root
        self.root.title("Choose Your Adventure")
        self.current_node = start_node
        self.create_widgets()

    def create_widgets(self):
        self.story_label = tk.Label(self.root, text=self.current_node.text, wraplength=400, padx=20, pady=20)
        self.story_label.pack()

        self.choice_buttons = []
        for i, (choice_text, _) in enumerate(self.current_node.choices, 1):
            button = tk.Button(self.root, text=choice_text, command=lambda i=i: self.make_choice(i), width=20)
            button.pack(pady=5)
            self.choice_buttons.append(button)

    def make_choice(self, choice):
        if 1 <= choice <= len(self.current_node.choices):
            _, next_node = self.current_node.choices[choice - 1]
            self.current_node = next_node
            self.update_display()
        else:
            messagebox.showinfo("Invalid Choice", "Please select a valid choice.")

    def update_display(self):
        self.story_label.config(text=self.current_node.text)

        # Destroy existing choice buttons
        for button in self.choice_buttons:
            button.destroy()

        # Create new choice buttons
        self.choice_buttons = []
        for i, (choice_text, _) in enumerate(self.current_node.choices, 1):
            button = tk.Button(self.root, text=choice_text, command=lambda i=i: self.make_choice(i), width=20)
            button.pack(pady=5)
            self.choice_buttons.append(button)

        # Check if it's the end of the story
        if not self.current_node.choices:
            messagebox.showinfo("The End", "The adventure has concluded.")
            self.root.destroy()

# Define your story nodes
start_node = StoryNode("You wake up in a futuristic city. Choose your next move.")
node1 = StoryNode("You decide to explore the city. A flying car passes by. What do you do?")
node2 = StoryNode("You choose to stay indoors. Suddenly, a robot knocks on your door. What do you do?")

# Connect the nodes
start_node.add_choice("Explore the city", node1)
start_node.add_choice("Stay indoors", node2)

# Define more story nodes
node3 = StoryNode("You follow the car and discover a hidden rebel base. The rebels ask for your help. What do you do?")
node4 = StoryNode("You continue exploring the city and find a high-tech market. What catches your eye?")

# Connect the nodes
node1.add_choice("Follow the car", node3)
node1.add_choice("Ignore the car", node4)

# Continue the game
node5 = StoryNode("The robot delivers a message from the future, warning of an impending disaster. What do you do?")
node6 = StoryNode("The robot leaves, and you spend the day watching futuristic TV shows. What genre do you choose?")

# Connect the nodes
node2.add_choice("Answer the door", node5)
node2.add_choice("Ignore the door", node6)

# Continue defining more story nodes
node7 = StoryNode("You join the rebels and participate in a daring mission to overthrow the oppressive government. What role do you take?")
node8 = StoryNode("You become a key member of the rebellion, fighting against the oppressive government. The rebels plan a final assault. What's your strategy?")

# Connect the nodes
node3.add_choice("Join the rebels", node7)
node3.add_choice("Decline the offer", node8)

node9 = StoryNode("You purchase a powerful laser gun. Feeling empowered, what's your next move?")
node10 = StoryNode("You immerse yourself in a virtual world, losing track of time and forgetting your initial mission. What's your favorite virtual activity?")

# Connect the nodes
node4.add_choice("Advanced weaponry", node9)
node4.add_choice("Virtual reality headset", node10)

# Conclusion of the story
end_node = StoryNode("The story concludes. Your choices have shaped the destiny of the futuristic city. What is your final reflection?")

# Connect the nodes
node7.add_choice("Reflect on the journey", end_node)
node8.add_choice("Reflect on the journey", end_node)
node9.add_choice("Reflect on the journey", end_node)
node10.add_choice("Reflect on the journey", end_node)

# Create the game and start playing
root = tk.Tk()
game = CYOAGame(root, start_node)
root.mainloop()


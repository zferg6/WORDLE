import tkinter as tk
from tkinter import messagebox
import random

# Load the list of words from a file
def load_words(file_path):
    with open(file_path, 'r') as file:
        return [word.strip().upper() for word in file.readlines()]

class WordleGUI:

    #Creates many of the variables used across the code, and starts the create_widgets() function to start the GUI window
    def __init__(self, root, word_list):
        self.root = root
        self.word_list = word_list
        self.secret = random.choice(word_list)
        self.used_letters = {"correct": set(), "misplaced": set(), "incorrect": set()}
        self.attempts = 6
        self.no_attempts = 0

        self.create_widgets()

    #Creates the GUI window, Entry field, Submit button, Used letters label, and Instructions label
    def create_widgets(self):
        self.root.title("Wordle")

        self.instructions = tk.Label(self.root, text="Guess the 5-letter word:", font=("Arial", 14))
        self.instructions.pack(pady=10)

        self.entry = tk.Entry(self.root, font=("Arial", 14), justify="center")
        self.entry.pack(pady=5)
        self.entry.focus()

        self.submit_button = tk.Button(self.root, text="Submit", command=self.check_guess, font=("Arial", 12))
        self.submit_button.pack(pady=10)

        self.feedback_label = tk.Label(self.root, text="", font=("Courier", 16), justify="center")
        self.feedback_label.pack(pady=10)

        self.used_letters_label = tk.Label(self.root, text="Used Letters:", font=("Arial", 12), justify="left")
        self.used_letters_label.pack(pady=5)

        self.status_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.status_label.pack(pady=10)

    #Creates the Used letters field and the boxes showing the letters' validity
    def update_used_letters(self):
        correct = ", ".join(sorted(self.used_letters['correct'])) or "None"
        misplaced = ", ".join(sorted(self.used_letters['misplaced'])) or "None"
        incorrect = ", ".join(sorted(self.used_letters['incorrect'])) or "None"

        self.used_letters_label.config(
            text=f"Used Letters:\n🟩 Correct: {correct}\n🟨 Misplaced: {misplaced}\n⬜ Incorrect: {incorrect}"
        )

    #Gets the guess from the Entry field and checks to see if it is correct, also creates the Guessed word and Attempts left labels every turn
    def check_guess(self):
        guess = self.entry.get().strip().upper()
        if len(guess) != 5 or not guess.isalpha():   # Deploys pop-up if word is higher or lower than 5 letters, has non-letter characters, or no
            messagebox.showerror("Invalid Input", "Please enter a valid 5-letter word!")
            return

        self.attempts -= 1
        feedback, current_used_letters = self.evaluate_guess(guess)

        self.guessword = tk.Label(self.root, text=f"Guessed Word: {guess}", font=("Arial", 14))
        self.guessword.pack(pady=10)

        self.attemptlabel = tk.Label(self.root, text=f"Attempts Left: {self.attempts}", font=("Arial", 10))
        self.attemptlabel.pack(pady=10)

        self.used_letters["correct"] = current_used_letters["correct"]   # Fully replaces correct letter list
        self.used_letters["misplaced"] = current_used_letters["misplaced"]   #Fully replaces misplaced letter list
        self.used_letters["incorrect"].update(current_used_letters["incorrect"])   #Add to the incorrect list
        self.update_used_letters()

        self.feedback_label.config(text=feedback)

        if guess == self.secret:
            self.status_label.config(text="Congratulations! You've guessed the word!", fg="green")
            self.end_game()
        elif self.attempts <= self.no_attempts:
            self.status_label.config(text=f"Sorry, you've used all attempts. The word was {self.secret}.", fg="red")
            self.end_game()

        self.entry.delete(0, tk.END)

    #Places the guessed letters into their correct slots after each guess
    def evaluate_guess(self, guess):
        feedback = []
        current_used_letters = {"correct": set(), "misplaced": set(), "incorrect": set()}

        for i in range(len(self.secret)):
            if guess[i] == self.secret[i]:
                feedback.append('🟩')  # Correct letter, correct position
                current_used_letters["correct"].add(guess[i])
            elif guess[i] in self.secret:
                feedback.append('🟨')  # Correct letter, wrong position
                current_used_letters["misplaced"].add(guess[i])
            else:
                feedback.append('⬜')  # Letter not in the word
                current_used_letters["incorrect"].add(guess[i])

        return ''.join(feedback), current_used_letters

    #Ends the game when the correct word is guessed or all attemps are used
    def end_game(self):
        self.entry.config(state="disabled")
        self.submit_button.config(state="disabled")

# Main program
if __name__ == "__main__":
    word_list_file = "unique_words.txt"  # Replace with your file path
    word_list = load_words(word_list_file)

    root = tk.Tk()
    app = WordleGUI(root, word_list)
    root.mainloop()

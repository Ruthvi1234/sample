import random
import tkinter as tk
from tkinter import messagebox

class HangmanGame:
    def _init_(self):
        # Create main window
        self.root = tk.Tk()
        self.root.title("Hangman Game")
        self.root.geometry("600x500")
        self.root.configure(bg="#F0F0F0")
        
        # Game variables
        self.words = ['python', 'programming', 'computer', 'keyboard', 'developer', 
                     'algorithm', 'function', 'variable', 'hangman', 'challenge']
        self.word = ""
        self.guessed_letters = []
        self.tries = 6
        self.game_over = False
        
        # Create UI
        self.create_ui()
        
        # Keyboard event binding
        self.root.bind("<KeyPress>", self.handle_keypress)
        
        # Start game
        self.new_game()
    
    def create_ui(self):
        # Title
        title_label = tk.Label(self.root, text="HANGMAN GAME", 
                              font=("Helvetica", 20, "bold"),
                              bg="#F0F0F0", fg="#333333")
        title_label.pack(pady=10)
        
        # Hangman canvas
        self.canvas = tk.Canvas(self.root, width=300, height=200, 
                               bg="white", highlightbackground="gray")
        self.canvas.pack(pady=10)
        
        # Word display
        self.word_display = tk.Label(self.root, text="", 
                                    font=("Courier", 18, "bold"),
                                    bg="#F0F0F0")
        self.word_display.pack(pady=10)
        
        # Guessed letters
        guessed_frame = tk.Frame(self.root, bg="#F0F0F0")
        guessed_frame.pack(fill=tk.X, padx=20)
        
        tk.Label(guessed_frame, text="Guessed Letters:", 
                font=("Helvetica", 12), bg="#F0F0F0").pack(side=tk.LEFT)
                
        self.guessed_display = tk.Label(guessed_frame, text="", 
                                       font=("Helvetica", 12),
                                       bg="#F0F0F0")
        self.guessed_display.pack(side=tk.LEFT, padx=5)
        
        # Tries remaining
        self.tries_label = tk.Label(self.root, text="Tries Left: 6", 
                                   font=("Helvetica", 12, "bold"),
                                   fg="#CC0000", bg="#F0F0F0")
        self.tries_label.pack(pady=5)
        
        # Message display
        self.message = tk.Label(self.root, text="Guess a letter!", 
                               font=("Helvetica", 12, "italic"),
                               bg="#F0F0F0")
        self.message.pack(pady=5)
        
        # Letter buttons (3 rows of keyboard)
        keyboard_frame = tk.Frame(self.root, bg="#F0F0F0")
        keyboard_frame.pack(pady=10)
        
        self.letter_buttons = {}
        
        # Row 1 (Q-P)
        row1 = tk.Frame(keyboard_frame, bg="#F0F0F0")
        row1.pack()
        for letter in "QWERTYUIOP":
            self.create_letter_button(row1, letter)
            
        # Row 2 (A-L)
        row2 = tk.Frame(keyboard_frame, bg="#F0F0F0")
        row2.pack()
        for letter in "ASDFGHJKL":
            self.create_letter_button(row2, letter)
            
        # Row 3 (Z-M)
        row3 = tk.Frame(keyboard_frame, bg="#F0F0F0")
        row3.pack()
        for letter in "ZXCVBNM":
            self.create_letter_button(row3, letter)
        
        # Control buttons
        control_frame = tk.Frame(self.root, bg="#F0F0F0")
        control_frame.pack(pady=10)
        
        tk.Button(control_frame, text="New Game", 
                 command=self.new_game, bg="#4CAF50", fg="white",
                 font=("Helvetica", 10), width=10).pack(side=tk.LEFT, padx=10)
        
        tk.Button(control_frame, text="Quit", 
                 command=self.root.destroy, bg="#F44336", fg="white",
                 font=("Helvetica", 10), width=10).pack(side=tk.LEFT, padx=10)
    
    def create_letter_button(self, parent, letter):
        button = tk.Button(parent, text=letter, width=3, height=1,
                          font=("Helvetica", 10), bg="#E0E0E0",
                          command=lambda l=letter: self.guess_letter(l))
        button.pack(side=tk.LEFT, padx=2, pady=2)
        self.letter_buttons[letter] = button
    
    def draw_hangman(self):
        self.canvas.delete("all")
        
        # Draw gallows
        self.canvas.create_line(50, 180, 250, 180, width=2)  # Base
        self.canvas.create_line(100, 180, 100, 30, width=2)   # Pole
        self.canvas.create_line(100, 30, 175, 30, width=2)    # Top
        self.canvas.create_line(175, 30, 175, 50, width=2)    # Noose
        
        # Draw hangman parts based on wrong guesses
        wrong_guesses = 6 - self.tries
        
        # Head
        if wrong_guesses >= 1:
            self.canvas.create_oval(160, 50, 190, 80, width=2)
        
        # Body
        if wrong_guesses >= 2:
            self.canvas.create_line(175, 80, 175, 130, width=2)
        
        # Left arm
        if wrong_guesses >= 3:
            self.canvas.create_line(175, 90, 145, 110, width=2)
        
        # Right arm
        if wrong_guesses >= 4:
            self.canvas.create_line(175, 90, 205, 110, width=2)
        
        # Left leg
        if wrong_guesses >= 5:
            self.canvas.create_line(175, 130, 145, 160, width=2)
        
        # Right leg
        if wrong_guesses >= 6:
            self.canvas.create_line(175, 130, 205, 160, width=2)
    
    def update_word_display(self):
        display = ""
        for letter in self.word:
            if letter in self.guessed_letters:
                display += letter + " "
            else:
                display += "_ "
        self.word_display.config(text=display)
    
    def update_guessed_display(self):
        self.guessed_display.config(text=", ".join(sorted(self.guessed_letters)))
    
    def handle_keypress(self, event):
        # Handle keyboard input
        if not self.game_over and event.char.isalpha():
            self.guess_letter(event.char.upper())
    
    def guess_letter(self, letter):
        if self.game_over:
            return
            
        letter = letter.lower()
        
        # Check if already guessed
        if letter in self.guessed_letters:
            self.message.config(text=f"You already guessed '{letter}'!")
            return
            
        # Add to guessed letters
        self.guessed_letters.append(letter)
        self.letter_buttons[letter.upper()].config(state="disabled", bg="#BBBBBB")
        
        # Check if in word
        if letter in self.word:
            self.message.config(text=f"Good guess! '{letter}' is in the word.")
        else:
            self.tries -= 1
            self.tries_label.config(text=f"Tries Left: {self.tries}")
            self.message.config(text=f"Sorry, '{letter}' is not in the word.")
        
        # Update displays
        self.update_word_display()
        self.update_guessed_display()
        self.draw_hangman()
        
        # Check game status
        self.check_game_status()
    
    def check_game_status(self):
        # Check if player won
        won = True
        for letter in self.word:
            if letter not in self.guessed_letters:
                won = False
                break
                
        if won:
            self.game_over = True
            self.message.config(text=f"Congratulations! You guessed the word!")
            tk.messagebox.showinfo("You Win!", f"You correctly guessed: {self.word}")
        
        # Check if player lost
        elif self.tries <= 0:
            self.game_over = True
            self.message.config(text=f"Game over! The word was: {self.word}")
            tk.messagebox.showinfo("Game Over", f"You ran out of tries. The word was: {self.word}")
    
    def new_game(self):
        # Reset game state
        self.word = random.choice(self.words).lower()
        self.guessed_letters = []
        self.tries = 6
        self.game_over = False
        
        # Reset UI
        self.message.config(text="Guess a letter!")
        self.tries_label.config(text="Tries Left: 6")
        self.update_word_display()
        self.update_guessed_display()
        self.draw_hangman()
        
        # Reset buttons
        for button in self.letter_buttons.values():
            button.config(state="normal", bg="#E0E0E0")

def run_game():
    game = HangmanGame()
    game.root.mainloop()

# Run the game when the script is executed
if __name__ == "_main_":
    print("runnung hangman")
    run_game()

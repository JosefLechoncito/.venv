import tkinter as tk
import turtle
from PIL import Image, ImageTk

class Game:
    def __init__(self):
        self.score = 0
        self.trash_types = [("plastic", "Non-Biodegradable", "IMAGES\IMAGES\plastic.jpg"),
                            ("fruit peels", "Biodegradable", "IMAGES\IMAGES\pruit_peels.jpg"),
                            ("metal cans", "Non-Biodegradable", "IMAGES\IMAGES\metal_cans.jpg")]
        self.current_trash_index = 0
        self.current_screen = None

    def start_game(self):
        self.root = tk.Tk()
        self.root.title("EcoSort: Trash Savior")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="light blue")  

        self.title_label = tk.Label(self.root, text="EcoSort: Trash Savior", font=("Arial", 20), bg="light blue")
        self.title_label.pack(pady=20)

        self.play_button = tk.Button(self.root, text="Press to Play!", command=self.show_game_instructions, width=20, height=2)
        self.play_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.root.mainloop()

    def show_game_instructions(self):
        self.root.withdraw()
        self.instructions_window = tk.Toplevel()
        self.instructions_window.title("Game Instructions")
        self.instructions_window.attributes('-fullscreen', True)
        self.instructions_window.configure(bg="light blue")  

        instructions_label = tk.Label(self.instructions_window, text="The people of this world do not know how to sort trash and are killing the planet.\nIt is up to you to influence them by showing them your sorting skills.",
                               font=("Arial", 16), justify="center", bg="light blue")
        instructions_label.pack(pady=50)

        ok_button = tk.Button(self.instructions_window, text="OK", command=self.close_instructions)
        ok_button.pack()

    def close_instructions(self):
        self.instructions_window.destroy()
        self.show_game_screen()

    def show_game_screen(self):
        if self.current_screen:
            self.current_screen.destroy()  

        self.game_screen = tk.Toplevel()
        self.game_screen.title("Trash Sorting Game")
        self.game_screen.attributes('-fullscreen', True)

    
        self.current_screen = self.game_screen

        self.game_screen.configure(bg="light green")

        trash_name, self.correct_ans, image_path = self.trash_types[self.current_trash_index]

        self.trash_image = Image.open(image_path)  
        self.trash_image = self.trash_image.resize((100, 100))
        self.trash_image_tk = ImageTk.PhotoImage(self.trash_image)

        self.game_canvas = turtle.ScrolledCanvas(self.game_screen)
        self.game_canvas.pack(fill="both", expand=True)
        self.game_turtle = turtle.RawTurtle(self.game_canvas)
        self.game_turtle.hideturtle()
        self.game_turtle.penup()

        self.game_canvas.config(bg="light green")

        self.trash_label = tk.Label(self.game_screen, text=trash_name, font=("Arial", 20), bg="light green")
        self.trash_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.trash_image_label = tk.Label(self.game_screen, image=self.trash_image_tk, bg="light green")
        self.trash_image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.biodegradable_button = tk.Button(self.game_screen, text="Biodegradable", command=lambda: self.sort_trash("Biodegradable"), width=20, height=2)
        self.biodegradable_button.place(relx=0.3, rely=0.7, anchor=tk.CENTER)

        self.non_biodegradable_button = tk.Button(self.game_screen, text="Non-Biodegradable", command=lambda: self.sort_trash("Non-Biodegradable"), width=20, height=2)
        self.non_biodegradable_button.place(relx=0.7, rely=0.7, anchor=tk.CENTER)

    def sort_trash(self, selected_option):
        if selected_option == self.correct_ans:
            self.score += 1
            self.show_result("Correct!")
        else:
            self.show_result(f"{self.trash_types[self.current_trash_index][0]} belongs on the {self.correct_ans.lower()} trash bin :(")

    def show_result(self, result_text):
        result_window = tk.Toplevel()
        result_window.title("Result")
        result_window.attributes('-fullscreen', True)
        result_label = tk.Label(result_window, text=result_text, font=("Arial", 16))
        result_label.pack(pady=20)
        proceed_button = tk.Button(result_window, text="Proceed", command=lambda: self.proceed_to_next_question(result_window))
        proceed_button.pack()

    def proceed_to_next_question(self, result_window):
        result_window.destroy()
        self.current_trash_index += 1
        if self.current_trash_index < len(self.trash_types):
            self.show_game_screen()
        else:
            self.show_final_score()

    def show_final_score(self):
        final_window = tk.Toplevel()
        final_window.title("Final Score")
        final_window.attributes('-fullscreen', True)

        if self.score >= 3:
            final_window.configure(bg="light blue")
            image_path = "IMAGES\IMAGES\perfect_score_image.png"  
        else:
            final_window.configure(bg="lightcoral")
            image_path = "IMAGES\IMAGES\dad_score_image.jpg"  

        if self.score >= 3:
            final_label = tk.Label(final_window, text="You have successfully influenced people into throwing their garbage in the correct bins.\nThe world is safe again!", font=("Arial", 16))
            final_label.pack(pady=20)
        else:
            final_label = tk.Label(final_window, text="You have unsuccessfully influenced people into segregating their trash.\nThe world has fallen apart.", font=("Arial", 16))
            final_label.pack(pady=20)

        
        image = Image.open(image_path)
        image = image.resize((300, 300)) 
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(final_window, image=photo)
        image_label.image = photo  
        image_label.pack(pady=20)

        retry_button = tk.Button(final_window, text="Retry", command=self.retry_game)
        retry_button.pack(pady=10)
        quit_button = tk.Button(final_window, text="Quit", command=self.root.destroy)
        quit_button.pack()

    def retry_game(self):
        self.score = 0
        self.current_trash_index = 0
        if self.current_screen:
            self.current_screen.destroy()  
        self.show_game_screen()


game = Game()
game.start_game()

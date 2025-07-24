from breezypythongui import EasyFrame
from tkinter import messagebox, Canvas
from PIL import Image, ImageTk

class NutriTrackApp(EasyFrame):
    def __init__(self):
        EasyFrame.__init__(self, title="NutriTrack", width=600, height=400)

        image_path = r"C:\Users\bigto\OneDrive\Desktop\NutriTrack\nutribackground1.webp"
        bg_raw = Image.open(image_path).resize((600, 400))
        self.bg_image = ImageTk.PhotoImage(bg_raw)

        self.canvas = Canvas(self, width=600, height=400)
        self.canvas.place(x=0, y=0)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        self.canvas.create_text(300, 50, text="Welcome to NutriTrack!", font=("Arial", 20), fill="white")
        self.canvas.create_text(300, 100, text="Are you a new user or a returning user?", font=("Arial", 14), fill="white")

        self.new_button = self.addButton("New User", row=0, column=0, command=self.new_user)
        self.return_button = self.addButton("Returning User", row=1, column=0, command=self.returning_user)
        self.new_button.place(x=250, y=150)
        self.return_button.place(x=250, y=190)

    def new_user(self):
        self.destroy()
        NewUserWindow(self)

    def returning_user(self):
        self.destroy()
        ReturningUserWindow(self)

class NewUserWindow(EasyFrame):
    def __init__(self, parent):
        EasyFrame.__init__(self, title="New User Registration", width=500, height=600)
        self.parent = parent

        self.addLabel("Name", row=0, column=0)
        self.nameField = self.addTextField("", row=0, column=1)

        self.addLabel("Age", row=1, column=0)
        self.ageField = self.addTextField("", row=1, column=1)

        self.addLabel("Body Type", row=2, column=0)
        self.bodyGroup = self.addRadiobuttonGroup(row=2, column=1)
        self.bodyGroup.addRadiobutton("Ectomorph")
        self.bodyGroup.addRadiobutton("Mesomorph")
        self.bodyGroup.addRadiobutton("Endomorph")
        self.bodyGroup.addRadiobutton("Other")

        self.addLabel("Current Weight (kg)", row=4, column=0)
        self.currentWeightField = self.addTextField("", row=4, column=1)

        self.addLabel("Goal Weight (kg)", row=5, column=0)
        self.goalWeightField = self.addTextField("", row=5, column=1)

        self.addLabel("Height (cm)", row=6, column=0)
        self.heightField = self.addTextField("", row=6, column=1)

        self.addLabel("Dietary Preference", row=8, column=0)
        self.dietGroup = self.addRadiobuttonGroup(row=8, column=1)
        self.dietGroup.addRadiobutton("None")
        self.dietGroup.addRadiobutton("Vegetarian")
        self.dietGroup.addRadiobutton("Vegan")
        self.dietGroup.addRadiobutton("Keto")

        self.addLabel("Activity Level", row=10, column=0)
        self.activityGroup = self.addRadiobuttonGroup(row=10, column=1)
        self.activityGroup.addRadiobutton("Sedentary")
        self.activityGroup.addRadiobutton("Moderate")
        self.activityGroup.addRadiobutton("Active")

        self.addButton("Submit", row=12, column=0, columnspan=2, command=self.submit_user_info)

    def submit_user_info(self):
        name = self.nameField.getText()
        age = self.ageField.getText()
        body_type = self.bodyGroup.getSelectedButton()["text"]
        current_weight = self.currentWeightField.getText()
        goal_weight = self.goalWeightField.getText()
        height = self.heightField.getText()
        diet_choice = self.dietGroup.getSelectedButton()["text"]
        activity_choice = self.activityGroup.getSelectedButton()["text"]

        if not all([name, age, body_type, current_weight, goal_weight, height, diet_choice, activity_choice]):
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

        try:
            with open("newUsers.txt", "a") as f:
                f.write(f"{name},{age},{body_type},{current_weight},{goal_weight},{height},{diet_choice},{activity_choice}\n")
            messagebox.showinfo("Registration Successful", "Now let’s create your login info.")
            self.destroy()
            CreateLoginWindow(self.parent, name)
        except Exception as e:
            messagebox.showerror("File Error", f"Could not save your info: {e}")

class CreateLoginWindow(EasyFrame):
    def __init__(self, parent, username):
        EasyFrame.__init__(self, title="Create Login Info", width=350, height=200)
        self.parent = parent
        self.username = username

        self.addLabel("Create Username", row=0, column=0)
        self.usernameField = self.addTextField("", row=0, column=1)

        self.addLabel("Create Password", row=1, column=0)
        self.passwordField = self.addTextField("", row=1, column=1)

        self.addButton("Save Login Info", row=2, column=0, columnspan=2, command=self.save_login_info)

    def save_login_info(self):
        username = self.usernameField.getText()
        password = self.passwordField.getText()

        if not username or not password:
            messagebox.showerror("Input Error", "Please enter both username and password.")
            return

        try:
            with open("login.txt", "a") as f:
                f.write(f"{username},{password}\n")
            messagebox.showinfo("Login Created", "Your login info has been saved!")
            self.destroy()
            WelcomeLegendWindow(self.parent, self.username)
        except Exception as e:
            messagebox.showerror("File Error", f"Could not save login info: {e}")

class ReturningUserWindow(EasyFrame):
    def __init__(self, parent):
        EasyFrame.__init__(self, title="Returning User Login", width=300, height=200)
        self.parent = parent

        self.addLabel("Username", row=0, column=0)
        self.usernameField = self.addTextField("", row=0, column=1)

        self.addLabel("Password", row=1, column=0)
        self.passwordField = self.addTextField("", row=1, column=1)

        self.addButton("Login", row=2, column=0, columnspan=2, command=self.login_user)

    def login_user(self):
        username = self.usernameField.getText()
        password = self.passwordField.getText()

        if not username or not password:
            messagebox.showerror("Login Error", "Please enter both username and password.")
            return

        try:
            with open("login.txt", "r") as f:
                for line in f:
                    saved_username, saved_password = line.strip().split(",")
                    if saved_username == username and saved_password == password:
                        messagebox.showinfo("Login Successful", f"Welcome back, {username}!")
                        self.destroy()
                        WelcomeLegendWindow(self.parent, username)
                        return
            messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")
        except:
            messagebox.showerror("Login Error", "Could not read login file.")

class WelcomeLegendWindow(EasyFrame):
    def __init__(self, parent, username):
        EasyFrame.__init__(self, title="Welcome Legend", width=500, height=500)
        self.parent = parent
        self.username = username

        self.addLabel("I SEE YOU LEGEND", row=0, column=0, columnspan=2, font=("Arial", 24))

        try:
            image_path = r"C:\Users\bigto\OneDrive\Desktop\NutriTrack\legend.webp"
            raw_image = Image.open(image_path).resize((400, 300))
            self.legend_image = ImageTk.PhotoImage(raw_image)

            self.canvas = Canvas(self, width=400, height=300)
            self.canvas.place(x=50, y=50)
            self.canvas.create_image(0, 0, anchor="nw", image=self.legend_image)
        except:
            self.addLabel("Image not found.", row=1, column=0)

        self.addButton("Next", row=3, column=0, columnspan=2, command=self.to_profile)

    def to_profile(self):
     self.destroy()
     self.profile_window = ProfileWindow(self.parent, self.username)

class ProfileWindow(EasyFrame):
    def __init__(self, parent, username):
        EasyFrame.__init__(self, title="User Profile", width=500, height=350)
        self.parent = parent
        self.username = username

        user_data = self.get_user_data(username)
        if user_data:
            name, age, body_type, current_weight, goal_weight, height, diet, activity = user_data

            try:
                height_m = float(height) / 100
                weight_kg = float(current_weight)
                bmi = round(weight_kg / (height_m ** 2), 1)
                bmi_msg = f"Your BMI is {bmi} — a good baseline for your journey."
            except:
                bmi = "Unavailable"
                bmi_msg = "We couldn't calculate your BMI."

            # 🎉 Welcome summary
            message = f"Welcome, {username}! Let's crush that goal of {goal_weight} kg. You've got this! 💪"

            self.addLabel(message, row=0, column=0, columnspan=2, font=("Arial", 14))
            self.addLabel(bmi_msg, row=1, column=0, columnspan=2, font=("Arial", 12))
            self.addLabel(f"Current Weight: {current_weight} kg", row=2, column=0)
            self.addLabel(f"Goal Weight: {goal_weight} kg", row=2, column=1)
            self.addLabel(f"Dietary Preference: {diet}", row=3, column=0)
            self.addLabel(f"Activity Level: {activity}", row=3, column=1)
        else:
            self.addLabel("User profile data not found.", row=0, column=0)

        self.addButton("Log a Meal", row=5, column=0)
        self.addButton("View Progress", row=5, column=1)
        self.addButton("Exit", row=6, column=0, columnspan=2, command=self.close)

    def get_user_data(self, username):
        try:
            with open("newUsers.txt", "r") as f:
                for line in f:
                    fields = line.strip().split(",")
                    if fields and fields[0] == username and len(fields) == 8:
                        return fields
        except:
            return None
        return None

    def close(self):
        self.destroy()

if __name__ == "__main__":
    NutriTrackApp().mainloop()
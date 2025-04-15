import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

class Project:
    def __init__(self):
        pass

    @staticmethod
    def validate_credentials(file_path, username, password):
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    stored_username, stored_password = line.strip().split(',')
                    if username == stored_username and password == stored_password:
                        return True
        except FileNotFoundError:
            print(f"Error: '{file_path}' not found.")
        return False

    def login(self):
        while True:
            user_type = input("Are you a student or an admin? ").strip().lower()
            if user_type == 'student':
                file_path = r'password.txt'
                break
            elif user_type == 'admin':
                file_path = r'adminpassword.txt'
                break
            else:
                print("Invalid user type. Please enter 'student' or 'admin'.")

        user_login = input("Enter your username: ")
        password_login = input("Enter your password: ")

        if not os.path.exists(file_path):
            print(f"File does not exist: {file_path}")
            return None, None

        if self.validate_credentials(file_path, user_login, password_login):
            print(f"Login successful. Welcome, {user_type}!")
            return user_type, user_login
        else:
            print("Invalid username or password. Please try again.")
            return None, None

    def register_user(self):
        username = input("Enter your username: ")
        file_path = r'password.txt'
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                for line in f:
                    if line.split(',')[0] == username:
                        print("Username already exists. Try a different one.")
                        return

        password = input("Enter your password: ")
        password_confirm = input('Confirm password: ')

        if password != password_confirm:
            print("Passwords don't match, please retype.")
        elif len(password) <= 7:
            print('Password is too short. It must be at least 8 characters long.')
        else:
            with open(file_path, 'a') as credentials_file:
                credentials_file.write(f"{username},{password}\n")
            print("User registered successfully!")

    def register_admin(self):
        username = input("Enter your username: ")
        file_path = r'adminpassword.txt'
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                for line in f:
                    if line.split(',')[0] == username:
                        print("Admin username already exists. Try a different one.")
                        return

        password = input("Enter your password: ")
        password_confirm = input('Confirm password: ')

        if password != password_confirm:
            print("Passwords don't match, please retype.")
        elif len(password) <= 7:
            print('Password is too short. It must be at least 8 characters long.')
        else:
            with open(file_path, 'a') as credentials_file:
                credentials_file.write(f"{username},{password}\n")
            print("Admin registered successfully!")

    def add_marks(self):
        student_name = input("Enter student's name: ")
        try:
            data_science = float(input("Enter the marks of DataScience: "))
            it = float(input('Enter the marks of IT: '))
            fom = float(input("Enter the marks of FOM: "))
            academic_english = float(input("Enter the marks of Academic English: "))
            itf = float(input('Enter the marks of ITF: '))
            with open('grades.txt', 'a') as grade_file:
                grade_file.write(f"{student_name},{data_science},{it},{fom},{academic_english},{itf}\n")
            print('Marks added successfully!')
        except ValueError:
            print("Invalid input. Please enter numeric values for marks.")

    def display_marks(self):
        try:
            df = pd.read_csv('grades.txt', header=None, names=["Name", "DataScience", "IT", "FOM", "AcademicEnglish", "ITF"])
            print("\n📋 Student Grades Table:")
            print(df)

            # Convert columns to numeric
            for col in ["DataScience", "IT", "FOM", "AcademicEnglish", "ITF"]:
                df[col] = pd.to_numeric(df[col], errors='coerce')

            # Compute individual averages
            df['Average'] = df.iloc[:, 1:].mean(axis=1, skipna=True)
            print("\n📊 Average Marks Per Student:")
            print(df[['Name', 'Average']])

            # Compute class average per subject
            class_averages = df.iloc[:, 1:-1].mean()
            print("\n🏫 Class Average Per Subject:")
            for subject, avg in class_averages.items():
                print(f"{subject}: {avg:.2f}")

            # Plot
            plt.figure(figsize=(10, 5))
            plt.bar(df['Name'], df['Average'], color='skyblue')
            plt.xlabel('Students')
            plt.ylabel('Average Marks')
            plt.title('Average Marks per Student')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

        except FileNotFoundError:
            print("Grades file not found.")
        except pd.errors.EmptyDataError:
            print("Grades file is empty or improperly formatted.")

    def add_eca(self):
        std = input("Enter student's username: ")
        sports = input("Interested sport: ")
        club = input("Joined clubs: ")
        services = input('Engaged in any services: ')
        more = input('Any other activities done: ')

        with open('eca.txt', 'a') as eca_file:
            eca_file.write(f'Username: {std}\nSports joined: {sports}\nClubs joined: {club}\nServices: {services}\nMore: {more}\n')
        print('ECA details added successfully!')

    def view_eca(self):
        username = input("Enter student's username: ")
        found = False

        try:
            with open('eca.txt', 'r') as eca_file:
                eca_data = eca_file.readlines()

            for i, line in enumerate(eca_data):
                if line.strip().startswith('Username:'):
                    if line.strip().split(': ')[1] == username:
                        found = True
                        print("Student's ECA details:")
                        for j in range(i, i + 5):
                            print(eca_data[j].strip())
                        break

            if not found:
                print("No ECA details found for the given username.")
        except FileNotFoundError:
            print("ECA file not found.")

    def delete_user(self):
        username = input("Enter the username of the user you want to delete: ")
        try:
            with open('password.txt', 'r') as file:
                lines = file.readlines()

            with open('password.txt', 'w') as file:
                for line in lines:
                    if not line.startswith(username + ','):
                        file.write(line)

            print(f"User '{username}' deleted successfully.")
        except FileNotFoundError:
            print("User file not found.")

# Main driver code
if __name__ == '__main__':
    project = Project()
    while True:
        print("\n1. Login")
        print("2. Register as a user")
        print("3. Register as an admin")

        try:
            choice = int(input("Enter a choice (1-3): ").strip())
        except ValueError:
            print("Please enter a valid number.")
            continue

        if choice == 1:
            user_type, username = project.login()
            if user_type:
                if user_type == 'student':
                    print("\n1. View ECA details")
                    print("2. View grades")
                    try:
                        action_choice = int(input("Enter your choice: ").strip())
                        if action_choice == 1:
                            project.view_eca()
                        elif action_choice == 2:
                            project.display_marks()
                        else:
                            print("Invalid choice.")
                    except ValueError:
                        print("Please enter a valid number.")
                elif user_type == 'admin':
                    print("\n1. Add user")
                    print("2. Delete user")
                    print("3. Add grades to a student")
                    print("4. Add ECA details to a student")
                    try:
                        action_choice = int(input("Enter your choice: ").strip())
                        if action_choice == 1:
                            project.register_user()
                        elif action_choice == 2:
                            project.delete_user()
                        elif action_choice == 3:
                            project.add_marks()
                        elif action_choice == 4:
                            project.add_eca()
                        else:
                            print("Invalid choice.")
                    except ValueError:
                        print("Please enter a valid number.")
        elif choice == 2:
            project.register_user()
        elif choice == 3:
            project.register_admin()
        else:
            print("Invalid choice.")

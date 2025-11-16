# import use case functions 
from app.use_cases.user_registration import register
from app.use_cases.user_login import login
from app.use_cases.view_profile import view_profile
from app.use_cases.edit_profile import edit_profile
from app.use_cases.follow_user import follow_user

from app.use_cases.unfollow_user import unfollow_user
from app.use_cases.view_friends import view_friends
from app.use_cases.friend_recommend import rec_friends 

WELCOME_MESSAGE = """
================================\n\nWELCOME TO THE APPLICATION!\n
================================\n
    Please select an option:\n
    1. UC-1: User Registration\n
    2. UC-2: User Login\n
    (*) exit: Exit the application\n"""

INTERFCE_MESSAGE = """
    Please select an option:\n
    ================================\n
    3.  UC-3: View Profile\n
    4.  UC-4: Edit Profile\n
    5.  UC-5: Follow Another User\n
    6.  UC-6: Unfollow a User\n
    7.  UC-7: View Friends\n 
    8.  UC-8: Mutual Connections\n
    9.  UC-9: Friend Recommendations\n
    10. UC-10: Search Users\n
    11. UC-11: Explore Popular Users\n
    (*) quit: Logout\n"""


username = ""

def main(): 
    print(WELCOME_MESSAGE)

    while True: 
        choice = input("Enter your choice (1, 2, exit): ").strip() 
        # Register a user
        if choice == '1': # IMPLEMENTED
            temp_username = input("Username: ").strip()
            password = input("Password: ").strip()
            name = input("Name: ").strip()
            email = input("Email: ").strip()
            registration_success = register(temp_username, password, name, email)

        # Login a user 
        elif choice == '2': # IMPLEMENTED
            global username
            # username will be saved in the global variable, and can be passed into other functions
            # refer to UC-3 and UC-4 implementations for examples
            username = input("Username: ").strip() 
            password = input("Password: ").strip()
            login_success = login(username, password)

            if login_success:
                while True:     
                    print(INTERFCE_MESSAGE)
                    choice = input("Enter your choice (3, 4, 5, 6, 7, 8, 9, 10, 11, quit): ").strip()
                    ###############################
                    ### Other use cases go here ###
                    ###############################

                    if choice == '3': # IMPLEMENTED
                        print("View Profile Selected")
                        view_profile(username)


                    elif choice == '4': # IMPLEMENTED
                        print("Edit Profile Selected")
                        edit_profile(username)

                    elif choice == '5': # IMPLEMENTED
                        print("Follow Another User")
                        follow_user(username)
                    elif choice == '6':
                        print("Unfollow a User - Testing")
                        unfollow_user(username)
                        #########################
                        ### TO BE IMPLEMENTED ###
                        #########################
                    elif choice == '7':
                        print("View Friends - Testing")
                        view_friends(username)
                        #########################
                        ### TO BE IMPLEMENTED ###
                        #########################
                    elif choice == '8':
                        print("Mutual Connections - To be implemented")
                        #########################
                        ### TO BE IMPLEMENTED ###
                        #########################
                    elif choice == '9':
                        print("Friend Recommendations - Testing")
                        rec_friends(username)
                        #########################
                        ### TO BE IMPLEMENTED ###
                        #########################
                    elif choice == '10':
                        print("Search Users - To be implemented")
                        #########################
                        ### TO BE IMPLEMENTED ###
                        #########################
                    elif choice == '11':
                        print("Explore Popular Users - To be implemented")
                        #########################
                        ### TO BE IMPLEMENTED ###
                        #########################
                    elif choice.lower() == 'quit':
                        print("Logging out. Returning to main menu.")
                        username = ""
                        break
                    else:
                        print("Invalid choice. Returning to main menu.")

        elif choice.lower() == 'exit': 
            print("Exiting the application. Goodbye!")
            break

        else: 
            print("Invalid choice. Please try again.")



if __name__ == "__main__":
    main()
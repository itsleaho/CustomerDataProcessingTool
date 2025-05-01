import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
import hashlib
from tkinter import *
from tkinter import messagebox
from tkinter import ttk


def load_data(file_path): #Function to load the data from the spreadsheet
    try: #Try and except statements used to catch errors
        data = pd.read_csv(file_path) #Loads the customer data
        data['Date'] = pd.to_datetime(data['Date'])
        return data #Returns the data as a DataFrame
    except FileNotFoundError: #Catch the error when the file has not been found
        print("no file found")
        messagebox.showerror("Error", "No file found. \nEnsure that customer_data.csv exists, then try again.")
        #Displays an error
        return None
    

def display_statistics(data, display):
    #Function to display statistics when 'Display statistics' button is pressed

    print("\n--- Data Statistics ---")
    display.config(text=data.describe())
    #Applies statistical variables to data and sets it as the text for the display label

    print(data.describe())
    

def generate_trend(data, display):
    #Function to display line chart and numerical chart information when 'Generate Trend Report' is pressed
    
    data['Timestamp'] = data['Date'].apply(lambda x: x.timestamp())
    #Converts 'date' in spreadsheet into numerical format 'timestamp'

    x = data['Timestamp']
    y = data['PurchaseAmount']
    #Defines x and y axis for line chart
    
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    #Perform linear regression

    data['Trend'] = intercept + slope * x
    #Creates the trend

    plt.figure(figsize=(10, 6))
    plt.scatter(data['Date'], data['PurchaseAmount'], label='Actual Data', color='blue')
    plt.plot(data['Date'], data['Trend'], label='Trend Line', color='red')
    plt.title('Customer Purchase Trends Over Time')
    plt.xlabel('Date')
    plt.ylabel('Purchase Amount')
    plt.legend()
    plt.show()
    #Creates the physical line chart including legend, labels, plotting etc.

    display.config(text=f"\n--- Trend Line Information ---\nSlope: {slope}\nIntercept: {intercept}\nR-squared: {r_value**2}\nP-value: {p_value}\nStandard Error: {std_err}")
    #Displays numerical information about the graph in the display label in the main menu
    

def display_data(data, display): #Function to display data when 'display data' button is pressed
    print("\n--- Loaded Data ---")
    print(data)

    display.config(text=data)
    #Displays raw data in the display label in main menu
    
    

def authenticate(authPage, usernameEntry, passwordEntry): #Authenticate function which runs on startup
    authorised = False #Boolean variable to be used later to check if user should have access

    auth = pd.read_csv('auth.csv')
    #Reads from authentication Excel spreadsheet
    
    username = str(hashlib.md5(usernameEntry.get().encode()).hexdigest())
    password = str(hashlib.md5(passwordEntry.get().encode()).hexdigest())
    #Encodes inputs into md5 hashes and casts them as strings

    for i in range(len(auth)): #For each value in the DataFrame
        if str(auth['Username'][i]) == username and str(auth['Password'][i]) == password:
            #If the username and password entries in the same row match the user inputted credentials
            print("\nAccess granted!")
            messagebox.showinfo("Granted", "Access Granted!") #Displays a message window
            authPage.destroy() #Closes the authentication window
            authPage.quit()
            #Prevents the mainloop for authPage to continuously run after the window shuts down
            
            authorised = True #User is authenticated
            main_menu() #Calls the function to display the main menu
            break
            

    if authorised == False: #If the user is not authenticated
        print("Incorrect username or password. Please try again.")
        messagebox.showerror("Denied", "Incorrect username or password. Please try again.")
        #Displays message window
        

def main_menu(): #Function to start the main menu when authentication returns 'True'
    file_path = 'customer_data.csv'
    data = load_data(file_path)
    #Reads the customer data spreadsheet and loads into the file

    if data is not None: #If data in the spreadsheet is not empty
        if True: #If authentication is set to true
            root = Tk() #Defines the main menu's window
            root.title("Customer Data Processing Tool")
            Label(root, text="Customer Data Processing Tool").grid(row=0, column=0)

            display = Label(root)
            display.grid(row=1, column=0)
            #Defines the label which is used to display data when a button is pressed

            Button(root, text="Display data", command=lambda *args: display_data(data, display)).grid(row=2, column=0)
            Button(root, text="Display statistics", command=lambda *args: display_statistics(data, display)).grid(row=2, column=1)
            Button(root, text="Generate trend report", command=lambda *args: generate_trend(data, display)).grid(row=3, column=0)
            Button(root, text="Exit", command=lambda *args: quit()).grid(row=3, column=1)
            #Defines the buttons for each function and applies them to the grid

            root.mainloop()
            #Defines the mainloop to allow the window to keep running
        

def main():
    authPage = Tk() #The main window for the authentication page
    authPage.title("Customer Data Processing Tool") #Defining the title

    Label(authPage, text="Please authenticate below").grid(row=0, column=0) #Initialises a label on the top of the window
    
    Label(authPage, text="Username").grid(row=1, column=0)
    usernameEntry = Entry(authPage)
    usernameEntry.grid(row=2, column=0) #Grid is used to display the label and its positioning
    
    Label(authPage, text="Password").grid(row=1, column=1)
    passwordEntry = Entry(authPage, show="*")
    passwordEntry.grid(row=2, column=1)
    #The 'show' attribute is used to define how any inputs should be displayed as

    Button(authPage, text="Submit", command = lambda *args: authenticate(authPage, usernameEntry, passwordEntry)).grid(row=3, column=0)
    #Defines the submit button - the 'command' attribute defines the function to be called on click
    #lambda *args is used to allow the function to wait until the button is pressed.

    authPage.mainloop() #Mainloop allows the Tkinter GUI to continuously run and update


if __name__ == "__main__":
    main() #Calls the main function only if the main file is being run

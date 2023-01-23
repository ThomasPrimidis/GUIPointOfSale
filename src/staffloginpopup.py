import tkinter as tk

class StaffLoginPopup(tk.Toplevel):
    """Screen asking for staff credentials to give access to staff page.

    Class instantiation is triggered by the customer page and if staff
    log in successfully, the class informs the customer page which then
    instantiates the staff page on top. The log in page is then deleted.
    It also informs the user if log in is unsuccessful.

    Attributes:
        self.invoker (Customer page instance): The customer page
    """

    def __init__(self, invoker):
        """Initialise the page"""
        tk.Toplevel.__init__(self, bg="white", padx=300, pady=150)

        if (invoker is None):
            raise TypeError

        try:
            name = invoker.getPageName()
            if (not isinstance(name, str)):
                raise TypeError
            if (not name in ["customerPage", "staffPage"]):
                raise ValueError
        except:
            raise TypeError

        self.invoker = invoker 
        self.grab_set() # Do not allow the user to use other windows while page is up
        self.geometry(self.invoker.root.winfo_geometry())
        self.resizable(False,False)
        self.title("Staff login")
        self.iconbitmap(r"../resources/staffLogo.ico")
        self.dictUsersAndPasswords = {"abc":"123", "thomas": "primidis"}
        self.successfullLogin = False

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)
        self.rowconfigure(3,weight=1)
        self.rowconfigure(4,weight=1)
        self.rowconfigure(5,weight=1)
        self.rowconfigure(6,weight=1)
        self.rowconfigure(7,weight=1)
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)

        #username label and text entry box
        self.usernameLabel = tk.Label(self, text="Username", bg = "white", font = "Calibri 20 bold")
        self.usernameLabel.grid(row=0, column=0, columnspan = 2, sticky = "news")
        self.username = tk.StringVar()
        self.usernameEntry = tk.Entry(self, textvariable=self.username, font = "Calibri 20", justify="center")
        self.usernameEntry.grid(row=1, column=0, columnspan = 2, sticky = "news")
        self.usernameEntry.focus()
        self.usernameEntry.bind("<Return>", self._quickLogin)
        
        #password label and password entry box
        self.passwordLabel = tk.Label(self,text="Password", bg = "white", font = "Calibri 20 bold")
        self.passwordLabel.grid(row=2, column=0, columnspan = 2, sticky = "news")
        self.password = tk.StringVar()  
        self.passwordEntry = tk.Entry(self, textvariable=self.password, show="*", font = "Calibri 20", justify="center")
        self.passwordEntry.grid(row=3, column=0, columnspan = 2, sticky = "news")
        self.passwordEntry.bind("<Return>", self._quickLogin)

        #login button
        self.loginButton = tk.Button(self, text="Log in", font = "Calibri 20 bold", bg = "black", fg = "white", command=self._onValidateLogin)
        self.loginButton.grid(row=4, column=0, columnspan = 2, sticky = "news", pady = 10)  

        #clear entries button
        self.clearEntriesButton = tk.Button(self, text="Clear", font = "Calibri 20 bold", command=self._onClearEntries)
        self.clearEntriesButton.grid(row=6, column=0, sticky = "news")

        #cancel button
        self.cancelButton = tk.Button(self, text="Cancel", font = "Calibri 20 bold", command=self._onCancel)
        self.cancelButton.grid(row=6, column=1, sticky = "news")  

        self.errorMessage = tk.Label(self, text="", bg = "white", fg = "red", font = "Calibri 10 bold")
        self.errorMessage.grid(row=7, column=0, columnspan=2, sticky = "news")

    def _quickLogin(self, event):
        """Trigger the log in button by pressing enter"""
        self._onValidateLogin()

    def _onValidateLogin(self):
        """Check entered credentials and act accordingly."""
        self.errorMessage.config(text = "")
        self.successfullLogin = False
        # if both username and password are correct
        if (self.username.get() in self.dictUsersAndPasswords.keys()):
            if (self.password.get() == self.dictUsersAndPasswords[self.username.get()]):
                self.successfullLogin = True
                # Tell the customer page to open the staff page
                self.invoker.openStorePage(self.username.get())
        # Tell user to try again
        if (not self.successfullLogin):
            self.errorMessage.after(100, lambda: self.errorMessage.config(text = "Username or password are incorrect. Please try again."))
            self._onClearEntries()

    def _onCancel(self):
        """Close the login page and return to the customer's page."""
        self.successfullLogin = False
        self.destroy()

    def _onClearEntries(self):
        """Clear the username and password entries."""
        self.usernameEntry.delete(0,"end")
        self.passwordEntry.delete(0,"end")

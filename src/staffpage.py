import tkinter as tk
import baskettotalwidget
import staffpagecontrols
import checkout

class StaffPage(tk.Toplevel):
    """The pop up page for staff access to the basket

    The page creates a copy of the customer's basket which is ammended
    by staff using controls found also on this page. Controls are
    addition and removal of 1 item of a specific category, the removal
    of all items of a specific category and the removal of all items
    of all categories. Staff can cancel without applying their changes
    to the customer's basket or confirm their changes and do so.

    Attributes:
        customerPage (CustomerPage instance): The customer page
    
        staffUsername (string): Username of logged in user

    Methods:
        onBasketUpdated(self,listItemCodeAndaction="all", signalStrength = "strong")
    """

    def __init__(self, customerPage, staffUsername):
        """Initialise the staff page.

        Parameters:
            customerPage (CustomerPage instance): The customer page

            staffUsername (string): Username of logged in user
        """

        tk.Toplevel.__init__(self, bg="white", padx=20, pady=20) 

        if (not isinstance(staffUsername, str)):
            raise TypeError
    
        if (customerPage is None):
            raise TypeError

        try:
            name = customerPage.getPageName()
            if (not isinstance(name, str)):
                raise TypeError
            if (not name in ["customerPage", "staffPage"]):
                raise ValueError
        except:
            raise TypeError
          
        # Initialise if no exceptions are raised
        self.grab_set() # Do not allow the user to use other windows while page is up
        self.customerPage = customerPage
        self.staffUsername = staffUsername
        self.geometry(self.customerPage.root.winfo_geometry())
        self.resizable(False,False)
        self.title("Store login")
        self.iconbitmap(r"../resources/staffLogo.ico")

        # copy constructor for the checkout class: copy data from customer page checkout class
        self._checkout = checkout.Checkout(orig=self.customerPage.getCheckout())

        # 3 rows, 1 for the header, 1 for the individual item controls and 1 for the whole basket controls
        self.rowconfigure(0,weight=0)
        self.rowconfigure(1,weight=0)
        self.rowconfigure(2,weight=1)
        self.columnconfigure(0, weight=1)

        # The frames for each row
        #------------------------------------------------------------------------
        self.headerFrame = tk.LabelFrame(self, bg="#51990F", bd=0, highlightthickness=0, highlightbackground="#C5E0B4")
        self.headerFrame.grid(row=0, column=0, sticky="ew")
        self.headerFrame.columnconfigure(0,weight=1)
        self.headerFrame.columnconfigure(1,weight=0)
        self.headerFrame.rowconfigure(0,weight=1)

        self.itemsControlsFrame = tk.LabelFrame(self, bg="#51990F", bd=0, highlightthickness=0, highlightbackground="#C5E0B4")
        self.itemsControlsFrame.grid(row=1, column=0, sticky="new")
        self.itemsControlsFrame.rowconfigure(0,weight=1)
        self.itemsControlsFrame.rowconfigure(1,weight=1)
        self.itemsControlsFrame.rowconfigure(2,weight=1)
        self.itemsControlsFrame.columnconfigure(0,weight=1)

        self.basketControlsFrame = tk.LabelFrame(self, bg="white", bd=0, highlightthickness=0, highlightbackground="#C5E0B4")
        self.basketControlsFrame.grid(row=2, column=0, sticky = "sew")
        self.basketControlsFrame.columnconfigure(0,weight=0)
        self.basketControlsFrame.columnconfigure(1,weight=1)
        self.basketControlsFrame.columnconfigure(2,weight=1)
        self.basketControlsFrame.columnconfigure(3,weight=0)
        self.basketControlsFrame.rowconfigure(0,weight=1)

        # Header items
        #------------------------------------------------------------------------
        # the date and time
        self.labelLoggedinUser=tk.Label(self.headerFrame, text = "Staff username: {}".format(self.staffUsername),  font = "Calibri 20 bold", bg="#51990F", padx=10)
        self.labelLoggedinUser.grid(row=0, column=0, sticky="w")

        # the return to front page button without applying the changes
        self.btnReturnToFront = tk.Button(self.headerFrame,text="Cancel", font = "Calibri",
          bg="#C0DE0C", activebackground="#C5E0B4", command=self._onCancel)
        self.btnReturnToFront.grid(row=0, column=1, sticky="e")

        # individual item and basket controls
        #------------------------------------------------------------------------
        # the empty basket button
        self.btnEmptyBasket = tk.Button(self.basketControlsFrame,
          text="Empty basket",
          font = "Calibri 20 bold",
          bg="#F2A876", activebackground="#F5C19D", bd=0, command=self._onEmptyBasketClicked)
        self.btnEmptyBasket.grid(row=0, column=0, sticky="news",padx=5, pady=5)

        # The basket total widget
        self.basketTotalWidget =  baskettotalwidget.BasketTotalWidget(self.basketControlsFrame)
        self.basketTotalWidget.grid(row=0, column=2, sticky="ew", padx=5, pady=5)
        self._checkout.register(self.basketTotalWidget)

        # the confirm changes button
        self.btnConfirmChanges = tk.Button(self.basketControlsFrame,
          text="Confirm\nchanges",
          font = "Calibri 20 bold",
          bg="#d446b5", activebackground="#db64c1", bd=0, command=self._onConfirm)
        self.btnConfirmChanges.grid(row=0, column=3, sticky="news",padx=5, pady=5)

        # The individual item controls
        itemCategoriesInBasket = self._checkout.getItemCategoriesInBasket()
        self.dictItemControlsWidgets = {}
        for index, itemCode in enumerate(itemCategoriesInBasket):
            itemControl = staffpagecontrols.StaffPageControls(
                self.itemsControlsFrame,
                self._checkout.getItemsCatalogue()[itemCode])

            self.dictItemControlsWidgets[itemCode]=itemControl
            self.dictItemControlsWidgets[itemCode].grid(row=index, column=0, sticky="news", padx=0, pady=0)
            self._checkout.register(self.dictItemControlsWidgets[itemCode])

        # trigger signal after all widgets have been drawn to update their data
        self._checkout.signal()

    def _onCancel(self):
        """Close the staff page and return to the customer page"""

        self.destroy()

    def _onConfirm(self):
        """Apply the basket changes to the basket in the customer page
        and close the staff page
        """

        self._checkout.copyTo(self.customerPage.getCheckout())
        self.destroy()

    def _onEmptyBasketClicked(self):
        """Action for when the Empty basket button is clicked by staff"""

        self.onBasketUpdated(signalStrength="weak")

    def onBasketUpdated(self,listItemCodeAndaction="all", signalStrength = "strong"):
        """Add or remove 1 item from the basket or remove all of 1
        category or remove everything from the basket
        """

        if (not isinstance(listItemCodeAndaction, str)):
            raise TypeError
        if (not (len(listItemCodeAndaction) <= 3 and 
            (listItemCodeAndaction=="all"
            or listItemCodeAndaction.endswith("-A")
            or not listItemCodeAndaction in self._checkout.getBasket().keys()))):
            raise ValueError
        if (not isinstance(signalStrength, str)):
            raise TypeError
        if (not signalStrength in ["weak", "strong"]):
            raise ValueError

        # Remove all items
        if (listItemCodeAndaction == "all"):
            self._checkout.clearBasket(signalStrength=signalStrength)
            return
        # Remove all items that belong to a specific category
        elif (listItemCodeAndaction.endswith("-A")):
            self._checkout.clearBasket(listItemCodeAndaction[0], "weak")
        # add or remove 1 item
        else:
            itemCode = listItemCodeAndaction[0]
            action=int(listItemCodeAndaction[1:3])
            if (action==-1):
                self._checkout.unscan(itemCode, signalStrength)
            elif (action==1):
                self._checkout.scan(itemCode, signalStrength)
            elif (action==0):
                self._checkout.clearBasket(itemCode, signalStrength)

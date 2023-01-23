import tkinter as tk
import tkinter.ttk as ttk
import checkout
import baskettotalwidget
import iteminfocard
import staffpage
import staffloginpopup
from time import strftime

class CustomerPage:
    """ The main graphical user interface of the application.

    The application allows the user to add up to 3 different
    items in their basket and see the status of their shopping
    dynamically. The page also has a button to allow staff
    login for advanced controls on the customer's basket.
    """

    def __init__(self):
        """Initialise the page"""

        # default constructor for the checkout engine class
        self._checkout = checkout.Checkout()

        # root with 2 rows
        self.root = tk.Tk()
        self.root.geometry("1000x700+10+10")
        self.root.resizable(False,False)
        self.root.title("Point of sale")
        self.root.iconbitmap(r"../resources/shoppingCart.ico")

        # Main window has 2 rows
        self.root.rowconfigure(0,weight=0)
        self.root.rowconfigure(1,weight=1)
        self.root.columnconfigure(0,weight=1)

        # frame for the date and time and the store login button
        self.headerFrame = tk.LabelFrame(self.root, bg="#51990F", bd=0, highlightthickness=0, highlightbackground="#C5E0B4")
        # frame is positioned on the top row of the parent (root)
        self.headerFrame.grid(row=0, column=0, sticky="ew")

        # frame has 2 columns, 1 for the date and time and one for the store login button
        self.headerFrame.columnconfigure(0,weight=4)
        self.headerFrame.columnconfigure(1,weight=0)
        self.headerFrame.rowconfigure(0,weight=1)

        # the date and time
        self.labelTime=tk.Label(self.headerFrame,bg="#51990F", padx=10)
        self.labelTime.grid(row=0, column=0, sticky="w")
        
        self.btnStaffLogin = tk.Button(self.headerFrame,text="Store login", font = "Calibri", bg="#C0DE0C", activebackground="#C5E0B4", command=self._staffLogin)
        self.btnStaffLogin.grid(row=0, column=1, sticky="e")

        # frame for the user controls
        self.shoppingFrame = tk.LabelFrame(self.root, bg="white", padx=20, pady=20, bd=0)
        # frame is positioned on the bottom row of the parent (root)
        self.shoppingFrame.grid(row=1,column=0, sticky="news")

        # frame has 2 columns, one for the scan buttons and 1 for the list of scanned items+total
        self.shoppingFrame.columnconfigure(0,weight=1)
        self.shoppingFrame.columnconfigure(1,weight=1)
        self.shoppingFrame.rowconfigure(0,weight=1)

        # frame for the scan item buttons
        self.scanButtonsFrame = tk.LabelFrame(self.shoppingFrame, bg="white", padx = 10, pady=10, width=250, bd=0, highlightthickness=0, highlightbackground="darkgrey")
        # frame has 3 rows, 1 for each button
        self.scanButtonsFrame.rowconfigure(0,weight=1)
        self.scanButtonsFrame.rowconfigure(1,weight=1)
        self.scanButtonsFrame.rowconfigure(2,weight=1)
        self.scanButtonsFrame.columnconfigure(0,weight=1)

        # frame is positioned on the left side of the bottom row of the parent (root)
        self.scanButtonsFrame.grid(row=0,column=0, sticky="news", padx=10)
        self.scanButtonsFrame.grid_propagate(False)

        # The scan apple button
        photoScanApple = tk.PhotoImage(file = r"../resources/AppleIcon.png").subsample(6,6)
        self.btnScanApple = \
          tk.Button(self.scanButtonsFrame,
          text = "Apple",
          font = "Calibri 20 bold",
          image=photoScanApple,
          compound=tk.BOTTOM,
          bg="white", activebackground="white",
          bd=2,
          command = lambda: self.onBasketUpdated("A+1"))
        self.btnScanApple.grid(row=0, column=0, sticky="news", pady=3)

        # The scan banana button
        photoScanBanana = tk.PhotoImage(file = r"../resources/BananaIcon.png").subsample(6,6)
        self.btnScanBanana = \
          tk.Button(self.scanButtonsFrame,
          text = "Banana",
          font = "Calibri 20 bold",
          image=photoScanBanana,
          compound=tk.BOTTOM,
          bg="white", activebackground="white",
          bd=2,
          command = lambda: self.onBasketUpdated("B+1"))
        self.btnScanBanana.grid(row=1, column=0, sticky="news", pady=3)

        # The scan pear button
        photoScanPear = tk.PhotoImage(file = r"../resources/PearIcon.png").subsample(6,6)
        self.btnScanPear = \
          tk.Button(self.scanButtonsFrame,
          text = "Pear",
          font = "Calibri 20 bold",
          image=photoScanPear,
          compound=tk.BOTTOM,
          bg="white", activebackground="white",
          bd=2,
          command = lambda: self.onBasketUpdated("P+1"))
        self.btnScanPear.grid(row=2, column=0, sticky="news", pady=3)

        # frame for the list of the already scanned items
        self.scannedItemsFrame = tk.LabelFrame(self.shoppingFrame, width = 350, bg="white", padx=10, pady=5, bd=0, highlightthickness=0, highlightbackground="darkgrey")
        # frame has 5 rows, 3 for the 3 items, 1 empty and 1 for the total cost
        self.scannedItemsFrame.rowconfigure(0,weight=0)
        self.scannedItemsFrame.rowconfigure(1,weight=0)
        self.scannedItemsFrame.rowconfigure(2,weight=0)
        self.scannedItemsFrame.rowconfigure(3,weight=1)
        self.scannedItemsFrame.columnconfigure(0,weight=1)

        # frame is positioned on the right side of the bottom row of the parent
        self.scannedItemsFrame.grid(row=0,column=1, sticky="news", padx=10)
        self.scannedItemsFrame.grid_propagate(False)

        # the 3 items
        itemsCatalogue = self._checkout.getItemsCatalogue()
        self.labelApple = iteminfocard.ItemInfoCard(self.scannedItemsFrame, itemsCatalogue["A"], "customerPage")
        self.labelBanana = iteminfocard.ItemInfoCard(self.scannedItemsFrame, itemsCatalogue["B"], "customerPage")
        self.labelPear = iteminfocard.ItemInfoCard(self.scannedItemsFrame, itemsCatalogue["P"], "customerPage")
        self._checkout.register(self.labelApple)
        self._checkout.register(self.labelBanana)
        self._checkout.register(self.labelPear)

        # total and checkout
        self.basketAndCheckout = tk.LabelFrame(self.scannedItemsFrame, bg="white", bd=0, highlightthickness=0)
        self.basketAndCheckout.columnconfigure(0,weight=1)
        self.basketAndCheckout.columnconfigure(1,weight=0)
        self.basketAndCheckout.rowconfigure(0,weight=1)
        self.basketAndCheckout.grid(row=3, column=0, sticky = "ews", padx=0)

        self.labelTotalWidget = baskettotalwidget.BasketTotalWidget(self.basketAndCheckout)
        self.labelTotalWidget.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self._checkout.register(self.labelTotalWidget)

        self.btnCheckout = tk.Button(self.basketAndCheckout, text = "Checkout", font = "Calibri 20 bold",
          bg="#51990F", activebackground="#B6E119", bd=2,command = lambda: self._onCheckout())
        self.btnCheckout.grid(row=0, column=1, sticky="news", padx=5, pady=5)

        self._showTime()

        # Run the window
        self.root.mainloop()

    def getPageName(self):
        """Return 'customerPage'"""

        return "customerPage"

    def _staffLogin(self):
        """Load the staff login page"""

        self.staffLoginPopup = staffloginpopup.StaffLoginPopup(self)

    def openStorePage(self, username):
        """Open the staff page for the user with this username"""

        if (not isinstance(username, str)):
            raise TypeError
        self.storePage = staffpage.StaffPage(self, username)
        self.staffLoginPopup.after(400, self.staffLoginPopup.destroy)

    def _showTime(self):
        """Update the clock of the application every 1 second"""

        time_string = strftime("%A %d %B %Y    %H:%M:%S %p") # time format 
        self.labelTime.config(text=time_string, font = "Calibri 15", fg="white")
        self.labelTime.after(1000,self._showTime) # time delay of 1000 milliseconds 

    def getCheckout(self):
        """Get the internal engine that runs under the hood of this page"""

        return self._checkout

    def _onCheckout(self):
        """Action for when the user clicks the checkout button"""

        self.onBasketUpdated()

    def onBasketUpdated(self,listItemCodeAndaction="all", signalStrength = "strong"):
        """Add or remove 1 item from the basket or remove all of 1
        category or remove everything from the basket
        """

        if (not isinstance(listItemCodeAndaction, str)):
            raise TypeError
        if (not (len(listItemCodeAndaction) <= 3 and( listItemCodeAndaction=="all" or listItemCodeAndaction.endswith("-A") or not listItemCodeAndaction in self._checkout.getBasket().keys()))):
            raise ValueError
        if (not isinstance(signalStrength, str)):
            raise TypeError
        if (not signalStrength in ["weak", "strong"]):
            raise ValueError

        # Print price on terminal and remove all items from basket
        if (listItemCodeAndaction == "all"):
            ###################################################
            #
            # This block is added merely because this specific functionality was asked
            # to be implemented in this specific way.
            #
            tempItemCodeList = []
            # get the basket keys
            for itemCode in self._checkout.getBasket().keys():
                # Append the itemCode to the temporary list as many times
                # as there are items with itemCode in the basket
                for index in range(self._checkout.getBasket()[itemCode]):
                    tempItemCodeList.append(itemCode)

            # Create a temporary dictionary that only holds
            # item code and item price
            tempItemPricesDict = {}
            for itemCode in self._checkout.getItemsCatalogue().keys():
                tempItemPricesDict[itemCode]=self._checkout.getItemsCatalogue()[itemCode].getPrice()

            # call the function
            print("You paid {}p.".format(self._checkout.checkout(tempItemCodeList, tempItemPricesDict)))
            #
            # END OF BLOCK
            #
            ###################################################

            self._checkout.clearBasket()
            return
        # Remove all items that belong to a specific category
        elif (listItemCodeAndaction.endswith("-A")):
            for widget in self.scannedItemsFrame.grid_slaves():
              if (not isinstance(widget, iteminfocard.ItemInfoCard)):
                continue
              if (widget.getItemCode()==listItemCodeAndaction[0]):
                self._checkout.clearBasket(widget.getItemCode(), signalStrength)
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

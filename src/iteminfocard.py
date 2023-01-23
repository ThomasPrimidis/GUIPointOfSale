import tkinter as tk
import checkout
from item import Item
from checkout import Checkout


class ItemInfoCard(tk.Frame):
    """Widget that displays item name, icon, price, population,
    cost of population and savings if relevant.

    One widget per item category that shows item name, picture, price
    per unit, number of such items in the basket, total cost of items
    and total savings of due to multi-buy offers if relevant.
    """

    def __init__(self, parent, item, hostPage):
        tk.Frame.__init__(self, parent, bg = "white", highlightbackground="#F2F2F2", highlightthickness=5, padx=0, pady=0)
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        self.columnconfigure(0,weight=1)

        self._parent = parent
        self._item = item
        self._hostPage = hostPage

        if (not isinstance(item, Item)):
            raise TypeError
        if (not isinstance(hostPage, str)):
            raise TypeError
        if (not (hostPage == "customerPage" or hostPage == "storePage")):
            raise ValueError

        # Configure the top row of the card
        self.topRow = tk.Frame(self, bg="white")
        self.topRow.grid(row=0, column=0, sticky="news", padx=10)
        self.topRow.columnconfigure(0,weight=0)
        self.topRow.columnconfigure(1,weight=0)
        self.topRow.columnconfigure(2,weight=1)
        self.topRow.columnconfigure(3,weight=0)
        self.topRow.rowconfigure(0,weight=1)

        # Configure the bottom row of the card
        self.bottomRow = tk.Frame(self,bg="white")
        self.bottomRow.grid(row=1, column=0, sticky="news", padx=10)
        self.bottomRow.columnconfigure(0,weight=0)
        self.bottomRow.columnconfigure(1,weight=0)
        self.bottomRow.columnconfigure(2,weight=1)
        self.bottomRow.rowconfigure(0,weight=1)

        # Add item name on the left of the top row
        self.itemNameLabel = tk.Label(self.topRow, text=self._item.getName(), font = "Calibri 20 bold", bg="white", anchor="w")
        self.itemNameLabel.grid(row=0, column=0, sticky="news", padx=0, pady=0)

        # Add item individual price in the middle of the top row
        self.valuePerItemLabel = tk.Label(self.topRow, text = "{}p each".format(self._item.getPrice()), font = "Calibry 10", bg="white", anchor="sw")
        self.valuePerItemLabel.grid(row=0, column=1, sticky="news", padx=0, pady=0)

        # Add item population cost on the right of the top row
        self.itemTotalValue = tk.Label(self.topRow, bg="white", anchor="se")
        self.itemTotalValue.grid(row=0, column=2, sticky="news", padx=0, pady=0)

        # Add item image on the left of the bottom row
        self.itemImage = item.getImage().subsample(10,10)
        self.itemImageLabel = tk.Label(self.bottomRow, image = self.itemImage, bg="white", anchor="w")
        self.itemImageLabel.grid(row=0, column=0, sticky="w", padx=0, pady=0)
 
        # Add item population in the middle of the bottom row
        self.itemPopulationLabel = tk.Label(self.bottomRow, bg="white", anchor="w")
        self.itemPopulationLabel.grid(row=0, column=1, sticky="w", padx=0, pady=0)

        # Add item multibuy savings on the right of the bottom row
        self.savingsLabel = tk.Label(self.bottomRow, anchor="e")
        self.savingsLabel.grid(row=0, column=3, sticky="news", padx=0, pady=0)

    def slot(self, checkout, signalStrength="strong"):
        """Method triggered by the signal of the checkout class"""

        if (not isinstance(checkout, Checkout)):
            raise TypeError
        if (not isinstance(signalStrength, str)):
            raise TypeError
        if (not (signalStrength == "strong" or signalStrength == "weak")):
            raise ValueError

        self.itemPopulation = checkout.getNumberOfItems(self.getItemCode())
        # We want cards on the customer page to disappear if item count==0
        # Those in the store login page must follow the rules of the signals
        if (self._hostPage == "customerPage"):
            self._update()
        else:
            self._update(signalStrength=="strong")

    def getItemName(self):
        """Return the item's name"""
        return self._item.getName()

    def getItemCode(self):
        """Return the item's code"""
        return self._item.getCode()

    def _update(self, removeWhenEmpty = True):
        """Update the widget's position, visibility and data"""

        if (not isinstance(removeWhenEmpty, bool)):
            raise TypeError

        # Widget placement/removal in the GUI
        #------------------------------------
        # if the widget is mapped but number of items is zero, remove it unless forced to keep it
        if (self.winfo_ismapped() and self.itemPopulation==0 and removeWhenEmpty):
            self.grid_forget()
            return
        # if the widget is not mapped and number of items is not zero find the
        # first empty row in the parent frame starting from 0 and add it there
        elif (not self.winfo_ismapped() and self.itemPopulation>0):
            ncols, nrows = self._parent.grid_size()
            if (ncols>1):
                raise Exception("GUI is not configured correctly"+str(ncols))
            for irow in range(nrows):
                if (len(self._parent.grid_slaves(irow,0))==0):
                  self.grid(row=irow, column=0, sticky="news", padx=5, pady=5)
                  break # if this break is commented, newest category is added on the top

        # Widget data updates
        #--------------------
        self.itemPopulationLabel.config(text="x{}".format(self.itemPopulation), font = "Calibri 20 bold", anchor="w")
        itemMultibuyCost, itemMultibuySavings = self._item.getMultibuyCost(self.itemPopulation)
        self.itemTotalValue.config(text="{:5d}p".format(itemMultibuyCost), font = "Calibry 10 bold")
        if (itemMultibuySavings>0.):
            self.savingsLabel.config(text="{}{:15d}p".format(self._item.printOffer(),-itemMultibuySavings),bg="#C5E0B4")
        else:
            self.savingsLabel.config(text="",bg="white")
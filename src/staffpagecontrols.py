import tkinter as tk
import iteminfocard
from item import Item
from checkout import Checkout

class StaffPageControls(tk.Frame):
    """Widget offering advanced controls to basket per item category

    Widget is placed in the staff login page. It comprises an
    ItemInfoCard widget, buttons to add or remove 1 item and a button
    to remove all items.

    Attributes:
        parent (tkinter LabelFrame): Frame in the StaffPage instance in
            which to position this widget.
        item (Item instance): The item that this widget is dedicated to.
        population (int): How many of these Items are in the basket.

    Methods:
        slot(self, checkout, signalStrength="strong")
    """

    def __init__(self, parent, item):
        """Initialise the widget in its parent frame for this item"""
        tk.Frame.__init__(self, parent, bg = "white", bd=0, padx=10, pady=10)
        self.columnconfigure(0,weight=0)
        self.columnconfigure(1,weight=0)
        self.columnconfigure(2,weight=1)
        self.columnconfigure(3,weight=0) 
        self.rowconfigure(0,weight=1)

        if (not isinstance(item, Item)):
          raise TypeError

        self.parent = parent
        self.item = item

        self.buttonMinus = tk.PhotoImage(file = r"../resources/buttonMinus.png").subsample(3,3)
        self.btnDecreaseItemCount = tk.Button(self, image=self.buttonMinus, bg="white", command = lambda: self._updateItemCount(-1, "weak"))
        self.btnDecreaseItemCount.grid(row=0, column=0, sticky="news")

        self.buttonPlus = tk.PhotoImage(file = r"../resources/buttonPlus.png").subsample(3,3)
        self.btnIncreaseItemCount = tk.Button(self, image=self.buttonPlus, bg="white", command = lambda: self._updateItemCount(1, "weak"))
        self.btnIncreaseItemCount.grid(row=0, column=1, sticky="news")

        self.itemCardContainer = tk.LabelFrame(self, bg = "white", bd=0)
        self.itemCardContainer.grid(row=0, column=2, sticky="news", padx=0, pady=0)
        self.itemCardContainer.rowconfigure(0, weight=1)
        self.itemCardContainer.columnconfigure(0, weight=1)
        self.itemCard = iteminfocard.ItemInfoCard(self.itemCardContainer, self.item, "storePage")

        self.removeAllImage = tk.PhotoImage(file = r"../resources/buttonBin.png")
        self.btnRemoveAllItemsOfThisCategory = tk.Button(self, text = "Remove\nall", font = "Calibri 14 bold",
          image=self.removeAllImage, compound=tk.BOTTOM, bg="red", activebackground="orange", command = lambda: self._updateItemCount(-2, signalStrength = "weak"))
        self.btnRemoveAllItemsOfThisCategory.grid(row=0, column=3, sticky="news")

    def slot(self, checkout, signalStrength="strong"):
        """Method triggered by the signal of the checkout class"""
        if (not isinstance(checkout, Checkout)):
            raise TypeError
        if (not isinstance(signalStrength, str)):
            raise TypeError
        if (not signalStrength in ["weak", "strong"]):
            raise ValueError
        # Send signal to the ItemInfoCard of this widget to update its display. 
        self.itemCard.slot(checkout, signalStrength)

    def _updateItemCount(self, mode, signalStrength = "strong"):
        """Change the number of items of this category of products in the basket."""

        if (not isinstance(mode, int)):
            raise TypeError
        if (not isinstance(signalStrength, str)):
            raise TypeError
        if (not mode in [-2, -1, 0, 1]):
            raise ValueError

        # remove all items of this category
        if (mode == 0):
            basketUpdateCode="all"
        # remove all of a single category
        elif (mode==-2):
            basketUpdateCode=self.item.getCode()+"-A"
        # add or remove 1
        else:
            basketUpdateCode="{}+{:1d}".format(self.item.getCode(),mode) if mode>0 else "{}{:2d}".format(self.item.getCode(),mode)

        # update the staff page
        self.parent.master.onBasketUpdated(basketUpdateCode, signalStrength)

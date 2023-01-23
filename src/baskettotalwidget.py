import tkinter as tk
from checkout import Checkout

class BasketTotalWidget(tk.Frame):
    """ Widget used for dynamically showing the total basket cost

    Attributes:
      totalLabel (tkinter Label): Displays the word Total
      totalBalueLabel (tkinter Label): Displays basket price in pence
      savingsLabel (tkinter Label): Displays basket savings in pence

    Methods:
        slot(self, checkout, signalStrength="strong"):
        _getAll(self):
        _setAll(self, other):
        _update(self, checkout):
    """

    def __init__(self, parent):
        """Initialise the basket widget

        Parameters:
            parent (CustomerPage or StaffPage instance): The page on
                which this widget will be displayed.

        Methods:
            slot(self, signalStrength = "strong")
        """

        tk.Frame.__init__(self, parent, bg="white", highlightbackground="#F2F2F2", highlightthickness=5)
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=0)
        self.rowconfigure(2,weight=1)
        self.columnconfigure(0,weight=1)
        self.totalLabel = tk.Label(self, text="Total", bg="white", anchor=tk.NW, font="Calibri 30 bold")
        self.totalLabel.grid(row=0, column=0, sticky="news", padx=5, pady=5)
        self.totalValueLabel = tk.Label(self,text="0p", bg="white", anchor = tk.E, font="Calibri 45 bold")
        self.totalValueLabel.grid(row=2, column=0, sticky="news", padx=0, pady=0)
        self.savingsLabel = tk.Label(self, bg="white", anchor=tk.E, font="Calibri 20 bold", fg="#76B620")
        self.savingsLabel.grid(row=1, column=0, sticky="news", padx=0, pady=0)

    def slot(self, checkout, signalStrength="strong"):
        """Method triggered by the signal of the checkout class"""
        if (not isinstance(checkout, Checkout)):
            raise TypeError
        self._update(checkout)

    def _getAll(self):
        """Return tuple with all the labels on the widget"""
        return self.totalLabel.cget("text"), self.totalValueLabel.cget("text"), self.savingsLabel.cget("text"), 

    def _setAll(self, other):
        """Shallow copy the displayed values of other widget to this widget"""
        if (not isinstance(other, BasketTotalWidget)):
            raise TypeError

        title, total, savings  = other._getAll()
        self.totalLabel.config(text = title)
        self.totalValueLabel.config(text = total)
        self.savingsLabel.config(text = savings)

    def _update(self, checkout):
        """Update the widget"""
        if (not isinstance(checkout, Checkout)):
            raise TypeError
        total, savings = checkout.total()
        self.totalValueLabel.config(text="{}p".format(total))
        if (savings>0.):
            self.savingsLabel.config(text="You saved {}p".format(savings))
        else:
            self.savingsLabel.config(text="")
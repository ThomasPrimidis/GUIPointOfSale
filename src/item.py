import tkinter as tk

class Item():
    """Class of items that can be bought from the supermarket.

    Items that can be bought from the supermarket have a name, a code
    with which they are identified within the application, an image
    of them, a price and an optional multibuy offer. Multibuy offers
    can either be for a specific price (e.g. 3 items for 100 pence) or
    for a subset of bought items (e.g. 3 items for the price of 2).

    Class attributes:
        dictItemNamePerCode (dict): Dictionary with item codes as keys
            and lists of 4 integers as values. List members are in
            order: price, multiBuyMinimumPopulation, offerOnPopulation,
            offerOnPrice.

        dictItemImagePath (dict): Dictionary with item codes as keys
            and strings of paths to items' pictures as values. One
            picture per item and one path per picture.

    Instance attributes:
        code (str): 1-character alphabetic code.

        price (int): the price per item of this item in pence.

        multibuyMinimumPopulation (int): the size of the group of
            items on which a multi-buy offer may apply. For example
            offers are given to groups of 3 items.

        offerOnPopulation (int): how many items should be charged
            from the group of 'multibuyMinimumPopulation' items. For
            example, 3 for the price of 2.

        offerOnPrice (int): how much in pence should the group of
        'multibuyMinimumPopulation' items be charged. For example 3 for
        100 pence.

    Methods:
        __init__

        getName(self)

        getCode(self)

        getPrice(self)

        getImage(self)

        printOffer(self)

        getMultibuyCost(self, groupSize)
    """

    # Class-wide definition of the relationship between item code and item name
    dictItemNamePerCode = {"A": "Apple",
                           "B": "Banana",
                           "P": "Pear"}

    # Class-wide definition of the relationship between item code and item icon
    dictItemImagePath = {"A": "../resources/AppleIcon.png",
                         "B": "../resources/BananaIcon.png",
                         "P": "../resources/PearIcon.png"}

    def __init__(self, code, price, multibuyMinimumPopulation, offerOnPopulation, offerOnPrice):
        """ Initialise an item with a code, price and multibuy offer
        details.

        Multi-buy offers can be either on item population (e.g. get 3
        for the price of 2) or on fixed price (e.g. get 3 for 100
        pence). Offers are applied to all unique groups of items (e.g.
        if offer is for 3 items then buying 7 will result in an offer
        for the first 3 and an offer for the second 3 with the seventh
        item charged at full price).

        Parameters:
            code (str): Alphabet letter used as identification code.

            price (int): Cost of single item in pence.

            multibuyMinimumPopulation (int): The group of items on
                which any relevant offers can be applied (e.g. offer
                for 3 bananas).

            offerOnPopulation (int): The number of items in an offer-
                worthy group of items that should be charged (e.g.
                offer: get 3 bananas for the price of 2).

            offerOnPrice (int): The price in pence to be charged for
                an offer-worthy group of items (e.g. 3 bananas for 100
                pence).
        """

        # Raise relevant exceptions before initialisation
        if (not isinstance(code,str)):
            raise TypeError
        if (not isinstance(price, int)):
            raise TypeError
        if (not isinstance(multibuyMinimumPopulation, int)):
            raise TypeError
        if (not isinstance(offerOnPopulation, int)):
            raise TypeError
        if (not isinstance(offerOnPrice, int)):
            raise TypeError
        if (not code in Item.dictItemNamePerCode.keys()):
           raise ValueError
        if (price <= 0 ):
            raise ValueError
        if (multibuyMinimumPopulation <= 0):
            raise ValueError
        if (offerOnPopulation < 0):
            raise ValueError
        if (offerOnPrice < 0):
            raise ValueError
        if (offerOnPopulation != 0 and offerOnPrice != 0):
            raise ValueError

        # initialise if no exceptions were raised
        self._code = code
        self._price = price
        self._multibuyMinimumPopulation = multibuyMinimumPopulation
        self._offerOnPopulation = offerOnPopulation
        self._offerOnPrice = offerOnPrice

    def getName(self):
        """Return the name of the item as a string."""

        return Item.dictItemNamePerCode[self.getCode()]

    def getCode(self):
        """Return the 1-character alphabetic code of the item as a
        string.
        """

        return self._code

    def getPrice(self):
        """Return the price in pence of the item as an int."""

        return self._price

    def getImage(self):
        """Return the photograph of the item as a tkinter PhotoImage."""

        return tk.PhotoImage(file = Item.dictItemImagePath[self._code])

    def printOffer(self):
        """Return a string describing the multibuy offer of the item."""

        if (self._offerOnPopulation>1):
            return "Get {:d} for the price of {:d}".format(self._multibuyMinimumPopulation, self._offerOnPopulation)
        else:
            return "Get {:d} for {:3d}p".format(self._multibuyMinimumPopulation, self._offerOnPrice)

    # Return the price in pence of groups of the same item applying relevant multibuy offers
    def getMultibuyCost(self,groupSize):
        """Return (total cost, multi-buy offer savings) in pence of
        an item group of size groupSize as an (int, int) tuple.

        Parameters:
            groupSize (int): the number of items for which to calculate
            total cost and an relevant multi-buy offer savings.
        """

        # Raise exceptions before calculation
        if (not isinstance(groupSize, int)):
            raise TypeError
        if (groupSize<0):
           raise ValueError

        # Calculate if no exceptions were raised
        if (self._multibuyMinimumPopulation>1):
            numberOfItemGroupsOnOffer = groupSize // self._multibuyMinimumPopulation
            numberOfItemsOutsideOffer = groupSize % self._multibuyMinimumPopulation
            costFromOffer = (self._offerOnPrice + self._price * self._offerOnPopulation) * numberOfItemGroupsOnOffer
            costOutsideOffer = numberOfItemsOutsideOffer * self._price
        else:
            costFromOffer = 0
            costOutsideOffer = groupSize*self._price

        # calculate total cost and total savings for bulk purchase of the item
        totalCost = costFromOffer + costOutsideOffer
        savings = groupSize*self._price - totalCost
        return totalCost, savings
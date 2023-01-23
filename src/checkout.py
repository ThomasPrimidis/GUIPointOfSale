import item
import copy

class Checkout():
    """The main engine that calculates data and updates the GUI.

    The main engine is responsible for calculating total cost, applying
    offers, controlling the basket and signaling to the graphical user
    interface about any changes in the basket. Members of the GUI are
    listed as listeners to the signaling mechanism of the class to that
    they can be triggered by the signal and read information from it.

    Attributes:
        _basket (dict): dictionary with item codes as keys and with
            number of items scanned as values.
        _itemsCatalogue (dict): dictionary with item codes as keys and
            with lists of item price and multi-buy details as values.

    Methods:
        copyTo(self, other)

        register(self,listener)

        unregister(self,listener)

        signal(self, signalStrength = "strong")

        _initItemsCatalogue(self,dictItemsAndPrices)

        initBasket(self)

        getItemsCatalogue(self)

        getBasket(self)

        getItemCategoriesInBasket(self)

        getNumberOfItems(self,itemCode="")

        scan(self,itemCode, signalStrength = "strong")

        unscan(self,itemCode, signalStrength = "strong")

        clearBasket(self, itemCode="all", signalStrength = "strong")

        total(self, item="all")
    """

    def __init__(self, orig=None, itemsAndPrices = {"A": [25, 3, 2, 0], "B": [40, 3, 0, 100], "P": [30, 1, 0, 0]}):
        """Initialise the core application engine with an empty basket.

        Parameters:
            orig (None or Checkout instance): Dictates whether this
                class instance will be instanciated from scratch or
                it will be an independent copy of another instance.

            itemsAndPrices (dict): Dictionary with the supermarket
                items catalogue. Keys are the item codes and values
                are lists of item price and multi-buy details.
        """

        # Raise exceptions before initialisation
        if (not (orig is None or isinstance(orig, Checkout))):
            raise TypeError 
        if (not isinstance(itemsAndPrices, dict)):
            raise TypeError
        if (not bool(itemsAndPrices)):
            raise ValueError
        
        for itemCode in itemsAndPrices.keys():
            if (not isinstance(itemCode, str)):
                raise TypeError
            elif (len(itemCode)>1):
                raise ValueError
            elif (not isinstance(itemsAndPrices[itemCode],list)):
                raise TypeError
            elif (len(itemsAndPrices[itemCode])!=4):
                raise ValueError
            elif (not itemCode in "ABP"):
                raise ValueError
        
            for number in itemsAndPrices[itemCode]:
                if (not isinstance(number, int)):
                    raise TypeError
        
            if (itemsAndPrices[itemCode][0] <= 0):
                raise ValueError        
            if (itemsAndPrices[itemCode][1] <= 0):
                raise ValueError
            if (itemsAndPrices[itemCode][2] < 0):
                raise ValueError
            if (itemsAndPrices[itemCode][3] < 0):
                raise ValueError
            if (itemsAndPrices[itemCode][2] != 0 and itemsAndPrices[itemCode][3] != 0):
                raise ValueError
        
        # Default constructor
        if (orig is None):
            self._basket = {}
            self._itemsCatalogue = {}
            self._initItemsCatalogue(itemsAndPrices)
            self.initBasket()
        # copy constructor
        else:
            self._basket = copy.copy(orig._basket)
            self._itemsCatalogue = copy.copy(orig._itemsCatalogue)
        
        # Instances must start with an empty list of listeners
        # regardless of the constructor used to build them
        self.listeners = set()

    def copyTo(self, other):
        """Copy the contents of this basket to the other basket and
        trigger the signals of the other basket to apply its changes
        to its related graphical user interface.
        """

        if (not isinstance(other, Checkout)):
            raise TypeError

        other._basket = copy.copy(self._basket)
        other._itemsCatalogue = copy.copy(self._itemsCatalogue)
        other.signal()

    def register(self,listener):
        """Add listener to listeners list"""

        if (listener is None):
            raise TypeError
        self.listeners.add(listener)

    def unregister(self,listener):
        """Remove listener from listeners list"""

        if (listener is None):
            raise TypeError
        self.listeners.discard(listener)

    def signal(self, signalStrength = "strong"):
        """Send a signal to all listeners"""

        if (not isinstance(signalStrength, str)):
            raise TypeError
        if (not signalStrength in ["weak", "strong"]):
            raise ValueError
        for listener in self.listeners:
            listener.slot(self, signalStrength)

    def _initItemsCatalogue(self,dictItemsAndPrices):
        """Initialise the catalogue of items sold at the supermarket
        and their prices
        """

        if (not isinstance(dictItemsAndPrices, dict)):
            raise TypeError

        for itemCode in dictItemsAndPrices:
            # item price
            itmPrice = dictItemsAndPrices[itemCode][0]
            # item minimum multibuy population
            itmMinMBP = dictItemsAndPrices[itemCode][1]
            # item offer on population
            itmOfferPop = dictItemsAndPrices[itemCode][2]
            # item offer on price
            itmOfferPrc = dictItemsAndPrices[itemCode][3]
            # init the item and append to the item catalogue
            self._itemsCatalogue[itemCode] = item.Item(itemCode,
                                                       itmPrice,
                                                       itmMinMBP,
                                                       itmOfferPop,
                                                       itmOfferPrc)


    def initBasket(self):
        """Initialise an empty basket"""

        for itemCode in self._itemsCatalogue:
            self._basket[itemCode] = 0
    

    def getItemsCatalogue(self):
        """Get the catalogue of items sold at the supermarket"""

        return self._itemsCatalogue


    def getBasket(self):
        """Get the basket"""

        return self._basket


    def getItemCategoriesInBasket(self):
        """Return a list of the item categories in the basket"""

        scannedItemsList=[]    
        for category in self._basket:
          if (self._basket[category]>0):
            scannedItemsList.append(category)
        return scannedItemsList


    def getNumberOfItems(self,itemCode=""):
        """return the number of items of a specific category or the total number of items in the basket"""

        if (not isinstance(itemCode, str)):
            raise TypeError
        if (itemCode==""):
            n = 0
            for itemCode in self._basket:
                n+=self._basket[itemCode]
            return n
        else:
            if (not itemCode in self._itemsCatalogue.keys()):
                raise ValueError
            return self._basket[itemCode]


    def scan(self,itemCode, signalStrength = "strong"):
        """Add an item to the basket"""

        if (not isinstance(itemCode, str)):
            raise TypeError
        if (not isinstance(signalStrength, str)):
            raise TypeError
        if (not itemCode in self._itemsCatalogue.keys()):
            raise ValueError
        if (not signalStrength in ["weak", "strong"]):
            raise ValueError
        self._basket[itemCode]+=1
        self.signal(signalStrength)


    def unscan(self,itemCode, signalStrength = "strong"):
        """Remove an item from the basket"""
        if (not isinstance(itemCode, str)):
            raise TypeError
        if (not isinstance(signalStrength, str)):
            raise TypeError
        if (not itemCode in self._itemsCatalogue.keys()):
            raise ValueError
        if (not signalStrength in ["weak", "strong"]):
            raise ValueError

        if (self._basket[itemCode]>0):
            self._basket[itemCode]-=1
            self.signal(signalStrength)

        if (self._basket[itemCode] <= 0):
            raise ValueError


    def clearBasket(self, itemCode="all", signalStrength = "strong"):
        """Remove all items from the basket"""

        if (not isinstance(itemCode, str)):
            raise TypeError
        if (not isinstance(signalStrength, str)):
            raise TypeError
        if (itemCode!="all" and not itemCode in self._itemsCatalogue.keys()):
            raise ValueError
        if (not signalStrength in ["weak", "strong"]):
            raise ValueError

        if (itemCode == "all"):
            for i_itemCode in self._basket:
                self._basket[i_itemCode] = 0
        else:
            self._basket[itemCode] = 0
        self.signal(signalStrength)


    def checkout(self, listOfItems, itemsCatalogue):
        """Takes a list of item codes and their current prices and returns
        the total price in pence, after applying any relevant offers.

        Parameters:
            listOfItems (list): List of item codes
            itemsCatalogue (dict): Dictionary with the supermarket
                items catalogue. Keys are the item codes and values
                are lists of item price and multi-buy details.
        """

        if (not isinstance(listOfItems, list)):
            raise TypeError

        if (not isinstance(itemsCatalogue, dict)):
            raise TypeError

        for itemCode in listOfItems:
            if (not isinstance(itemCode, str)):
                raise TypeError
            if (not itemCode in self.getItemsCatalogue().keys()):
                raise ValueError

        for itemCode in itemsCatalogue.keys():
            if (not itemCode in self.getItemsCatalogue().keys()):
                raise ValueError
            if (not isinstance(itemsCatalogue[itemCode], int)):
                raise TypeError
            if (itemsCatalogue[itemCode] <= 0):
                raise ValueError
            if (itemsCatalogue[itemCode] != self.getItemsCatalogue()[itemCode].getPrice()):
                raise ValueError

        # We can apply the same elegant calculation used in self.total(self, item)
        # so we must create a temporary basket from the list and pass it
        tempBasket = {"A": 0, "B": 0, "P": 0}
        for itemCode in listOfItems:
            tempBasket[itemCode]+=1

        totalCost = 0
        for itemCode in tempBasket:
            _totalCost, _ =self._itemsCatalogue[itemCode].getMultibuyCost(tempBasket[itemCode])
            totalCost+=_totalCost

        return totalCost


    def total(self, item="all"):
        """
        Returns the total cost and the savings after applying any
        relevant offers on individual item categories or the whole basket
        :param item: the item on which to calculate the cost and the savings
        :returns: tuple of 2 integers
        :raises Nothing
        """

        if (not isinstance(item, str)):
            raise TypeError

        for itemCode in self._basket:
            if (not (item=="all" or itemCode==item)):
                raise ValueError

        totalCost=0
        savings=0
        for itemCode in self._basket:
            if (item=="all" or itemCode==item):
                _totalCost, _savings =self._itemsCatalogue[itemCode].getMultibuyCost(self._basket[itemCode])
                totalCost+=_totalCost
                savings+=_savings
            
        return totalCost, savings

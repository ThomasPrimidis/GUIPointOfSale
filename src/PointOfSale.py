"""This is a point of sale application with a graphica user interface.

It allows the user to add items to their basket by clicking on the
relevant item button on the screen. Users finish their shopping by
clicking the checkout button. A list of scanned items is shown to the
user in real time as well as the total cost of the basket after any
multi-buy offers have been applied.

The application allows advanced controls on the basket via a store
page that needs staff credentials to open. In that page, staff can
remove items from the basket and either confirm the changes or return
to the main page without affecting the basket.
"""

import customerpage

def Main():
 guiApplication = customerpage.CustomerPage()

if __name__ == "__main__":
  Main()
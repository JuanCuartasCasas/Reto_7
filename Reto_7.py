"""
Reto 3: Restaurant Order System
The code presents a sample of a system to take orders and calculate
payments in a restaurant.
"""

from typing import List  # Adds List Type annotation
from queue import Queue
import time


class MenuItem:
    def __init__(self, name: str, price: float):
        self.name = name
        self._price = price
        self._stock = 10  # Assuming each item has a stock of 10 for simplicity
        self.style = "Regular"

    def get_stock(self):
        return self._stock

    def set_stock(self, new_stock: int):
        if new_stock < 0:
            raise ValueError("Stock cannot be negative.")
        self._stock = new_stock

    def get_price(self):
        return self._price

    def set_price(self, new_price: float):
        if new_price < 0:
            raise ValueError("Price cannot be negative.")
        self._price = new_price

    def remove_stock(self, quantity: int):
        if quantity > self.get_stock():
            raise ValueError(
                f"Not enough stock for {self.name}. Available: {self.get_stock()}"
            )
        self.set_stock(self.get_stock() - quantity)


class Order:
    def __init__(self):
        self.menu_items = []

    def add_item(self, menu_item: MenuItem):
        self.menu_items.append(menu_item)

    def calculate_total(self):
        total = sum(item.get_price() for item in self.menu_items)
        return total

    """it was determined that the customer is eligible for a discount of 10% on the total order
    taking to account the total amount, and the types of items ordered."""

    def apply_discount(self):
        if any(isinstance(item, Appetizer) for item in self.menu_items) and any(
            isinstance(item, Dessert) for item in self.menu_items
        ):
            # discount if the order includes 2 maincourses
            if sum(isinstance(item, MainCourse) for item in self.menu_items) >= 2:
                return self.calculate_total() * 0.15
            return self.calculate_total() * 0.10
        return 0  # No discount if conditions are not met


class Restaurant:
    def __init__(self, name: str = "Polleria la 22", location: str = "123 Main St"):
        self.location = location
        self.name = name
        self.menu: List[MenuItem] = []

    def take_order(self, order: Order):
        print(f"Welcome to {self.name}! Here is our menu:")

        for i, item in enumerate(self.menu):
            print(
                f"{i + 1}. {item.name} - ${item.get_price():.2f}\n{'=' * len(item.name) + '=' * 11}"
            )
        print("0. Done\n")
        while True:
            choice = input(
                "Please enter the number of the item you want to order (or 'done' to finish): "
            )
            if choice == "0" or choice.lower() == "done":
                print("Thank you for your order!")
                break
            try:
                int_choice = int(choice)

            except ValueError:
                print(
                    "Invalid input. Please enter a number corresponding to the menu item or 'done' to finish."
                )
                continue

            if int_choice > len(self.menu) or int_choice < 1:
                print("Invalid choice. Please try again.")
                continue

            try:
                order.add_item(self.menu[int_choice - 1])
                # stock reduction
                self.menu[int_choice - 1].remove_stock(1)
                print(f"Added {self.menu[int_choice - 1].name} to your order.")
                print(f"Current total: ${order.calculate_total():.2f}")
            except ValueError as e:
                print(f"Error: {e}")

    def calculate_payment(self, order: Order):
        total = order.calculate_total()
        discount = order.apply_discount()
        final_amount = total - discount
        return final_amount

    def add_menu_items(self, menu_items: List[MenuItem]):
        for i in menu_items:
            self.menu.append(i)


class MainCourse(MenuItem):
    def __init__(self, name: str, price: float):
        super().__init__(name, price)
        self.style = "Main Course"
        self.stock = 20
        self.description = "A delicious main course to satisfy your hunger,\
        based on 100 g of protein mixed with 200 g of vegetables and a side \
        rice or potatoes."


class Dessert(MenuItem):
    def __init__(self, name: str, price: float):
        super().__init__(name, price)
        self.style = "Dessert"
        self.stock = 15
        self.description = "A sweet treat to end your meal,\
        made with high-quality ingredients and a touch of creativity."


class Beverage(MenuItem):
    def __init__(self, name: str, price: float):
        super().__init__(name, price)
        self.style = "Beverage"
        self.stock = 30
        self.description = "A refreshing drink to complement your meal,\
        available in a variety of flavors and options."


class Appetizer(MenuItem):
    def __init__(self, name: str, price: float):
        super().__init__(name, price)
        self.style = "Appetizer"
        self.stock = 25
        self.description = "A delicious starter to whet your appetite,\
        made with fresh ingredients and bold flavors."


class Payment:
    def __init__(self):
        pass

    def pay(self,*args):
        raise NotImplementedError("It must have a specific payment method implemented.")


class cash_payment(Payment):
    def __init__(self, amount: float):
        super().__init__()
        self.amount = amount

    def pay(self, amount_to_pay: float) -> None:
        if self.amount < amount_to_pay:
            raise ValueError(
                f"Insufficient cash. Amount provided: ${self.amount:.2f}, amount to pay: ${amount_to_pay:.2f}"
            )
        else:
            print(f"Payment successful. Change: ${self.amount - amount_to_pay:.2f}")


class card_payment(Payment):
    def __init__(self, number: str, cvv: str, expiration_date: str, amount: float):
        super().__init__()
        self.number = number
        self.cvv = cvv
        self.expiration_date = expiration_date
        self.amount = amount

    def pay(self, amount_to_pay: float):
        if self.amount < amount_to_pay:
            raise ValueError(
                f"Insufficient funds on card. Amount available: ${self.amount:.2f}, amount to pay: ${amount_to_pay:.2f}"
            )

        print(
            f"Payment of ${amount_to_pay:.2f} successful with card ending in {self.number[-4:]}."
        )


def create_menu():
    # Appetizer
    churros = Appetizer("churros", 5.99)
    empanadas = Appetizer("empanadas", 4.99)
    ceviche = Appetizer("ceviche", 6.99)

    # Main Course
    carne_asada = MainCourse("carne asada", 15.99)
    pollo_a_la_parrilla = MainCourse("pollo a la parrilla", 12.99)
    pescado_frito = MainCourse("pescado frito", 14.99)

    # Dessert
    merengon = Dessert("merengon", 6.99)
    tres_leches = Dessert("tres leches", 7.99)

    # Beverage
    limonada = Beverage("limonada", 2.99)
    jugo_de_naranja = Beverage("jugo de naranja", 3.99)
    agua = Beverage("agua", 1.99)

    menu = [
        churros,
        empanadas,
        ceviche,
        carne_asada,
        pollo_a_la_parrilla,
        pescado_frito,
        merengon,
        tres_leches,
        limonada,
        jugo_de_naranja,
        agua,
    ]

    return menu


def pay():

    payment = input("Please select a payment method (cash/card): ").lower()

    if payment == "cash":
        amount = float(input("Enter the amount of cash provided: "))
        payment = cash_payment(amount)

    elif payment == "card":
        number = input("Enter card number: ")
        cvv = input("Enter CVV: ")
        expiration_date = input("Enter expiration date (MM/YY): ")
        amount = float(input("Enter the amount available on the card: "))
        payment = card_payment(number, cvv, expiration_date, amount)

    else :
        raise TypeError("Please select the cash or card payment method")
    return payment


def main():
    restaurant = Restaurant()
    menu = create_menu()

    restaurant.add_menu_items(menu)
    flag = True

    while flag:    
        try:
            orders_number = int(input("Please Select how many Orders you`d like to have"))
            flag = False
        except ValueError:
            print("The amount of orders must be a number, try again")
    
    order_line = Queue(maxsize= orders_number)

    for i in range(0,orders_number):
        print(f'\n{"=" * 10} \n{i} Order Number {i+1}\n{"=" * 10}')
        
        order = Order()
        restaurant.take_order(order)
        order_line.put(order)
    
    print("Assigning orders....")
    time.sleep(2)
    print("Estimating prices")
    counter = 1
    while not order_line.empty():
        order_head = order_line.get()
        
        if not order_head.menu_items:  # Si la orden está vacía
            print(f"Order {counter}: Empty order, skipping payment.\n")
            counter += 1
            continue
        
        print(f"Order Numer {counter}: \n")
        total_payment = restaurant.calculate_payment(order_head)
        print(f"Total payment after discount: ${total_payment:.2f}")

        payment_method = pay()
        try:
            payment_method.pay(total_payment)
        except ValueError as e:
            print(f"Payment error: {e}")

        counter += 1

    print("Thank you for visit our restaurant!")


if __name__ == "__main__":
    main()
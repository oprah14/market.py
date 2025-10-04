class Product:
    def __init__(self, name, wholesale_price, sell_price, stock=0):
        self.name = name
        self.wholesale_price = wholesale_price
        self.sell_price = sell_price
        self.stock = stock


class MarketOwner:
    def __init__(self):
        self.balance = 5000.0
        self.products = {}
        self.profit_margin = 0.2

    def show_products(self):
        print("\n--- Market Products ---")
        if not self.products:
            print("No products available.")
        else:
            for name, p in self.products.items():
                print(f"{name}: {p.stock} units | Sell price: {p.sell_price:.2f} $")

    def buy_from_wholesaler(self):
        print(f"\n Current Market Balance: {self.balance:.2f} $")
        print("--- Buy from Wholesaler ---")
        name = input("Enter product name: ")
        try:
            wholesale_price = float(input("Enter wholesale price: "))
            amount = int(input("Enter quantity to buy: "))
        except ValueError:
            print("Invalid input.")
            return

        total_cost = wholesale_price * amount
        self.balance -= total_cost
        sell_price = wholesale_price * (1 + self.profit_margin)

        if name in self.products:
            self.products[name].stock += amount
        else:
            self.products[name] = Product(name, wholesale_price, sell_price, amount)

        print(f" Bought {amount} of {name} for {total_cost:.2f} $.")
        print(f"New Market Balance: {self.balance:.2f} $")

    def set_profit_margin(self):
        try:
            new_margin = float(input("Enter new profit margin (e.g. 0.25 for 25%): "))
            self.profit_margin = new_margin
            for p in self.products.values():
                p.sell_price = p.wholesale_price * (1 + new_margin)
            print(f"Profit margin updated to {self.profit_margin*100:.0f}%.")
        except ValueError:
            print("Invalid input.")


class Customer:
    def __init__(self, market):
        self.balance = 1000.0
        self.cart = {}
        self.market = market

    def add_to_cart(self):
        product_name = input("Enter product name: ")
        if product_name not in self.market.products:
            print("Product not found.")
            return

        product = self.market.products[product_name]
        if product.stock <= 0:
            print("Out of stock.")
            return

        try:
            qty = int(input("Enter quantity: "))
        except ValueError:
            print("Invalid input.")
            return

        total_cost = qty * product.sell_price
        if total_cost > self.balance:
            print(" Credit limit reached! Not enough balance.")
            return

        if qty > product.stock:
            print(f"Only {product.stock} units available.")
            return

        product.stock -= qty
        self.balance -= total_cost
        self.market.balance += total_cost
        self.cart[product_name] = self.cart.get(product_name, 0) + qty

        print(f" Added {qty} x {product_name} for {total_cost:.2f} $.")
        print(f" Your Balance: {self.balance:.2f} $ |  Market Balance: {self.market.balance:.2f} $")

    def checkout(self):
        print("\n--- Checkout ---")
        if not self.cart:
            print("Cart is empty.")
            return
        total_spent = 0
        print(" Items in cart:")
        for item, qty in self.cart.items():
            price = self.market.products[item].sell_price
            cost = price * qty
            total_spent += cost
            print(f"- {item} x{qty} = {cost:.2f} $")
        print(f"\nTotal spent: {total_spent:.2f} $")
        print(f"Remaining balance: {self.balance:.2f} $")
        print(" Payment completed. Thank you for shopping!")


def main():
    market_owner = MarketOwner()
    print("=== Welcome to the Market Simulation ===")

    while True:
        print("\n====================================")
        print("Select your role:")
        print("1. Market Owner")
        print("2. Customer")
        print("3. Exit")
        print("====================================")        
        role = input("Choose: ")

        if role == "1":
            while True:
                print("\n=== Market Owner Menu ===")
                print(f" Market Balance: {market_owner.balance:.2f} $")
                print("-------------------------")
                print("1. Buy from wholesaler")
                print("2. Set profit margin")
                print("3. View products")
                print("4. Back to main menu")
                choice = input("Choose: ")

                if choice == "1":
                    market_owner.buy_from_wholesaler()
                elif choice == "2":
                    market_owner.set_profit_margin()
                elif choice == "3":
                    market_owner.show_products()
                elif choice == "4":
                    break
                else:
                    print("Invalid choice.")

        elif role == "2":
            customer = Customer(market_owner)
            while True:
                print("\n=== Shopping Menu ===")
                print(f" Customer Balance: {customer.balance:.2f} $")                
                print("-------------------------")
                print("1. View products")
                print("2. Add to cart")
                print("3. Checkout")
                print("4. Exit")
                choice = input("Choose: ")

                if choice == "1":
                    market_owner.show_products()
                elif choice == "2":
                    customer.add_to_cart()
                elif choice == "3":
                    customer.checkout()
                    break
                elif choice == "4":
                    break
                else:
                    print("Invalid choice.")

        elif role == "3":
            print("Exiting program...")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()

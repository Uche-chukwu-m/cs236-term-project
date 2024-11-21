import queue
import csv
from datetime import datetime

class EventTicketingSystem:
    def __init__(self, vip_tickets=5, regular_tickets=5):
        self.vip_queue = queue.Queue()
        self.regular_queue = queue.Queue()
        self.vip_tickets = vip_tickets
        self.regular_tickets = regular_tickets
        self.transaction_log = 'ticket_transactions.csv'

        # Initialize transaction log
        with open(self.transaction_log, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Timestamp', 'Name', 'Ticket Type', 'Status'])

    def register_ticket(self, name, ticket_type, number):
        tickets = {"V":"VIP", "R":"Regular"}
        if not name:
            print("Name cannot be empty!")
            return False

        if ticket_type == 'V' and self.vip_tickets > 0:
            if number > self.vip_tickets:
                print(f"Number of tickets exceeds available VIP tickets. There are {self.vip_tickets} tickets available.")
                return False
            for i in range(number):
                self.vip_queue.put(name)
                self._log_transaction(name, 'VIP', 'Pending')
                print(f"{name} is in the VIP queue. Current position: {1000+self.vip_queue.qsize()}.")
            return True
        elif ticket_type == 'R' and self.regular_tickets > 0:
            if number > self.regular_tickets:
                print(f"Number of tickets exceeds available Regular tickets. There are {self.regular_tickets} tickets available.")
                return False
            for i in range(number):
                self.regular_queue.put(name)
                self._log_transaction(name, 'Regular', 'Pending')
                print(f"{name} is in the Regular queue. Current position: {1000+self.regular_queue.qsize()}.")
            return True
        status = "Sold Out" if ticket_type in tickets else "Invalid Type"
        self._log_transaction(name, tickets[ticket_type], status)
        print(f"Sorry, no tickets available for the selected type or invalid ticket type.")
        return False



    def process_tickets(self):
        processed_tickets = []

        # Process VIP tickets first
        while not self.vip_queue.empty() and self.vip_tickets > 0:
            name = self.vip_queue.get()
            self.vip_tickets -= 1
            self._log_transaction(name, 'VIP', 'Confirmed')
            processed_tickets.append((name, 'VIP'))

        # Then process regular tickets
        while not self.regular_queue.empty() and self.regular_tickets > 0:
            name = self.regular_queue.get()
            self.regular_tickets -= 1
            self._log_transaction(name, 'Regular', 'Confirmed')
            processed_tickets.append((name, 'Regular'))

        return processed_tickets

    def cancel_ticket(self, name, ticket_type, number):
        tickets = {"V":"VIP", "R":"Regular"}
        ticket_type = ticket_type.strip().title()
        cancelled = False

        if ticket_type == 'V':
            for i in range(number):
                cancelled = self._remove_from_queue(self.vip_queue, name)
                if cancelled:
                    self._log_transaction(name, 'VIP', 'Cancelled')
                    print(f"{name}'s VIP ticket has been cancelled.")
                    self.vip_tickets += 1
        elif ticket_type == 'R':
            for i in range(number):
                cancelled = self._remove_from_queue(self.regular_queue, name)
                if cancelled:
                    self._log_transaction(name, 'Regular', 'Cancelled')
                    print(f"{name}'s Regular ticket has been cancelled.")
                    self.regular_tickets += 1
        print(f"Ticket for {name} ({tickets[ticket_type]}) was not found.")
        return False

    def _remove_from_queue(self, q, name):
        temp_queue = queue.Queue()
        found = False

        while not q.empty():
            current = q.get()
            if current == name and not found:
                found = True
            else:
                temp_queue.put(current)

        while not temp_queue.empty():
            q.put(temp_queue.get())

        return found

    def _log_transaction(self, name, ticket_type, status):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.transaction_log, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, name, ticket_type, status])

    def get_ticket_availability(self):
        return {
            'VIP': self.vip_tickets,
            'Regular': self.regular_tickets
        }

    def get_ticket_summary(self):
        total_tickets = 5 + 5  # Initial total tickets
        sold_tickets = (5 - self.vip_tickets) + (5 - self.regular_tickets)

        with open(self.transaction_log, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            transactions = list(reader)

        vip_sold = sum(1 for t in transactions if t[2] == 'VIP' and t[3] == 'Confirmed')
        regular_sold = sum(1 for t in transactions if t[2] == 'Regular' and t[3] == 'Confirmed')

        return {
            'Total Tickets': total_tickets,
            'Tickets Sold': sold_tickets,
            'VIP Tickets Sold': vip_sold,
            'Regular Tickets Sold': regular_sold,
            'VIP Tickets Remaining': self.vip_tickets,
            'Regular Tickets Remaining': self.regular_tickets
        }

def main():
    ticketing_system = EventTicketingSystem()

    while True:
        print("\n--- Event Ticketing System ---")
        print("1. Register for a Ticket")
        print("2. Check Ticket Availability")
        print("3. Process Ticket Requests")
        print("4. Cancel Ticket")
        print("5. View Sales Summary")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            name = input("Enter your name: ")
            ticket_type = input("Select ticket type ('V' for VIP/ 'R' for Regular): ").strip().upper()
            if ticket_type not in ['V', 'R']:
                print("Invalid ticket type. Please select 'V' for VIP or 'R' for Regular.")
                continue
            try:
                number = int(input("Enter the number of tickets you want to purchase: "))
                if 10 <= number <= 0:
                    print("Invalid number of tickets. Please enter a positive number.")
                    continue   
            except ValueError:
                print("Invalid input. Please enter a valid number.")
                continue
            ticketing_system.register_ticket(name, ticket_type, number)

        elif choice == '2':
            availability = ticketing_system.get_ticket_availability()
            print(f"VIP Tickets: {availability['VIP']}")
            print(f"Regular Tickets: {availability['Regular']}")

        elif choice == '3':
            processed = ticketing_system.process_tickets()
            if processed:
                print("Processed Tickets:")
                for name, ticket_type in processed:
                    print(f"{name} - {ticket_type}")
            else:
                print("No tickets to process.")

        elif choice == '4':
            name = input("Enter your name: ")
            ticket_type = input("Select ticket type to cancel ('V' for VIP/ 'R' for Regular): ").strip()
            if ticket_type not in ['V', 'R']:
                print("Invalid ticket type. Please select 'V' for VIP or 'R' for Regular.")
                continue
            try:
                number = int(input("Enter the number of tickets you want to purchase: "))
                if 10 <= number <= 0:
                    print("Invalid number of tickets. Please enter a positive number.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a valid number.")
                continue
            ticketing_system.cancel_ticket(name, ticket_type, number)

        elif choice == '5':
            summary = ticketing_system.get_ticket_summary()
            for key, value in summary.items():
                print(f"{key}: {value}")

        elif choice == '6':
            print("Thank you for using the Event Ticketing System!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

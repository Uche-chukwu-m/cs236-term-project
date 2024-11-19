import queue
import csv
from datetime import datetime

class EventTicketingSystem:
    def __init__(self, vip_tickets=50, regular_tickets=100):
        self.vip_queue = queue.Queue()
        self.regular_queue = queue.Queue()
        self.vip_tickets = vip_tickets
        self.regular_tickets = regular_tickets
        self.transaction_log = 'ticket_transactions.csv'
        
        # Initialize transaction log
        with open(self.transaction_log, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Timestamp', 'Name', 'Ticket Type', 'Status'])
    
    def register_ticket(self, name, ticket_type):
        if ticket_type == 'VIP' and self.vip_tickets > 0:
            self.vip_queue.put(name)
            self._log_transaction(name, 'VIP', 'Pending')
            return True
        elif ticket_type == 'Regular' and self.regular_tickets > 0:
            self.regular_queue.put(name)
            self._log_transaction(name, 'Regular', 'Pending')
            return True
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
        total_tickets = 50 + 100  # Initial total tickets
        sold_tickets = (50 - self.vip_tickets) + (100 - self.regular_tickets)
        
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
        print("4. View Sales Summary")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            name = input("Enter your name: ")
            ticket_type = input("Select ticket type (VIP/Regular): ").strip().title()
            
            if ticketing_system.register_ticket(name, ticket_type):
                print(f"Ticket request for {name} ({ticket_type}) registered successfully!")
            else:
                print("Sorry, no tickets available for the selected type.")
        
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
            summary = ticketing_system.get_ticket_summary()
            for key, value in summary.items():
                print(f"{key}: {value}")
        
        elif choice == '5':
            print("Thank you for using the Event Ticketing System!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

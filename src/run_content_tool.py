from content_tool import main as create_seed
from create_facebook_draft import main as create_facebook_draft


def show_menu() -> None:
    print("\nEddie's Content Tools")
    print("---------------------")
    print("1. Create a new event seed")
    print("2. Create a Facebook draft from a saved seed")
    print("3. Run the complete flow")
    print("4. Quit")


def run_full_flow() -> None:
    print("\nStep 1: Create an event seed")
    print("----------------------------")
    create_seed()

    print("\nStep 2: Create a Facebook draft")
    print("--------------------------------")
    create_facebook_draft()


def main() -> None:
    while True:
        show_menu()
        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            create_seed()
        elif choice == "2":
            create_facebook_draft()
        elif choice == "3":
            run_full_flow()
        elif choice == "4":
            print("Goodbye.")
            return
        else:
            print("Invalid choice. Enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
    
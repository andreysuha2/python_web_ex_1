from app.interfaces.console import ConsoleHandler, ConsoleInterface

INTERFACE_HANDLERS = [ ConsoleHandler(interface=ConsoleInterface()) ]

def main():
    for handler in INTERFACE_HANDLERS:
        handler.run()

if __name__ == "__main__":
    main()
from handlers import MonkRegister


def main():
    for register in MonkRegister():
        register.to_queue()


if __name__ == "__main__":
    main()

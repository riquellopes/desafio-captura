from monk.monk import MonkWorker
from handlers import MonkRegister


def main():
    worker = MonkWorker(MonkRegister())
    worker.run()

if __name__ == "__main__":
    main()

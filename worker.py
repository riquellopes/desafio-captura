from monk.monk import MonkWorker
from handlers import MonkRegister

if __name__ == "__main__":
    worker = MonkWorker(MonkRegister())
    worker.run()

from lab_data_recorder.services.base import start_service
from lab_data_recorder.services.examples import RandomNumberService


def main():
    start_service(RandomNumberService, port=18813)


if __name__ == "__main__":
    main()

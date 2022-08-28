from typing import Dict, Type
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    MULTIPLIER: int = 18
    SUBTRACTION: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.MULTIPLIER
                * (self.get_mean_speed())
                - self.SUBTRACTION)
                * self.weight
                / self.M_IN_KM
                * self.duration
                * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    MULTIPLIER_WEIGHT: float = 0.035
    MULTIPLIER_WEIGHT_SPEED: float = 0.029

    def __init__(self,
                 action,
                 duration,
                 weight,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.MULTIPLIER_WEIGHT * self.weight
                + ((self.get_mean_speed()) ** 2 // self.height)
                * self.MULTIPLIER_WEIGHT_SPEED * self.weight)
                * self.duration * self.MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SUM_MEAN_SPEED: float = 1.1
    MULTIPLIER_WEIGHT: int = 2

    def __init__(self,
                 action,
                 duration,
                 weight,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.count_pool = count_pool
        self.length_pool = length_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                + self.SUM_MEAN_SPEED)
                * self.MULTIPLIER_WEIGHT
                * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    kind_of_training: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                   'RUN': Running,
                                                   'WLK': SportsWalking
                                                   }
    return kind_of_training[workout_type](*data)


def main(train: Training) -> None:
    """Главная функция."""
    info = train.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

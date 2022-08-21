class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65
    type_of_training = ''

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

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
    type_of_training = 'RUN'

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_1 = 18
        coeff_2 = 20
        calories = (coeff_1 * (self.get_mean_speed()) - coeff_2) *\
            self.weight / self.M_IN_KM * self.duration * 60
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    type_of_training = 'WLK'

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        coeff_3 = 0.035
        coeff_4 = 0.029
        self.calories = (coeff_3 * self.weight
                         + ((self.get_mean_speed())**2 // self.height)
                         * coeff_4 * self.weight) * self.duration * 60
        return self.calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    type_of_training = 'SWM'

    def __init__(self,
                 action,
                 duration,
                 weight,
                 length_pool,
                 count_pool,
                 ):
        super().__init__(action, duration, weight)
        self.count_pool = count_pool
        self.length_pool = length_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        self.speed = self.length_pool * self.count_pool / \
            self.M_IN_KM / self.duration
        return self.speed

    def get_spent_calories(self) -> float:
        coeff_5 = 1.1
        coeff_6 = 2
        self.calories = (self.get_mean_speed() + coeff_5) * \
            coeff_6 * self.weight
        return self.calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    kind_of_training = {'SWM': Swimming,
                        'RUN': Running,
                        'WLK': SportsWalking
                        }
    train = kind_of_training[workout_type](*data)
    return train


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
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

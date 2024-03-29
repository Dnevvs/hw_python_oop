from abc import abstractmethod
from dataclasses import dataclass, asdict
from typing import List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    imessage = ('Тип тренировки: {training_type};'
                ' Длительность: {duration:.3f} ч.;'
                ' Дистанция: {distance:.3f} км;'
                ' Ср. скорость: {speed:.3f} км/ч;'
                ' Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        result = self.imessage.format(**asdict(self))
        return result


class Training:
    MIN_IN_H: float = 60
    M_IN_KM: float = 1000
    LEN_STEP: float = 0.65
    # 1.38 для плавания
    """Базовый класс тренировки."""

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
        result: float = self.action * self.LEN_STEP / self.M_IN_KM
        return result

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        # return преодолённая_дистанция_за_тренировку / время_тренировки
        result: float = self.get_distance() / self.duration
        return result

    @abstractmethod
    def get_spent_calories(self) -> float:
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = self.__class__.__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        result = InfoMessage(training_type, duration,
                             distance, speed, calories)
        return result


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        # (18 * средняя_скорость + 1.79) * вес_спортсмена / M_IN_KM *
        # время_тренировки_в_минутах
        result: float = (((self.CALORIES_MEAN_SPEED_MULTIPLIER
                         * self.get_mean_speed()
                         + self.CALORIES_MEAN_SPEED_SHIFT)
                         * self.weight / self.M_IN_KM)
                         * self.duration * self.MIN_IN_H)
        return result


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 0.035
    CALORIES_MEAN_SPEED_SHIFT: float = 0.029
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: float = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        # ((0.035 * вес + (средняя_скорость_в_метрах_в_секунду**2 /
        # рост_в_метрах) * 0.029 * вес) * время_тренировки_в_минутах)
        speed: float = (self.get_mean_speed() * self.KMH_IN_MSEC)**2
        result: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                         * (self.weight)
                         + (speed / (self.height / self.CM_IN_M))
                         * self.CALORIES_MEAN_SPEED_SHIFT
                         * self.weight) * self.duration * self.MIN_IN_H)
        return result


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 2
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        # длина_бассейна * count_pool / M_IN_KM / время_тренировки
        result: float = (self.length_pool * self.count_pool
                         / self.M_IN_KM / self.duration)
        return result

    def get_spent_calories(self) -> float:
        # (средняя_скорость + 1.1) * 2 * вес * время_тренировки
        result = ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                  * self.CALORIES_MEAN_SPEED_MULTIPLIER
                  * (self.weight)
                  * self.duration)
        return result


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    action_classes = {'SWM': Swimming,
                      'RUN': Running,
                      'WLK': SportsWalking}
    if workout_type in action_classes:
        action_class: Training = action_classes[workout_type](*data)
        return action_class
    else:
        raise ValueError(f'Некорректный тип тренировки {workout_type} !')


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    infotext: str = info.get_message()
    print(infotext)
    return


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

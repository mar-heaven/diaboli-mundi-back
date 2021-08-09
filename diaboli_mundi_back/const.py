from enum import Enum


class DeathReason(Enum):
    # 死亡方式
    NORMAL = "normal_death"


class Status(int, Enum):
    # 数据状态
    normal = 1
    deleted = 0

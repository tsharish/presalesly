from enum import Enum


class OppStatus(str, Enum):
    open = "Open"
    won = "Won"
    lost = "Lost"


class Priority(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"
    very_high = "Very High"


class TaskStatus(str, Enum):
    not_started = "Not Started"
    in_progress = "In Progress"
    completed = "Completed"


class Permission(str, Enum):
    create = "Create"
    read = "Read"
    update = "Update"
    delete = "Delete"


class MLAlgorithm(str, Enum):
    catboost = "catboost"
    lightgbm = "lightgbm"


class Scoring(str, Enum):
    accuracy = "accuracy"
    f1 = "f1"
    precision = "precision"
    recall = "recall"

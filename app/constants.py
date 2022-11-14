import enum


class ExportStatusEnum(enum.Enum):
    SUCCESS = 1
    ERROR = 2


class ExportFileTypeEnum(enum.Enum):
    PDF = 1
    CSV = 2
    XLS = 3

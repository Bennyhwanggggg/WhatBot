import enum


class QueryError(enum.Enum):
    UNKNOWN_QUERY_TYPE = 'Unknown query type'
    NO_DATA = 'Do not have information to answer your question'


class UploadFileError(enum.Enum):
    NO_FILE = 'No file part.'
    NO_FILE_SELECTED = 'No file selected for uploading.'
    INVALID_FORMAT = 'The format of the file you are trying to upload is invalid.'

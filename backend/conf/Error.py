import enum


class QueryError(enum.Enum):
    UNKNOWN_QUERY_TYPE = 'Sorry, I cannot understand your question.'
    NO_DATA = "Sorry, I don't have enough information to answer your question."
    NO_SUCH_COURSE = "Sorry, I don't have the information for this course."
    NOT_AVAILABLE = "Sorry, I cannot do that."
    NO_STUDENT = "Sorry, I don't have the data for this student."
    NO_CONSULTATION = "Sorry, you don't have any consultation booking to show."


class UploadFileError(enum.Enum):
    NO_FILE = 'No file part.'
    NO_FILE_SELECTED = 'No file selected for uploading.'
    INVALID_FORMAT = 'The format of the file you are trying to upload is invalid.'


class AuthenticationError(enum.Enum):
    INVALID_CREDENTIALS = 'Invalid username or password'

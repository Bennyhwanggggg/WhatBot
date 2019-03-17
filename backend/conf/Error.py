import enum


class QueryError(enum.Enum):
    UNKNOWN_QUERY_TYPE = 'Unknown query type'
    NO_DATA = 'Do not have information to answer your question'

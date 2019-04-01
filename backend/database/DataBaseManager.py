import psycopg2
import boto3
import re
from conf.Logger import Logger

"""
    Logger setup
"""
logger = Logger(__name__).log

HOST = 'whatbot.ciquzj8l3yd7.ap-southeast-2.rds.amazonaws.com'
USERNAME = 'whatbot'
PASSWORD='12345678'
DATABASE = "postgres"
PORT = '5432'
FILE_STORAGE = 'whatbots3'
aws_access_key_id = 'AKIAUHOEW66FFI2ABONG'
aws_secret_access_key = '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'


class DataBaseManager:
    def __init__(self, host=HOST, port=PORT, database_name=DATABASE, file_storage_name=FILE_STORAGE):
        self.host, self.port, self.database_name = host, port, database_name
        self.file_storage_name = file_storage_name
        self.connection, self.cursor, self.s3_resource = None, None, None

    def connect_database(self):
        """Manages all database connection and autocommits

        :return: None
        """
        if self.connection is not None:
            return
        self.connection = psycopg2.connect(database=self.database_name,
                                           user=USERNAME,
                                           password=PASSWORD,
                                           host=self.host,
                                           port=str(self.port))
        self.connection.set_session(autocommit=True)
        self.cursor = self.connection.cursor()
        logger.info('Connection to AWS opened')

    def disconnect_database(self):
        """Manages all disconnection from database. Resets connection and cursor to None

        :return: None
        """
        if self.connection and self.cursor:
            self.cursor.close()
            self.connection.close()
            logger.info('Connection to AWS closed')
        self.connection, self.cursor = None, None

    def execute_query(self, query, *args):
        """Used to execute query with the query string given and the arguments used for that
        query. Arguments are given through *args so we can use self.cursor.execute to sanitize
        the query and prevent SQL injection attacks.

        :param query: query string
        :type: str
        :param args: tuple of arguments that goes into query string in a tuple. This field is optional.
        :type: tuple
        :return: result of query
        :rtype: list or str
        """
        result = None
        try:
            if not self.connection and not self.cursor:
                self.connect_database()
            if args:
                self.cursor.execute(query, (args[0]))
            else:
                self.cursor.execute(query)
            regex = re.compile(r'SELECT', re.IGNORECASE)
            result = self.cursor.fetchall() if regex.search(query) else "execute successfully"
        except (Exception, psycopg2.Error) as e:
            logger.error("Error executing query:\n{}".format(str(e)))
        finally:
            self.disconnect_database()
        logger.debug('Query is: {}\nResult is: {}'.format(query, result))
        return result

    def connect_file_storage(self):
        """Used to establish AWS S3 bucket connections and instances with the provided access keys

        :return: None
        """
        if self.s3_resource is None:
            self.s3_resource = boto3.resource('s3',
                                              aws_access_key_id=aws_access_key_id,
                                              aws_secret_access_key= aws_secret_access_key)
            logger.info('Connection to file storage established')
        else:
            logger.warning('Connection to file storage already exist')

    def disconnect_file_storage(self):
        """Used to disconnect from S3 buckets.

        :return: None
        """
        if self.s3_resource is not None:
            self.s3_resource = None
            logger.info('Connection to file storage closed')
        else:
            logger.warning('No connection to file storage to disconnect from')

    def upload_file(self, path_to_file, file_name):
        """Used to upload file to S3 bucket for file storage.

        :param path_to_file: path of the file to upload to
        :type: str
        :param file_name: the file name you want it to be stored as on S3
        :type: str
        :return: None
        """
        self.connect_file_storage()
        self.s3_resource.Bucket(self.file_storage_name).upload_file(Filename=path_to_file, Key=file_name)
        self.disconnect_file_storage()

    def download_file(self, file_name, path_to_download_to):
        """Download file from S3

        :param file_name: file on S3 you want to download
        :type: str
        :param path_to_download_to: location where you want to download the file to
        :type: str
        :return: None
        """
        self.connect_file_storage()
        self.s3_resource.Bucket(self.file_storage_name).download_file(Key=file_name, Filename=path_to_download_to)
        self.disconnect_file_storage()

    def read_file(self, file_name):
        """Read a file from S3 without downloading. Converts the bytes data into string.

        :param file_name: file you want to read
        :type: str
        :return: file content
        :rtype: str
        """
        self.connect_file_storage()
        binary_data = self.s3_resource.Object(self.file_storage_name, file_name).get()['Body'].read()
        self.disconnect_file_storage()
        return self.process_string_data(binary_data.decode('utf-8'))

    def get_list_of_files_from_storage(self):
        self.connect_file_storage()
        objects = self.s3_resource.Bucket(self.file_storage_name).objects.all()
        self.disconnect_file_storage()
        return [object.key for object in objects]

    def process_string_data(self, string_data, separator='\n'):
        """Convert string data into lists using a separator. By default it is new line ('\n').
        This is used mainly to process the data we read from S3

        :param string_data: string data to process
        :type: str
        :param separator: separator to use for processing
        :type: str
        :return: list of strings separated by the specified separator
        :rtype: list[str]
        """
        return [x for x in string_data.split(separator)]

    """
        Common SQL query operations
    """
    def get_course_outline(self, cid):
        key_part = '%' + cid.upper()
        query = "SELECT description,outline_url from info_handbook where cid like %s"
        inputs = (key_part, )
        return self.execute_query(query, inputs)

    def get_all_lecturers(self):
        query = "SELECT * from lecturer"
        return self.execute_query(query)

    def make_consultation_booking(self, tid):
        query = "UPDATE Timeslot SET available = %s  WHERE tid = %s"
        inputs = ('False', tid, )
        return self.execute_query(query, inputs)

    def get_consultation_timeslots(self, tid):
        query = "SELECT tid, start_time, end_time, available from Timeslot Where tid = %s"
        inputs = (tid, )
        return self.execute_query(query, inputs)

    def add_course(self, course_code, course_name, timetable, adk, comment):
        query = "INSERT INTO courselist(course_code, course_name, timetable, ADK, comment) VALUES (%s, %s, %s, %s, %s)"
        inputs = (course_code, course_name, timetable, adk, comment, )
        return self.execute_query(query, inputs)

    def add_handbook_entry(self, cid, title, credit, prerequisite, outline_url, faculty_url, school_url, offer_term,
                           campus, description, pdf_url, indicative_contact_hr, commonwealth_std, domestic_std,
                           international_std):
        query = "INSERT INTO info_handbook(cid, title, credit, prerequisite, outline_url, faculty_url, school_url, " \
                "offer_term, campus, description, pdf_url, indicative_contact_hr, commonwealth_std, domestic_std, " \
                "international_std) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        inputs = (cid, title, credit, prerequisite, outline_url, faculty_url,
                  school_url, offer_term, campus, description, pdf_url,
                  indicative_contact_hr, commonwealth_std, domestic_std, international_std, )
        return self.execute_query(query, inputs)

    def get_course(self, cid):
            key_part = '%' + cid.upper()
            query = "SELECT * from courselist where course_code like %s"
            inputs = (key_part, )
            return self.execute_query(query, inputs)

    def get_location(self, cid):
        key_part = '%' + cid.upper()
        query = "SELECT campus from info_handbook where cid like %s"
        inputs = (key_part,)
        return self.execute_query(query, inputs)

    def get_tuition_fee(self, cid):
        key_part = '%' + cid.upper()
        query = "SELECT commonwealth_std, domestic_std, international_std from info_handbook where cid like %s"
        inputs = (key_part,)
        return self.execute_query(query, inputs)

    def get_faculty(self, cid):
        key_part = '%' + cid.upper()
        query = "SELECT faculty_url from info_handbook where cid like %s"
        inputs = (key_part, )
        return self.execute_query(query, inputs)

    def get_prerequisites(self, cid):
        key_part = '%' + cid.upper()
        query = "SELECT prerequisite from info_handbook where cid like %s"
        inputs = (key_part, )
        return self.execute_query(query, inputs)

    def get_offer_term(self, cid):
        key_part = '%' + cid.upper()
        query = "SELECT offer_term from info_handbook where cid like %s"
        inputs = (key_part, )
        return self.execute_query(query, inputs)

    def get_indicative_hours(self, cid):
        key_part = '%' + cid.upper()
        query = "SELECT indicative_contact_hr from info_handbook where cid like %s"
        inputs = (key_part,)
        return self.execute_query(query, inputs)

    def get_pdf_url(self, cid):
        key_part = '%' + cid.upper()
        query = "SELECT pdf_url from info_handbook where cid like %s"
        inputs = (key_part,)
        return self.execute_query(query, inputs)

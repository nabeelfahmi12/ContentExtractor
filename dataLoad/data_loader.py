import pandas as pd
# import os
from logger.appLogger import AppLogger
from flask import Flask, render_template,request
import pymongo



class DataGetter():
    """
    This class shall  be used for obtaining the data from the source for training.

    Written By: Nabeel Fahmi
    Version: 1.0
    Revisions: None

    """

    def __init__(self):
        """
                Method Name: __init__
                Description: This method is for attributes initialization
                Output: attributes

                Written By: Nabeel fahmi
                Version: 1.0
                Revisions: None

        """
        """
        self.log_file = 'logs/dataLoadLogs.txt'
        if os.path.exists(self.log_file):
            self.file_mode = 'a+'  # append if already exists
        else:
            self.file_mode = 'w'  # make a new file if not
        print(self.file_mode)
        print(os.getcwd())
        self.log_file_name = open(self.log_file,self.file_mode)
        """
        self.log_file_name = open('logs/dataLoadLogs.txt', 'a+')
        self.logger = AppLogger()

    def read_data_from_csv(self, file_name):
        """
                Method Name: read_data_from_csv
                Description: This method reads the data from a CSV file.
                Output: A pandas DataFrame.
                On Failure: Raise Exception

                Written By: Nabeel Fahmi
                Version: 1.0
                Revisions: None

                """
        self.logger.log(self.log_file_name, 'Entered the read_data_from_csv method of the Data_Getter class')
        try:
            self.csv = pd.read_csv(file_name, sep=',', header='infer', names=None, usecols=None)
            self.logger.log(self.log_file_name,
                            'Data Load Successful.Exited the read_data_from_csv method of the Data_Getter class')
            return self.csv
        except Exception as e:
            self.logger.log(self.log_file_name,
                            'Exception occured in read_data_from_csv method of the Data_Getter class. Exception message: ' + str(
                                e))
            self.logger.log(self.log_file_name,
                            'Data Load Unsuccessful.Exited the read_data_from_csv method of the Data_Getter class')
            raise Exception()
    def read_data_from_excel(self, file_name):
        """
                       Method Name: read_data_from_excel
                       Description: This method reads the data from a excel file.
                       Output: A pandas DataFrame.
                       On Failure: Raise Exception

                       Written By: Nabeel Fahmi
                       Version: 1.0
                       Revisions: None

                       """


        self.logger.log(self.log_file_name, 'Entered the read_data_from_excel method of the Data_Getter class')
        try :
            excel = pd.read_excel(file_name, sheet_name=0, header=0, names=None, index_col=None, usecols=None, )
            self.logger.log(self.log_file_name,'Data Load Successful.Exited the read_data_from_excel method of the Data_Getter class')
            return pd.DataFrame(excel)
        except Exception as e:
            self.logger.log(self.log_file_name,
                            'Exception occured in read_data_from_excel method of the Data_Getter class. Exception message: ' + str(
                                e))
            self.logger.log(self.log_file_name,
                            'Data Load Unsuccessful.Exited the read_data_from_excel method of the Data_Getter class')
            raise Exception()
    def read_data_from_json(self, file_name):
        """
                       Method Name: read_data_from_json
                       Description: This method reads the data from a json file.
                       Output: A pandas DataFrame.
                       On Failure: Raise Exception

                       Written By: Nabeel Fahmi
                       Version: 1.0
                       Revisions: None

                       """


        self.logger.log(self.log_file_name, 'Entered the read_data_from_json method of the Data_Getter class')
        try:
            json = pd.read_json(file_name)
            self.logger.log(self.log_file_name, 'Data Load Successful.Exited the read_data_from_json method of the Data_Getter class' )
            return pd.DataFrame(json)
        except Exception as e:
            self.logger.log(self.log_file_name,
                            'Exception occured in read_data_from_json method of the Data_Getter class. Exception message: ' + str(
                                e))
            self.logger.log(self.log_file_name,
                            'Data Load Unsuccessful.Exited the read_data_from_json method of the Data_Getter class')
            raise Exception()

    def read_data_from_text(self, file_name, delim):
        """
                       Method Name: read_data_from_text
                       Description: This method reads the data from a text file.
                       Output: A pandas DataFrame.
                       On Failure: Raise Exception

                       Written By: Nabeel Fahmi
                       Version: 1.0
                       Revisions: None

                       """


        self.logger.log(self.log_file_name, 'Entered the read_data_from_text method of the Data_Getter class')
        try:
            text = pd.read_csv(file_name, sep = delim, header = "infer")
            self.logger.log(self.log_file_name, 'Data Load Successful.Exited the read_data_from_text method of the Data_Getter class' )
            return pd.DataFrame(text)
        except Exception as e:
            self.logger.log(self.log_file_name,
                            'Exception occured in read_data_from_json method of the Data_Getter class. Exception message: ' + str(
                                e))
            self.logger.log(self.log_file_name,
                            'Data Load Unsuccessful.Exited the read_data_from_json method of the Data_Getter class')
            raise Exception()

    def read_data_from_html(self, file_name):
        """
                       Method Name: read_data_from_html
                       Description: This method reads the data from a html file.
                       Output: A pandas DataFrame.
                       On Failure: Raise Exception

                       Written By: iNeuron Intelligence
                       Version: 1.0
                       Revisions: None

                       """

        self.logger.log(self.log_file_name, 'Entered the read_data_from_html method of the Data_Getter class')
        try :
            html = pd.read_html(file_name)
            data = html[0]
            self.logger.log(self.log_file_name, 'Data Load Successful.Exited the read_data_from_html method of the Data_Getter class')
            return pd.DataFrame(data)
        except Exception as e:
            self.logger.log(self.log_file_name,
                            'Exception occured in read_data_from_html method of the Data_Getter class. Exception message: ' + str(
                                e))
            self.logger.log(self.log_file_name,
                            'Data Load Unsuccessful.Exited the read_data_from_html method of the Data_Getter class')
            raise Exception()

    def mongoDB_homePage(self):
        return render_template("mongo_db_login_page.html")

    def connection_to_mongodb(self):
        try:
            root = request.form['content']
            password = request.form['content1']
            dataset = request.form['content2']
            data = request.form['content3']
            dbConn = pymongo.MongoClient(
                "mongodb://" + root + ":" + password + "/")  # have to provide  thier respective host ID,connection to the mongo DB server
            db = dbConn[dataset]
            test = db[data]  # have to provide their collection name,accessing the collection inside that data base
            test = pd.DataFrame(list(test.find()))  # converting the collection to DataFrame
            print(test)
            return test
        except Exception as e:
            print('The Exception message is: ', e)
            return render_template('mongo_db_login_page.html')

    def sql_homePage(self):
        return render_template("sql_login_page.html")

    # def connection_to_sql():
    #     root = request.form['content']
    #     password = request.form['content1']
    #     database = request.form['content2']
    #     dataset = request.form['content3']
    #     con = sqlalchemy.create_engine("mysql+pymysql://"+root+":"+password+"@"host:port")  # have to provide  thier respective host ID,connection to the mongo DB server
    #     sql_data = pd.read_sql_table(table, con)
    #     return sql_data

    def get_data(self, file_type, file,delimeter):
        """
                        Method Name: get_data
                        Description: This method reads the data based on the file
                                    format
                        Output: A pandas DataFrame.
                        On Failure: Raise Exception

                        Written By: Nabeel Fahmi
                        Version: 1.0
                        Revisions: None

                        """
        self.logger.log(self.log_file_name, 'Entered the get_data method of '
                                            'the Data_Getter class')
        try:
            if file_type == 'csv':
                data = self.read_data_from_csv(file)
                self.logger.log(self.log_file_name,
                                    'Data Load Successful.Exited the get_data method of the Data_Getter class')
            elif file_type == 'xlsx':
                data = self.read_data_from_excel(file)
                self.logger.log(self.log_file_name,
                                    'Data Load Successful.Exited the get_data method of the Data_Getter class')
            elif file_type == 'html':
                data = self.read_data_from_html(file)
                self.logger.log(self.log_file_name,
                                    'Data Load Successful.Exited the get_data method of the Data_Getter class')
            elif file_type == 'json':
                data = self.read_data_from_json(file)
                self.logger.log(self.log_file_name,
                                    'Data Load Successful.Exited the get_data method of the Data_Getter class')

                self.logger.log(self.log_file_name,
                            'Data Load Successful.Exited the get_data method of the Data_Getter class')

            elif file_type == 'txt':
                data = self.read_data_from_text(file,delimeter)
                self.logger.log(self.log_file_name,
                                'Data Load Successful.Exited the get_data method of the Data_Getter class')

                self.logger.log(self.log_file_name,
                                'Data Load Successful.Exited the get_data method of the Data_Getter class')

            data.columns=data.columns.str.replace(r'\s+', '') # remove spaces from the column names

            return data
        except Exception as e:
            self.logger.log(self.log_file_name,
                            'Exception occured in get_data method of the Data_Getter class. Exception message: ' + str(
                                e))
            self.logger.log(self.log_file_name,
                            'Data Load Unsuccessful.Exited the get_data method of the Data_Getter class')
            raise Exception()





from logger.appLogger import AppLogger


class Preprocessor():
    """
        This class shall be used to include all Data Pre-processing techniques to be
        fed to the Machine Learning Models

        Written By: Nabeel Fahmi
        Version: 1.0
        Revisions: None

    """

    def __init__(self):
        self.file_object = open('logs/dataPreprocessingLogs.txt', 'a+')
        self.logger_object = AppLogger()

    def get_data_profile(self, data):
        """
            Method Name: get_data_profile
            Description: This method will be used to do data-profiling

            Input Description:
            data: Name of the input dataframe

            On Exception: Write the exception in the log file. Raise an exception with the appropriate error message

            Output: The full data profile report using a dictionary

            Written By: Nabeel Fahmi
            Version: 1.0
            Revisions: None
        """

        self.data_profile = {}
        self.missing_values = {}
        self.missing_val_pct = {}
        self.data_profile['rows'] = data.shape[0]
        self.data_profile['columns'] = data.shape[1]
        self.missing_vals = data.isna().sum()
        for col in data.columns:
            if data[col].isnull().sum() > 0:
                self.missing_values[col] = data[col].isnull().sum()
                self.missing_val_pct[col] = (data[col].isnull().sum() / len(data)) * 100
        self.data_profile['missing_values'] = self.missing_values
        self.data_profile['missing_vals_pct'] = self.missing_val_pct
        self.data_profile['categorical_columns'] = list(data.select_dtypes(exclude=["int64", "float"]))
        self.data_profile['num_categorical_columns'] = len(self.data_profile['categorical_columns'])
        self.data_profile['numerical_columns'] = list(data.select_dtypes(exclude=["object"]))
        self.data_profile['num_numerical_columns'] = len(self.data_profile['numerical_columns'])
        self.data_profile['num_duplicate_rows'] = data.duplicated().sum()


        self.describe = data.describe().T
        if 'std' not in self.describe:
            self.describe = data.astype(float).describe().T

        self.standard_deviation = self.describe[self.describe['std'] == 0]
        self.standard_deviation = list(self.standard_deviation.index)
        self.data_profile['num_col_with_std_zero'] = len(self.standard_deviation)
        if len(self.standard_deviation) > 0:
            self.data_profile['cols_with_std_zero'] = self.standard_deviation

        self.size = data.size / (1024 * 1024)
        self.data_profile['datasize'] = str(round(self.size, 4)) + " MB"

        return self.data_profile

    def separate_label_feature(self, data, label_column_name):
        """
            Method Name: separate_label_feature
            Description: This method separates the features and a Label Coulmns.
            Output: Returns two separate Dataframes, one containing features and the other containing Labels .
            On Failure: Raise Exception

            Written By: Nabeel Fahmi
            Version: 1.0
            Revisions: None

        """
        self.logger_object.log(self.file_object, 'Entered the separate_label_feature method of the Preprocessor class')

        try:
            self.X = data.drop(labels=label_column_name,axis=1)  # drop the columns specified and separate the feature columns
            self.Y = data[label_column_name]  # Filter the Label columns
            self.logger_object.log(self.file_object,
                                   'Label Separation Successful. Exited the separate_label_feature method of the Preprocessor class')
            return self.X, self.Y
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in separate_label_feature method of the Preprocessor class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'Label Separation Unsuccessful. Exited the separate_label_feature method of the Preprocessor class')
            raise Exception()

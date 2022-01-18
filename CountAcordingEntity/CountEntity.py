from logger.appLogger import AppLogger
import pandas as pd
import numpy as np





class CountEntity ():
    """
    This class shall be used for Count variable according Entity for selected colour.

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
        self.log_file_name = open('logs/CountAcourdigEntity.txt', 'a+')
        self.logger = AppLogger()

    def count_no_variable(self, df, post_coloum, coloumn_list, keyword_list):
        dataframe = None
        try:
            json = {'key word': keyword_list}

            for coloumn in coloumn_list:
                list = []
                total_list = []
                for word in keyword_list:
                    count = []

                    df2 = df[df[post_coloum].str.contains(word) == True].index.tolist()
                    for i in df2:
                        if (pd.isnull(df[coloumn][i])):
                            continue
                        if isinstance(df[coloumn][i], str):
                            count.append(df[coloumn][i])
                        else:
                            count.append(df[coloumn][i])

                    total = sum(count)
                    list.append(total)
                    total_list.append(len(df2))
                json['Toatl no of post'] = total_list
                json[coloumn] = list
            dataframe = pd.DataFrame(json)
        except Exception as e:
            self.logger.log(self.log_file_name,
                            'Exception occurred in creating Selected Coloum Dataframe. Exception message: ' + str(
                                e))
        return dataframe



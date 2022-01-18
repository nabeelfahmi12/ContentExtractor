import pandas as pd
import pymongo
from flask import Flask, render_template, request, send_file
from sqlalchemy import create_engine
from CountAcordingEntity.CountEntity import CountEntity
from dataLoad.data_loader import DataGetter
from dataPreprocessing.preProcess import Preprocessor

app = Flask(__name__, template_folder='templates')

dataset = None
Count_dataset = None


@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/get_data', methods=['GET', 'POST'])
def get_data_from_user():
    return render_template('data_load.html')


@app.route('/load_data', methods=['POST'])
def load_data_from_source():
    """
                                Method Name: load_data_from_source
                                Description: describes data frame infomation as below:
                                             	The number of rows
                                             	The number of columns
                                             	Number of missing values per column and their percentage
                                             	Total missing values and it’s percentage
                                             	Number of categorical columns and their list
                                             	Number of numerical columns and their list
                                             	Number of duplicate rows
                                             	Number of columns with zero standard deviation and their list
                                                 Size occupied in RAM
                                Output: tabels.html page
                                On Failure: Raise Exception
                                Written By: iNeuron Intelligence
                                Revisions: None
                       """
    # declared as a global variable
    global dataset, delimeter
    try:
        if request.files['filename'] is not None:
            file = request.files['filename']  # File can be obtained from request.files

        file_type = request.form['source']  # File Source can be obtained here
        db_type = request.form['source_db']
        # print(file,file_type)
        if request.form['delimiter'] is not None:
            delimeter = str(request.form['delimiter'])
        # Declare global variable
        """
            if request.form['file'] is None and request.form['file_type'] is  None:
            data_getter = DataGetter()  # instantiation for genrating preprocessing logs
            dataset = data_getter.get_data(file_type, file, delimeter)
        """
        if file_type == "DB" and db_type == "mongo_db":
            try:
                root = request.form['content']
                password = request.form['content1']
                dataset = request.form['content2']
                data = request.form['content3']
                dbConn = pymongo.MongoClient(
                    "mongodb://" + root + "/" + password)  # have to provide  their respective host ID,connection to 
                # the mongo DB server 
                db = dbConn[dataset]
                test = db[data]  # have to provide their collection name,accessing the collection inside that data base
                dataset = pd.DataFrame(list(test.find()))  # converting the collection to DataFrame

                dataset.drop(columns=['_id'], axis=1, inplace=True)

                preprocessor = Preprocessor()  # instantiation for genrating preprocessing logs
                data_profile = preprocessor.get_data_profile(dataset)
                return render_template('tabels.html', tables=[dataset.head(10).to_html(classes='data', header="True")],
                                       columns=dataset.columns, profile=data_profile)
            except Exception as e:
                print('The Exception message is: ', e)
                return render_template('index.html', message="No input entered")
        elif file_type == "DB" and db_type == "mysql":
            try:
                root = request.form['content']
                password = request.form['content1']
                database = request.form['content2']
                table = request.form['content3']
                con = create_engine("mysql+pymysql://" + root + ":" + password + "@localhost/" + database)
                sql = "SELECT * FROM " + table
                dataset = pd.read_sql(sql, con)
                preprocessor = Preprocessor()  # instantiation for genrating preprocessing logs
                data_profile = preprocessor.get_data_profile(dataset)
                return render_template('tabels.html', tables=[dataset.head(10).to_html(classes='data', header="True")],
                                       columns=dataset.columns, profile=data_profile)

            except Exception as e:
                print('The Exception message is: ', e)
                return render_template('index.html', message="No input entered")


        else:
            data_getter = DataGetter()  # instantiation for genrating preprocessing logs
            dataset = data_getter.get_data(file_type, file,
                                           delimeter)  # call get_data method, it will load the dataset into dataframe

            # get number of independent variables
            no_of_independent_variables = len(dataset.columns) - 1

            # Setting the config values

            preprocessor = Preprocessor()  # instantiation for genrating preprocessing logs
            data_profile = preprocessor.get_data_profile(dataset)  # call get_data_profile
            # print(data.head())
            # render template tabels.html with the respective dataset

    except Exception as e:
        return render_template("index.html", message="No file selected")
    print("preprocessor is done")
    return render_template('tabels.html', tables=[dataset.head(10).to_html(classes='data', header="True")],
                           columns=dataset.columns, profile=data_profile)


@app.route('/entity_finder', methods=['GET', 'POST'])
def entity_finder():
    global dataset, Count_dataset
    try:
        entity_type = request.form['problem_type']
        Target_coloum = request.form['target_column']
        selected_coloum_list = request.form.getlist('Select_Matrix')
        text = request.form['keywords']

        keyword_list = text.split(',')
        Count = CountEntity()
        Count_dataset = Count.count_no_variable(df=dataset, post_coloum=Target_coloum, keyword_list=keyword_list,
                                                coloumn_list=selected_coloum_list)
        return render_template(
            'count_entity_dataset.html',
            tables=[Count_dataset.head(10).to_html(classes="table table-striped table-bordered", header="True")],
            coloums=Count_dataset.columns
        )
    except Exception as e:
        print(e)
        msg = 'No Match Found'
        return render_template(
            'base1.html',
            tables=[dataset.head(10).to_html(classes="table table-striped table-bordered", header="True")],
            coloums=dataset.columns, msg=msg
        )


@app.route('/download', methods=['POST'])
def download():
    global Count_dataset
    try:
        filetype = request.form['filetype']
        if filetype == 'csv':
            Count_dataset.to_csv('Output/file.csv')
            return send_file('Output/file.csv',
                             mimetype='text/csv',
                             attachment_filename='Adjacency.csv',
                             as_attachment=True)
        elif filetype == 'xlsx':
            print('yes')
            Count_dataset.to_excel('Output/file.xlsx')
            print('yes 1')
            return send_file('Output/file.xlsx',
                             mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                             attachment_filename='Adjacency.xlsx',
                             as_attachment=True)
        elif filetype == 'json':
            Count_dataset.to_json('Output/file.json')
            return send_file('Output/file.json',
                             mimetype='application/json',
                             attachment_filename='Adjacency.json',
                             as_attachment=True)
    except Exception as e:
        print(e)
        return render_template(
            'count_entity_dataset.html',
            tables=[Count_dataset.head(10).to_html(classes="table table-striped table-bordered", header="True")],
            coloums=Count_dataset.columns
        )


if __name__ == '__main__':
    app.run()

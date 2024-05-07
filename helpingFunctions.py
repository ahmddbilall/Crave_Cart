import re
import pickle
import pandas as pd


def validate_email(email):
    regex = '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email)


def get_all_item_name():
    menus = pickle.load(open('menus.pkl','rb'))
    return menus['ItemName'].values()


def recommend(name):
    data = pd.DataFrame(pickle.load(open('menus.pkl','rb')))
    similarity = pickle.load(open('similarity.pkl','rb'))
    index = data[data['ItemName'] == name].index[0]
    distances = similarity[index]
    
    
    listOfRecomendation = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:20]
    
    Recommended = []
    for i in listOfRecomendation:
        Recommended.append(int(data.iloc[i[0]].Menuid))
    return Recommended

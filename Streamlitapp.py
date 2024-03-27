import os
import pickle

import matplotlib.pyplot as plt
import seaborn as sns

import streamlit as st
from dotenv import load_dotenv

from utils.b2 import B2
from utils.modeling import *



REMOTE_DATA = 'Train_subset.csv'
df = pd.read_csv("Train_subset.csv")

load_dotenv()

# load Backblaze connection
b2 = B2(endpoint=os.environ['B2_ENDPOINT'],
        key_id=os.environ['B2_KEYID'],
        secret_key=os.environ['B2_applicationKey'])

def get_data():
    # collect data frame of reviews and their sentiment
    b2.set_bucket(os.environ['B2_BUCKETNAME'])
    df = b2.get_df(REMOTE_DATA)
    return df

st.title("The distribution of ages among different segments of customers")

def forward_fill(df):
    df_filled = df.apply(lambda col: col.fillna(method='ffill') if col.isnull().any() else col, axis=0)
    return df_filled

train1  = forward_fill(df)
train1.isnull().sum()

train=train1.drop(['ID','Var_1'],axis=1)

data_cleaned = df.dropna(subset=['Age', 'Segmentation'])

fig = plt.figure(figsize=(12, 8))
sns.violinplot(x='Segmentation', y='Age', data=data_cleaned, palette='Set3')
plt.title('Distribution of Ages Among Different Customer Segments')
plt.xlabel('Segmentation')
plt.ylabel('Age')
plt.grid(True)
plt.tight_layout()
plt.show()

st.pyplot(fig)

st.dataframe(df.head(30))

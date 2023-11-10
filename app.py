import os
import json

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from utils.b2 import B2


if 'STREAMLIT_B2_ENDPOINT' in os.environ.keys():
    config_vars = {
        'B2_ENDPOINT': os.environ['STREAMLIT_B2_ENDPOINT'],
        'B2_KEYID': os.environ['STREAMLIT_B2_KEYID'],
        'B2_APPKEY':os.environ['STREAMLIT_B2_APPKEY'],
        'B2_BUCKETNAME': os.environ['STREAMLIT_B2_BUCKETNAME']
    }
else:
    with open('./config_vars.json') as f:
        config_vars = json.load(f)

b2 = B2(config_vars['B2_ENDPOINT'], 
        config_vars['B2_KEYID'],
        config_vars['B2_APPKEY'])

st.write(
'''
## Seattle Home Prices
We can import data into our streamlit app using pandas read_csv then display the resulting dataframe with st.dataframe()
''')

b2.set_bucket(config_vars['B2_BUCKETNAME'])

data = b2.to_df('seattle_home_prices/SeattleHomePrices_2.csv')
data = data.rename(columns={'LATITUDE': 'lat', 'LONGITUDE': 'lon'})
st.dataframe(data)

# PART 4

st.write(
'''
### Graphing and Buttons
Lets graph some of our data with matplotlib. We can also add buttons to add interactivity to our app.
'''
)

fig, ax = plt.subplots()

ax.hist(data['PRICE'])
ax.set_title('Distribution of House Prices in $100,000s')

show_graph = st.checkbox('Show Graph', value=True)

if show_graph:
    st.pyplot(fig)

# PART 5
    
st.write(
'''
### Mapping and Filtering Our Data
We can also use streamlits built in mapping functionality.
We can use a slider to filter for houses within a particular price range as well.
'''
)

price_input = st.slider('House Price Filter', int(data['PRICE'].min()), int(data['PRICE'].max()), 100000 )

price_filter = data['PRICE'] < price_input
st.map(data.loc[price_filter, ['lat', 'lon']])

# PART 6

st.write(
'''
## Train a linear Regression Model
Create a model to predict house price from sqft and number of beds
'''
) 

# There is a better way to do this ...
from sklearn.linear_model import LinearRegression

clean_data = data.dropna(subset=['PRICE', 'SQUARE FEET', 'BEDS'])

X = clean_data[['SQUARE FEET', 'BEDS']]
y = clean_data['PRICE']

lm = LinearRegression()

lm.fit(X, y)


# PART 7

st.write(
'''
## Make predictions with the trained model from user input
'''
)

sqrft = st.number_input('Square Footage of House', value=2000)
beds = st.number_input('Number of Bedrooms', value=3)

input_data = pd.DataFrame({'SQUARE FEET': [sqrft], 'BEDS': [beds]})
pred = lm.predict(input_data)[0]
st.write(
f'Predicted Sale Price of House: ${int(pred):,}'
)
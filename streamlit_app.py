# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customise Your Smoothie! :cup_with_straw:")
st.write("Choose the fruit you want in your custom Smoothie!")

st.markdown("""
- :page_with_curl: [Streamlit open source documentation](https://docs.streamlit.io)
- :snowflake: [Streamlit in Snowflake documentation](https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit)
- :books: [Demo repo with templates](https://github.com/Snowflake-Labs/snowflake-demo-streamlit)
- :memo: [Streamlit in Snowflake release notes](https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake)
""")


name_on_order = st.text_input('Name on Smoothie:')
st.write('The name of the smoothie will be:', name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list = st.multiselect(
    'choose upto 5 ingredients:',my_dataframe
)
if ingredients_list:
    
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    st.write(ingredients_string)

my_insert_stmt = """INSERT INTO smoothies.public.orders (ingredients, name_on_order) 
                    VALUES ('""" + ingredients_string + """', '""" + name_on_order + """')"""

st.write(my_insert_stmt)

time_to_insert = st.button('Submit Order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered,' + name_on_order + '!', icon="✅")

from streamlit_extras.let_it_rain import rain
from openai.error import AuthenticationError
from pydantic import ValidationError
import streamlit as st
from PIL import Image
import pinecone, json
import numpy as np

from firebase_admin import credentials
from firebase_admin import firestore
import firebase_admin

from models import (
    layer_1,
    get_similarity_search_from_pinecone,
    non_refine_target,
    layer_2,
    create_df_food_nutrient,
    get_CatFood,
    review_table,
)
from prompts import (
    system_message_layer_1,
    human_message_layer_1,
    response_schemas_layer_1,
    response_schemas_layer_2,
    human_message_non_refine,
    refine_prompt_template,
    initial_qa_template,
)

from login import sidebar_login


PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]
PINECONE_API_ENV = st.secrets["PINECONE_API_ENV"]
PINECONE_INDEX_NAME = st.secrets["PINECONE_INDEX_NAME"]
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_API_ENV)

key_dict = json.loads(st.secrets["textkey_catfood"])

if not firebase_admin._apps:
    cred = credentials.Certificate(key_dict)
    firebase_admin.initialize_app(cred)
db = firestore.client()

SUPER_USER = "MyCatBeeluIsTheBest"

page_title = "Cat Disease GPT"
page_icon = "🐈"
layout = "centered"

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)
sidebar_login(db=db)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

input_text = st.text_area(
    "Type in your cat's symptom",
    placeholder="ex: My cat vomits, gets thirsty, lose weith ...",
)
button = st.button("Submit")

refine_target = [
    "Hepatic Lipidosis",
    "Lower Urinary Tract Diseases/Feline Interstitial Cystitis",
    "Chronic Kidney Disease",
    "Diabetes",
    "Pancreatitis",
    "Inflammatory Bowel Disease(IBD)",
    "Hyperthyroidism",
]

if st.session_state.get("OPENAI_API_KEY") == SUPER_USER:
    df_review = review_table(db)
    st.header("Reviews")
    st.dataframe(df_review)
elif button and input_text != "":
    try:
        OPENAI_API_KEY = st.session_state.get("OPENAI_API_KEY")
        with st.spinner("Wait for it ... Meow"):
            st.session_state["button"] = True
            col_pic_left, col_disease, col_pic_right = st.columns([0.5, 1, 0.5])
            with col_pic_left:
                image = Image.open("pic/cover_left.jpg")
                st.image(image)
            with col_pic_right:
                image = Image.open("pic/cover_right.jpg")
                st.image(image)
            with col_disease:
                layer_1_result = layer_1(
                    input_text,
                    openai_api_key=OPENAI_API_KEY,
                    response_schemas=response_schemas_layer_1,
                    system_message=system_message_layer_1,
                    human_message=human_message_layer_1,
                )
                st.subheader(
                    f"Most Possible Disease: :red[{layer_1_result['Possible disease:']}]"
                )
            if layer_1_result["Possible disease:"] not in refine_target:
                layer_2_result = non_refine_target(
                    disease_input=layer_1_result["Possible disease:"],
                    openai_api_key=OPENAI_API_KEY,
                    response_schemas=response_schemas_layer_2,
                    system_message=system_message_layer_1,
                    human_message=human_message_non_refine,
                )
            else:
                docs = get_similarity_search_from_pinecone(
                    PINECONE_INDEX_NAME,
                    layer_1_result["Possible disease:"],
                    openai_api_key=OPENAI_API_KEY,
                )
                query = (
                    input_text
                    + ", what's the possible diseases and dietary suggestions?"
                )
                layer_2_result = layer_2(
                    docs=docs,
                    query=query,
                    openai_api_key=OPENAI_API_KEY,
                    layer_1_suggestions=layer_1_result["Dietary suggestions"],
                    response_schemas=response_schemas_layer_2,
                    refine_prompt_template=refine_prompt_template,
                    initial_qa_template=initial_qa_template,
                )
            _, col_description, _ = st.columns([0.15, 1, 0.15])
            with col_description:
                with st.expander("Disease Description", expanded=True):
                    st.markdown(f"**{layer_2_result['Disease description']}**")
            tab1, tab2, tab3 = st.tabs(
                ["Dietary Suggestions", "Food Suggestions", "Nutrients Suggestions"]
            )
            with tab1:
                tab1_pic_choice = [
                    "pic/sushi-cats-1.jpeg",
                    "pic/sushi-cats-2.jpeg",
                    "pic/sushi-cats-3.jpeg",
                    "pic/sushi-cats-4.jpeg",
                    "pic/sushi-cats-5.jpeg",
                    "pic/sushi-cats-6.jpeg",
                    "pic/sushi-cats-7.jpeg",
                    "pic/sushi-cats-8.jpeg",
                    "pic/sushi-cats-9.jpeg",
                ]
                st.subheader("Dietary Suggestions:")
                st.markdown(f"**{layer_2_result['Dietary advices']}**")
                tab1_pic = np.random.choice(tab1_pic_choice)
                image = Image.open(tab1_pic)
                st.image(image)
            df_catfood, df_nutrients = create_df_food_nutrient(db)
            with tab2:
                st.subheader("Food Suggestions:")
                catfood_categories = [
                    "Protein",
                    "Fat",
                    "Carbs",
                    "Fiber",
                    "Moisture",
                ]
                nutrient_list = [
                    [k, v] for k, v in layer_2_result.items() if k in catfood_categories
                ]
                filtered_food_df = get_CatFood(
                    df=df_catfood, nutrient_list=nutrient_list, top=2
                )
                for idx, series in filtered_food_df.iterrows():
                    st.subheader(f":blue[Brand Name]: {series['name']}")
                    st.markdown(f":blue[Reviews]: {series['pros_cons']}")
                    st.markdown(
                        f"**:blue[Potential Allergens]: {series['Potential_Allergens']}**"
                    )
                    with st.expander("Ingredients"):
                        st.markdown(
                            f"**:blue[Ingredients]: {series['Ingredient_details']}**"
                        )
                    col_link, col_pic = st.columns([1, 1])
                    with col_link:
                        st.markdown(f"**:blue[Chewy Link]: {series['url']}**")
                    with col_pic:
                        image = Image.open("pic/" + series["pic"])
                        st.image(image)
            with tab3:
                st.subheader("Nutrients Suggestions:")
                nutrients = layer_2_result["Minerals, vitamins and supplements"].split(
                    ","
                )
                nutrients = list({nutrient.strip() for nutrient in nutrients})
                if layer_2_result["Minerals, vitamins and supplements"] == "None":
                    website = f"https://www.chewy.com/s?query=cat+vitamin&rh=c%3A417"
                    series_nutrient = df_nutrients[
                        df_nutrients["Nutrients"] == "Vitamins B"
                    ]
                    for idx, series in series_nutrient.iterrows():
                        st.subheader(f"**:blue[{series['Nutrients']}]**")
                        with st.expander("Details"):
                            st.markdown(f"**{series['Information']}**")
                        st.markdown(f"**:blue[Chewy Link]: {website}**")
                else:
                    for nutrient in nutrients:
                        if nutrient in df_nutrients["Nutrients"].tolist():
                            word = (nutrient + " for cats").split()
                            word = [i.strip() for i in word]
                            join_words = "%20".join(word)
                            series_nutrient = df_nutrients[
                                df_nutrients["Nutrients"] == nutrient.strip()
                            ]
                            for idx, series in series_nutrient.iterrows():
                                website = f"https://www.chewy.com/s?query={join_words}&nav-submit-button="
                                st.subheader(f"**:blue[{series['Nutrients']}]**")
                                with st.expander("Details"):
                                    st.markdown(f"**{series['Information']}**")
                                st.markdown(f"**:blue[Chewy Link]: {website}**")
        rain(
            emoji="🐈",
            font_size=54,
            falling_speed=5,
            animation_length=2,
        )
    except ValidationError as e:
        st.error("Please configure your OpenAI API key!")
    except AuthenticationError as e:
        st.error("Please configure your OpenAI API key!")
else:
    st.subheader(f"Please type in your cat's symptoms!")

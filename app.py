import streamlit as st
import os
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

# -------------------------
# App Title + Logo
# -------------------------

st.title("🍽️ Surprise Me with a Recipe!")

# Local logo
st.image("logo.png", width=200, caption="Shraddha's AI Chef")

# -------------------------
# LangGraph Setup
# -------------------------

class RecipeState:
    def __init__(self, cuisine: str, ingredients: str, recipe: str = None):
        self.cuisine = cuisine
        self.ingredients = ingredients
        self.recipe = recipe

def generate_recipe(state: RecipeState) -> RecipeState:
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.7,
        api_key=os.environ["OPENAI_API_KEY"]
    )

    prompt = f"""
    You are a creative chef.

    Cuisine: {state.cuisine}
    Available ingredients: {state.ingredients}

    Suggest a recipe from this cuisine that can be prepared using these ingredients. 
    Provide:
    - Recipe name
    - Ingredients list
    - Step-by-step instructions

    Surprise me with something unique!
    """

    result = llm.invoke(prompt).content.strip()
    state.recipe = result
    return state

graph = StateGraph(RecipeState)
graph.add_node("generate_recipe", generate_recipe)
graph.set_entry_point("generate_recipe")
graph.add_edge("generate_recipe", END)

runnable = graph.compile()

# -------------------------
# Streamlit UI
# -------------------------

cuisine = st.text_input("Which cuisine do you feel like eating?")
ingredients = st.text_area("What ingredients do you have? (comma separated)")

if st.button("Surprise Me!"):
    with st.spinner("Cooking up a recipe..."):
        state = RecipeState(cuisine=cuisine, ingredients=ingredients)
        result = runnable.invoke(state)
        st.markdown(
            "<h2 style='color:#E56B6F;'>Here's your recipe!</h2>",
            unsafe_allow_html=True
        )
        st.markdown(result.recipe)

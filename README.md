<h1 align="center">
  🐈 Cat Disease GPT
</h1>

Answer possible disease and give dietary suggestions, recommend cat food and supplements for your cat.

## 🔧 Features

- Input symptoms and diagnose the most possible disease with dietary suggestions.
- Based on the answer above, recommed cat food and supplments that best fit the dietary suggestions.

## 💻 Approaches

- Gathered cat food and nutrient details by utilizing scraping tools.
- Cleaned and processed cat food and nutrient data and stored it in a Google Firestore database.
- Employed LangChain ChatOpenAI chat model with output parser to deliver structured basic results.
- Embedded and stored cat disease papers into the vector database pinecone and performed similarity search to retrieve the most relevant paper.
- Implemented LangChain load_qa_chain model with output parser and refined it using the first basic results and the relevant paper from the similarity search.
- Match the best cat food and nutrient with LangChain result.
- Deployed the project on Streamlit.

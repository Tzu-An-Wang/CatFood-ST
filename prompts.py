from langchain.output_parsers import ResponseSchema

# for layer 1
response_schemas_layer_1 = [
    ResponseSchema(
        name="Possible disease:", description="analyze the most possible diseases."
    ),
    ResponseSchema(
        name="Dietary suggestions",
        description="Give diet suggestions of the most possible diseases in one sentence less than 20 words.",
    ),
]

system_message_layer_1 = (
    "You are a experienced vet and animal nutritionist specialized in cat field."
)
human_message_layer_1 = "Use the symptoms to provide only the most possible disease and give dietary suggestions. The most possible disease should \
                be one of the followings: Hepatic Lipidosis, Lower Urinary Tract Diseases/Feline Interstitial Cystitis, Chronic Kidney Disease,\
                Diabetes, Pancreatitis, Inflammatory Bowel Disease(IBD) and Hyperthyroidism. If it's not one the above diseases, name it into  \
                others. Also for Dietary suggestion, make it less than 40 words.\n{format_instructions}\n{symptoms}"

human_message_non_refine = "Use the disease to provide Dietary advices, Protein, Fat, Carbs, Fiber, Ash, Moisture, Minerals, vitamins and supplements, Disease description.\n{format_instructions}\n{Disease}"


# for layer 2:
response_schemas_layer_2 = [
    ResponseSchema(name="Disease", description="reply the most possible disease"),
    ResponseSchema(
        name="Dietary advices",
        description="Based on refined answer, summarize in less than 50 words",
    ),  # Each dietary suggestion should be in one sentence and )
    ResponseSchema(
        name="Protein",
        description="if there's no suggestions, reply none, else reply only High, Moderate or Low.",
    ),
    ResponseSchema(
        name="Fat",
        description="if there's no suggestions, reply none, else reply only High, Moderate or Low.",
    ),
    ResponseSchema(
        name="Carbs",
        description="if there's no suggestions, reply none, else reply only High, Moderate or Low.",
    ),
    ResponseSchema(
        name="Fiber",
        description="if there's no suggestions, reply none, else reply only High, Moderate or Low.",
    ),
    ResponseSchema(
        name="Ash",
        description="if there's no suggestions, reply none, else reply only High, Moderate or Low.",
    ),
    ResponseSchema(
        name="Moisture",
        description="if there's no suggestions, reply none, else reply only High, Moderate or Low.",
    ),
    ResponseSchema(
        name="Minerals, vitamins and supplements",
        description="if there's no suggestions, reply none, else reply only the exact names in one of the following items: Taurine, Arginine, Vitamin A, Vitamin D, Vitamins B, Omega-3",
    ),
    ResponseSchema(
        name="Disease description",
        description="summary the disease discription in 50 words",
    ),
]

refine_prompt_template = (
    "The original question is as follows: {question}\n"
    "We have provided an existing answer: {existing_answer}\n"
    "We have the opportunity to refine the existing answer"
    "(only if needed) with some more context below.\n"
    "------------\n"
    "{context_str}\n"
    "------------\n"
    "You are a professional vet and nutritionist specialized in cat."
    "Given the new context, refine the original answer to better, "
    "add minerals, vitamins and supplements if the original answer is missing it,"
    "answer the question."
)

initial_qa_template = (
    "Context information is below. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "I already have a existing answer {existing_answer}"
    "You are a professional vet and nutritionist specialized in cat."
    "If the existing answer is one of the possible disease, focus on that disease and give Dietary suggestions."
    "Possible disease should be in one of the following categories :Hepatic Lipidosis, Lower Urinary Tract Diseases/Feline Interstitial Cystitis, \
        Chronic Kidney Disease, Diabetes, Pancreatitis, Inflammatory Bowel Disease(IBD),Hyperthyroidism, others."
    "Add specific minerals, vitamins and supplements if it's not in the Dietary suggestions"
    "Summarize Dietary suggestions to less than 100 words.\n{format_instructions_layer_2}"
)

from langchain.prompts import ChatPromptTemplate, PromptTemplate, HumanMessagePromptTemplate

# Define the modified prompt template
basis_prompt = ChatPromptTemplate(
    input_variables=['context', 'question'],
    metadata={
        'lc_hub_owner': 'rlm',
        'lc_hub_repo': 'rag-prompt',
        'lc_hub_commit_hash': '50442af133e61576e74536c6556cefe1fac147cad032f4377b60c436e6cdcb6e'
    },
    messages=[
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=['context', 'question'],
                template=(
                    "You are an assistant for question-answering tasks. Use ONLY the following pieces of retrieved context to answer the question. "
                    "Do not use any external information or prior knowledge. If you don't know the answer based on the provided context, just say that you don't know. "
                    "Answer in up to five sentences maximum, staying concise. However, if the user explicitly asks for a detailed or exhaustive answer, provide a more thorough response while still focusing solely on the context.\n"
                    "Question: {question} \nContext: {context} \nAnswer:"
                )
            )
        )
    ]
)

basis_prompt_2 = ChatPromptTemplate(
    input_variables=['context', 'question'],
    metadata={
        'lc_hub_owner': 'rlm',
        'lc_hub_repo': 'rag-prompt',
        'lc_hub_commit_hash': '50442af133e61576e74536c6556cefe1fac147cad032f4377b60c436e6cdcb6e'
    },
    messages=[
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=['context', 'question'],
                template=(
                    "You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. "
                    "Do not use any external information or prior knowledge. If you don't know the answer based on the provided context, just say that you don't know. "
                    "Answer in up to five sentences maximum, staying concise. However, if the user explicitly asks for a detailed or exhaustive answer, provide a more thorough response while still focusing solely on the context.\n"
                    "Question: {question} \nContext: {context} \nAnswer:"
                )
            )
        )
    ]
)

test_prompt =  ChatPromptTemplate( # For debugging purposes
    input_variables=['context', 'question'],
    metadata={
        'lc_hub_owner': 'rlm',
        'lc_hub_repo': 'rag-prompt',
        'lc_hub_commit_hash': '50442af133e61576e74536c6556cefe1fac147cad032f4377b60c436e6cdcb6e'
    },
    messages=[
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=['context', 'question'],
                template=(
                    "You are an assistant, answer the questions. Question: {question} \nContext: {context} \nAnswer:"
                )
            )
        )
    ]
)
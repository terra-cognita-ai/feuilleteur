import os

import pytest
import openai
from dotenv import load_dotenv, find_dotenv
from loguru import logger

from backend.src.rag import answer_question, load_and_process_epub, split_documents_with_positions, vectorize_documents

load_dotenv(find_dotenv())
openai.api_key = os.environ.get("OPENAI_API_KEY")


@pytest.fixture
def setup_environment():
    file_path = "data/dumas_monte_cristo_1.epub"
    TEST_VECTORS_FOLDER = "tests/data/session/vectors"
    os.makedirs(TEST_VECTORS_FOLDER, exist_ok=True)

    return file_path, TEST_VECTORS_FOLDER


def test_rag_with_low_percentage(setup_environment):
    """Test the RAG system with a very low percentage of the document (1%)."""
    file_path, TEST_VECTORS_FOLDER = setup_environment
    question = "Quelle est la particularité du cimetière du château d'If ?"
    expected_response = ("Désolé, je ne sais pas. Le contexte fourni ne donne pas d'information sur la "
                         "particularité du cimetière du château d'If.")  # Expected answer for 1% of the document

    # Use the helper function to run the test
    run_rag_test(file_path, TEST_VECTORS_FOLDER, question, expected_response, percentage=1, similarity_threshold=0.1, mode="below")


def test_rag_with_high_percentage(setup_environment):
    """Test the RAG system with a higher percentage of the document (50%)."""
    file_path, TEST_VECTORS_FOLDER = setup_environment
    question = "Quelle est la particularité du cimetière du château d'If ?"
    expected_response = ("La particularité du cimetière du château d'If est qu'il n'existe pas. Les corps sont "
                         "directement jetés à la mer.")

    # Use the helper function to run the test
    run_rag_test(file_path, TEST_VECTORS_FOLDER, question, expected_response, percentage=100, similarity_threshold=0.8, mode="above")


def run_rag_test(file_path, test_vector_folder, question, expected_response, percentage, similarity_threshold, mode="above"):
    """Helper function to run the RAG test with LLM-based similarity check."""

    result = load_and_process_epub(file_path, percentage=percentage)
    splits = split_documents_with_positions(result)
    vectorize_documents(splits,test_vector_folder) #TODO: When the percentage will be managed at the retrieval level, this will be moved to fixture as it will be common to all tests

    # Run the RAG system
    answer, _ = answer_question(test_vector_folder, question)
    logger.info(f"Answer:\n{answer}")
    # Use LLM to check similarity
    similarity_score = get_similarity(answer, expected_response)

    if mode == "above":
        # Assert the similarity score is above the threshold
        assert similarity_score > similarity_threshold, f"Low similarity score: {similarity_score} for percentage: {percentage}"
    else:
        # Assert the similarity score is below the threshold
        assert similarity_score < similarity_threshold, f"High similarity score: {similarity_score} for percentage: {percentage}"


def get_similarity(answer, ground_truth):
    """Use the new OpenAI API to check the similarity between the answer and ground truth."""
    response = openai.chat.completions.create(
        model="gpt-4",  # or "gpt-3.5-turbo", depending on your preference
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Rate the similarity between the following two texts on a scale from 0 to 1:\n\nText 1: {answer}\nText 2: {ground_truth}\n\nScore:"}
        ],
    )
    similarity_score = float(response.choices[0].message.content.strip())
    return similarity_score
import argparse

from loguru import logger

from backend.src.rag import answer_question
def main():
    """Main function for command-line execution."""
    parser = argparse.ArgumentParser(description="Process an EPUB file and ask questions without spoilers.")
    parser.add_argument(
        '--file-path',
        type=str,
        default="data/dumas_monte_cristo_1.epub",
        help="Path to the book to analyse"
    )
    parser.add_argument(
        '--percentage',
        type=int,
        default=10,
        help="Percentage of the book to process (default: 10%)"
    )
    parser.add_argument(
        '--question',
        type=str,
        required=True,
        help="The question you want to ask about the book"
    )
    args = parser.parse_args()

    answer = answer_question(args.file_path, args.percentage, args.question)
    logger.info(f"Answer:\n{answer}")


if __name__ == "__main__":
    main()
<script lang="ts">
	import { onMount } from "svelte";
    import { RequestStatus, type QuestionRequest } from "./types";

    let books: string[] = [];

    onMount(getBooks);


    let question: QuestionRequest = {
        question: "",
        book: "",
        percentage: 100,
        answer: {
            text: "",
            documents: [],
            status: RequestStatus.idle
        }
    }

    async function postQuestion() {
        try {
            question.answer = {
                text: "",
                documents: [],
                status: RequestStatus.processing
            }

            const response = await fetch('ask-question', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(question)
            });

            const data = await response.json();

            if (response.ok) {
                question.answer.text = data.answer;
                question.answer.documents = data.documents;
                question.answer.status = data.status;
            }
            else {
                question.answer.status = data.error;
            }

        } catch (error) {
            question.answer.status = RequestStatus.error;
        }
    }

    async function getBooks() {
        try {
            const response = await fetch('books', {
                method: 'GET'
            });

            const data = await response.json();

            if (response.ok) {
                if (data.books?.length > 0) books = data.books;
            }
        } catch (error) {
            console.error('Fetch error:', error);
        }
    }
</script>

{#if books.length > 0}
    <section id="questions-form">
        <article>
            <h4>Ask Questions</h4>
            <hr>
            <form>
                <label for="book">
                    Book
                    <select name="book" aria-label="Select" required bind:value={question.book}>
                        <option selected disabled value="">Select a book</option>
                        {#each books as book}
                        <option value={book}>
                            {book}
                        </option>
                        {/each}
                    </select>
                </label>
                <label for="percentage">
                    Percentage
                    <input type="number" name="percentage" placeholder="Percentage" aria-label="Percentage" bind:value={question.percentage} min="0" max="100">
                </label>
                <label for="question">
                    Question
                <input type="search" name="question" placeholder="Your Question" aria-label="Search" bind:value={question.question} />
                </label>
                <button aria-busy={question.answer.status == RequestStatus.processing} on:click={postQuestion} class="full-width">
                    {question.answer.status == RequestStatus.processing ? "Processing" : "Ask Question"}
                </button>
            </form>
            {#if question.answer.status == RequestStatus.ok}
                <blockquote>
                    {question.answer.text}
                </blockquote>
                {#each question.answer.documents as document}
                <details>
                    <summary>
                        {document.position}
                    </summary>
                    <blockquote>
                        {document.content}
                    </blockquote>
                </details>
                {/each}
            {:else if question.answer.status != RequestStatus.idle}
                <span>
                    {question.answer.status}
                </span>
            {/if}
        </article>
    </section>
{/if}

<style>
    .full-width {
        width: 100%;
    }
</style>
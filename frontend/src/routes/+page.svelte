<script lang="ts">
	import { onMount } from "svelte";
    let books: string[] = [];
    let status = "";

    onMount(fetchBooks);

    type QuestionRequest = {
        question: string;
        book: string;
        percentage: number;
    }

    let question: QuestionRequest = {
        question: "",
        book: "",
        percentage: 100
    }

    type Passage = {
        content: string,
        position: string
    }

    type Answer = {
        text: string,
        documents: Passage[],
        status: string
    }

    let answer: Answer = {
        text: "",
        documents: [],
        status: ""
    }

    async function postQuestion() {
        try {
            answer = {
                text: "",
                documents: [],
                status: "processing"
            }

            const response = await fetch('ask-question', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(question)
            });

            const data = await response.json();

            if (response.ok) {
                answer.text = data.answer;
                answer.documents = data.documents;
                answer.status = data.status;
            }
            else {
                answer.status = data.error;
            }

        } catch (error) {
            answer.status = error;
        }
    }

    async function postBook() {
        const fileInput = document.getElementById('file') as HTMLInputElement;
        const formData = new FormData();
        if (fileInput.files) formData.append('file', fileInput.files[0]);
        try {
            const response = await fetch('upload-file', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            if (response.ok) {
                await fetchBooks();
            } else {
                console.error('Fetch error:', data.error);
            }
        } catch (error) {
            console.error('Fetch error:', error);
        }
    }

    async function fetchBooks() {
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

    async function fetchStatus() {
        const response = await fetch('status', {
            method: 'GET'
        });
        const data = await response.json();
        if (response.ok && data.status) return data.status;
        else throw new Error(response.statusText);
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
                <button aria-busy={answer.status == "processing"} on:click={postQuestion}>
                    {answer.status == "processing" ? "Processing" : "Ask Question"}
                </button>
            </form>
            {#if answer.status == "ok"}
                <blockquote>
                    {answer.text}
                </blockquote>
                {#each answer.documents as document}
                <details>
                    <summary>
                        {document.position}
                    </summary>
                    <blockquote>
                        {document.content}
                    </blockquote>
                </details>
                {/each}
            {:else if answer.status != ""}
                <span>
                    {answer.status}
                </span>
            {/if}
        </article>
    </section>
{/if}

<section id="upload-form">
	<article>
        <h4>Import Books</h4>
        <hr>
        {#await fetchStatus()}
            <span aria-busy="true">Checking server status...</span>
        {:then status} 
            <form>
                <input type="file" id="file" name="file" accept=".epub"/>
                <input type="submit" value="Import" on:click={postBook} />
            </form>
        {:catch error}
            <span>
                Server unavailable: "{error.message}"
            </span>
        {/await}
    </article>
</section>
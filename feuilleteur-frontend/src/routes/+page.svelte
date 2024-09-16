<script lang="ts">
	import { onMount } from "svelte";
    let books: string[] = [];

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
        documents: Passage[]
    }

    let answer: Answer = {
        text: "",
        documents: []
    }

    async function postQuestion() {
        try {
            console.log(question)
            const response = await fetch('http://127.0.0.1:8890/ask-question', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(question)
            });

            const data = await response.json();

            if (response.ok) {
                answer.text = data.answer;
                answer.documents = data.documents;
            }
            else {
                console.error(data.error);
            }

        } catch (error) {
            console.error('Fetch error:', error);
        }
    }

    async function postBook() {
        const fileInput = document.getElementById('file') as HTMLInputElement;
        const formData = new FormData();
        if (fileInput.files) formData.append('file', fileInput.files[0]);
        try {
            const response = await fetch('http://127.0.0.1:8890/upload-file', {
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
            const response = await fetch('http://127.0.0.1:8890/books', {
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
                <select name="select" aria-label="Select" required bind:value={question.book}>
                    <option selected disabled value="">Select a book</option>
                    {#each books as book}
                    <option value={book}>
                        {book}
                    </option>
                    {/each}
                </select>
                <label for="percentage">
                    Percentage
                    <input type="number" name="percentage" placeholder="Percentage" aria-label="Percentage" bind:value={question.percentage} min="0" max="100">
                </label>
                <input type="search" name="search" placeholder="Your Question" aria-label="Search" bind:value={question.question} />
                <input type="submit" value="Submit" on:click={postQuestion}/>
            </form>
            {#if answer.text}
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
            {/if}
        </article>
    </section>
{/if}

<section id="upload-form">
	<article>
        <h4>Import Books</h4>
        <hr>
        <form>
            <input type="file" id="file" name="file" accept=".epub"/>
            <input type="submit" value="Import" on:click={postBook} />
        </form>
	</article>
</section>
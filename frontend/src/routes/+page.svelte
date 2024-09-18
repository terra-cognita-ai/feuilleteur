<script lang="ts">
    import { onMount } from "svelte";
	import QuestionForm from "$lib/QuestionForm.svelte";
	import SearchForm from "$lib/SearchForm.svelte";
	import UploadForm from "$lib/UploadForm.svelte";

    let books: string[] = [];

    onMount(getBooks);

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

<QuestionForm books={books}></QuestionForm>

<SearchForm on:new-book={getBooks}></SearchForm>

<UploadForm on:new-book={getBooks}></UploadForm>
<script lang="ts">
    import { onMount } from "svelte";
	import QuestionForm from "$lib/QuestionForm.svelte";
	import SearchForm from "$lib/SearchForm.svelte";
	import UploadForm from "$lib/UploadForm.svelte";
    import { BackendService } from "../client";

    let books: string[] = [];

    onMount(getBooks);

    async function getBooks() {
        try {
            const response = await BackendService.getBooks();
            if (response.data && response.data.length > 0) {
                books = response.data;
            }
            else {
                console.error('No books found:', response.error);
            }
        } catch (error) {
            console.error('Fetch error:', error);
        }
    }
</script>

<QuestionForm books={books}></QuestionForm>

<SearchForm on:new-book={getBooks}></SearchForm>

<UploadForm on:new-book={getBooks}></UploadForm>
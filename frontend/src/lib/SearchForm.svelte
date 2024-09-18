<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import BookCard from "./BookCard.svelte";
	import ErrorMessage from "./ErrorMessage.svelte";
    import { type Book, type ImportRequest, type SearchRequest } from "./types";

    const dispatch = createEventDispatcher();

    let searchRequest: SearchRequest = {
        search: "",
        status: "idle",
        results: []
    };

    let importRequest: ImportRequest = {
        status: "idle",
        error: ""
    };

    async function searchBook() {
        searchRequest.status = "processing";
        importRequest.status = "idle";
        importRequest.error = "";
        searchRequest.results = [];
        const searchURL = 'https://gutendex.com/books?search=' + searchRequest.search.replaceAll(" ", "%20");
        const response = await fetch(searchURL, {
            method: 'GET'
        });
        const data = await response.json();
        if (response.ok && data.results.length > 0) {
            searchRequest.results = data.results;
            searchRequest.status = "ok";
        }
        else throw new Error(response.statusText);
    }

    async function importBook(book: Book) {
        importRequest.status = "processing";
        importRequest.error = "";
        searchRequest.results = [book];
        const response = await fetch('import-book', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(book)
        });

        const data = await response.json();

        if (response.ok) {
            importRequest.status = "ok";
            setTimeout(()=>{searchRequest.results = []}, 3000);
            dispatch("new-book");
        }
        else {
            importRequest.status = "error";
            importRequest.error = data ? JSON.stringify(data) : response.statusText; 
        }
    }
</script>

<section id="search-form">
    <article>
        <h4>Search Public Domain Books</h4>
        <hr>
        <form>
            <input type="search" name="search" placeholder="Search Book" aria-label="Search" bind:value={searchRequest.search} />
            <button aria-busy={searchRequest.status == "processing"} on:click={searchBook} class="full-width">
                {searchRequest.status == "processing" ? "Processing" : "Search"}
            </button>
        </form>
        <div class="grid overflow-auto">
            {#each searchRequest.results as book}
                <BookCard book={book}>
                    <button aria-busy={importRequest.status == "processing"} on:click={()=>importBook(book)} class="full-width">
                        {#if importRequest.status == "idle"}
                            Import 
                        {:else if importRequest.status == "processing"}
                            Processing
                        {:else if importRequest.status == "ok"}
                            Success !
                        {:else}
                            Error
                        {/if}
                    </button>
                </BookCard>
            {/each}
        </div>
        <ErrorMessage message={importRequest.error}></ErrorMessage>
    </article>
</section>

<style>
    .full-width {
        width: 100%;
    }
    .grid {
        grid-template-columns: repeat(4, 1fr);
        /* grid-gap: 10px;
        grid-auto-rows: minmax(100px, auto); */
    }
    @media only screen and (max-width: 1280px) {
        .grid {
            grid-template-columns: repeat(3, 1fr);
        }
    }
    @media only screen and (max-width: 1024px) {
        .grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    @media only screen and (max-width: 480px) {
        .grid {
            grid-template-columns: repeat(1, 1fr);
        }
    }
</style>
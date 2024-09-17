<script lang="ts">
    import { type Book, type ImportRequest, type SearchRequest } from "./types";

    let searchRequest: SearchRequest = {
        search: "",
        status: "idle",
        results: []
    };

    let importRequest: ImportRequest = {
        status: "idle"
    };

    async function searchBook() {
        searchRequest.status = "processing";
        importRequest.status = "idle";
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
        searchRequest.results = [book];
        const response = await fetch('import-book', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(book)
        });

        const data = await response.json();

        if (response.ok) {
            importRequest.status = "ok";
        }
        else {
            importRequest.status = "error";
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
        <div>
            {#each searchRequest.results as book}
                <article>
                    <div class="grid">
                        <div>
                            <img
                            src={book.formats["image/jpeg"]}
                            alt={book.title}
                            />
                        </div>
                        <div>
                            <hgroup>
                                <h5>{book.title}</h5>
                                <span>{book.authors[0].name}</span>
                            </hgroup>
                            <button aria-busy={importRequest.status == "processing"} on:click={()=>importBook(book)} class="full-width">
                                {importRequest.status == "processing" ? "Processing" : "Import"}
                            </button>
                        </div>
                    </div>
                </article>
            {/each}
        </div>
    </article>
</section>

<style>
    .full-width {
        width: 100%;
    }
</style>
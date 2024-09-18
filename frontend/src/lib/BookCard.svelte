<script lang="ts">
    import type { Book } from "./types";
    export let book: Book;
</script>

<article class="flex">
    <figure class="full-width flex-grow">
        {#if book.formats["image/jpeg"]}
        <img
        class="full-width"
        src={book.formats["image/jpeg"]}
        alt={book.title}
        />
        {/if}
    </figure>
    <div>
        <hgroup>
            <h5 class="text">{book.title}</h5>
            {#if book.authors.length > 0}
                <p class="text">{book.authors.map((b)=>b.name).reduce((a, b) => a + ', ' + b)}</p>
            {/if}
            {#if book.languages.length > 0}
                <p>Language : {book.languages.reduce((a, b) => a + ', ' + b)}</p>
            {/if}
        </hgroup>
    </div>
    <div class="end full-width">
        <slot></slot>
    </div>
</article>

<style>
    .full-width {
        width: 100%;
    }
    .flex {
        display: flex;
        flex-direction: column;
        /* align-self: end; */
        align-content: end;
        height: 100%;
    }
    .flex-grow {
        flex-grow: 1;
        align-content: center;
    }
    .end {
        align-self: flex-end;
    }
    .text{
        text-overflow: ellipsis;
        cursor: pointer;          
        /* word-break: break-all; */
        overflow:hidden;         
        white-space: nowrap;
    }
    .text:hover{
        overflow: visible;        
        white-space: normal;
        /* height:auto; */
    }
</style>
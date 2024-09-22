<script lang="ts">
    import type { QuestionAnswer } from "./types";
    export let answer: QuestionAnswer;
</script>


{#if answer.status == "ok"}
    <article>
        <h4>Answer</h4>
        <hr>
        <blockquote>
            <cite>{answer.text}</cite>
        </blockquote>
        {#each answer.documents as document, i}
        <details>
            <summary>
                {"Source " + String(i+1) + " : " + document.position}
            </summary>
            <blockquote>
                {document.content}
            </blockquote>
        </details>
        {/each}
    </article>
{/if}
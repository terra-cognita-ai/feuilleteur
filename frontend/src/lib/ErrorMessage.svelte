<script lang="ts">
    export let message = "";
</script>

{#if message}
<mark>
    {message.replaceAll("\\n", " ")}
</mark>
{/if}
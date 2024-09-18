<script lang="ts">
    export let message = "";
</script>

{#if message}
<mark>
    {message}
</mark>
{/if}
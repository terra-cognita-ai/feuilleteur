<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    import type { ImportRequest } from './types';
	import ErrorMessage from "./ErrorMessage.svelte";

    const dispatch = createEventDispatcher();

    let importRequest: ImportRequest = {
        status: "idle",
        error: ""
    };

    async function postBook() {
        importRequest.status = "processing";
        importRequest.error = "";
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
                importRequest.status = "ok";
                dispatch("new-book");
            }
            else {
                importRequest.error = data ? JSON.stringify(data) : response.statusText;
            }
        } 
        catch (error) {
            importRequest.error = String(error);
        }
    }

    async function getStatus() {
        const response = await fetch('status', {
            method: 'GET'
        });
        const data = await response.json();
        if (response.ok && data.status) return data.status;
        else throw new Error(response.statusText);
    }
</script>

<section id="upload-form">
	<article>
        <h4>Import Epub Files</h4>
        <hr>
        {#await getStatus()}
            <span aria-busy="true">Checking server status...</span>
        {:then status} 
            <form>
                <input type="file" id="file" name="file" accept=".epub"/>
                <button aria-busy={importRequest.status == "processing"} on:click={postBook} class="full-width">
                    {#if importRequest.status == "idle"}
                        Upload
                    {:else if importRequest.status == "processing"}
                        Processing
                    {:else if importRequest.status == "ok"}
                        Success !
                    {:else}
                        Error
                    {/if}
                </button>
            </form>
        {:catch error}
            <span>
                Server unavailable: "{error.message}"
            </span>
        {/await}
        <ErrorMessage message={importRequest.error}></ErrorMessage>
    </article>
</section>


<style>
    .full-width {
        width: 100%;
    }
</style>
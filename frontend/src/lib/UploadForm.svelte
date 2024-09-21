<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    import type { ImportRequest } from './types';
	import ErrorMessage from "./ErrorMessage.svelte";
	import { BackendService } from '../client';

    const dispatch = createEventDispatcher();

    let importRequest: ImportRequest = {
        status: "idle",
        error: ""
    };

    async function postBook() {
        const fileInput = document.getElementById('file') as HTMLInputElement;
        if (fileInput.files) {
            importRequest.status = "processing";
            importRequest.error = "";
            try {
                const response = await BackendService.uploadFile({body:{file:fileInput.files[0]}});
                if (response.response.ok) {
                    importRequest.status = "ok";
                    dispatch("new-book");
                }
                else {
                    importRequest.error = String(response.error);
                }
            } 
            catch (error) {
                importRequest.error = String(error);
            }
        }
    }

    async function getStatus() {
        const response = await BackendService.getStatus();
        if (response.response.ok) return response.data;
        else throw new Error(response.response.statusText);
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
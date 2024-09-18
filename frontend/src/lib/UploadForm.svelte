<script lang="ts">
	import ErrorMessage from "./ErrorMessage.svelte";

    let errorMessage = "";

    async function postBook() {
        errorMessage = "";
        const fileInput = document.getElementById('file') as HTMLInputElement;
        const formData = new FormData();
        if (fileInput.files) formData.append('file', fileInput.files[0]);
        try {
            const response = await fetch('upload-file', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            errorMessage = data ? JSON.stringify(data) : response.statusText;
        } 
        catch (error) {
            errorMessage = String(error);
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
                <input type="submit" value="Import" on:click={postBook} />
            </form>
        {:catch error}
            <span>
                Server unavailable: "{error.message}"
            </span>
        {/await}
        <ErrorMessage message={errorMessage}></ErrorMessage>
    </article>
</section>
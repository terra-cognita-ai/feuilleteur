import { defineConfig } from 'vite';
import { sveltekit } from '@sveltejs/kit/vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		proxy: {
		  '/books': 'http://127.0.0.1:8000',
		  '/ask-question': 'http://127.0.0.1:8000',
		  '/upload-file': 'http://127.0.0.1:8000',
		  '/status': 'http://127.0.0.1:8000',
		  '/import-book': 'http://127.0.0.1:8000',
		  '/cover': 'http://127.0.0.1:8000',
		}
	  }
});

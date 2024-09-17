import { defineConfig } from 'vite';
import { sveltekit } from '@sveltejs/kit/vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		proxy: {
		  '/books': 'http://127.0.0.1:8890',
		  '/ask-question': 'http://127.0.0.1:8890',
		  '/upload-file': 'http://127.0.0.1:8890',
		  '/status': 'http://127.0.0.1:8890',
		  '/import-book': 'http://127.0.0.1:8890',
		}
	  }
});

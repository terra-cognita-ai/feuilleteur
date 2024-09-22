import { defineConfig } from '@hey-api/openapi-ts';

export default defineConfig({
  client: '@hey-api/client-fetch',
  input: 'http://localhost:8000/openapi.json',
  output: 'src/client',
  services: {
    asClass: true,
    name: 'BackendService',
    operationId: false,
    methodNameBuilder: (operation) => (operation.summary ?? operation.path).split(' ').map((e,i) => i ? e.charAt(0).toUpperCase() + e.slice(1).toLowerCase() : e.toLowerCase()).join('')
  },
});
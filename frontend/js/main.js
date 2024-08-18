// Upload Form Submission
document.getElementById('uploadForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    console.log('Upload form submitted');  // Debugging statement

    const fileInput = document.getElementById('file');
    const loadingElement = document.getElementById('uploadLoading');
    const uploadResultElement = document.getElementById('uploadResult');
    const questionContainer = document.getElementById('questionContainer');

    // Show the uploading message
    loadingElement.style.display = 'block';
    uploadResultElement.innerText = '';

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('http://127.0.0.1:8890/upload-file', {
            method: 'POST',
            body: formData
        });

        console.log('Response received');  // Debugging statement

        const data = await response.json();

        // Hide the uploading message
        loadingElement.style.display = 'none';

        if (response.ok) {
            console.log('File uploaded successfully');  // Debugging statement
            uploadResultElement.innerText = data.message ? data.message : "File uploaded.";
            questionContainer.style.display = 'block';

            if (data.cover_image_url) {
                const coverImageElement = document.getElementById('coverImage');
                coverImageElement.src = `http://127.0.0.1:8890${data.cover_image_url}`;
                coverImageElement.style.display = 'block';
            }

            // Scroll to the top of the first container after upload
            document.querySelector('.container').scrollIntoView({ behavior: 'smooth', block: 'start' });
        } else {
            uploadResultElement.innerText = data.error ? data.error : "An error occurred.";
            console.error('Error:', data.error);  // Debugging statement
        }
    } catch (error) {
        console.error('Fetch error:', error);
        uploadResultElement.innerText = "An error occurred during file upload.";
    }
});

// Question Form Submission
document.getElementById('questionForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    console.log('Question form submitted');  // Debugging statement

    const percentage = document.getElementById('percentage').value;
    const question = document.getElementById('question').value;

    const loadingElement = document.getElementById('loading');
    const answerElement = document.getElementById('answer');
    const contextContainer = document.getElementById('contextContainer');
    const contextDocs = document.getElementById('contextDocs');

    // Show the loading message
    loadingElement.style.display = 'block';
    answerElement.innerText = '';
    contextContainer.style.display = 'none'; // Hide the context initially

    try {
        const response = await fetch('http://127.0.0.1:8890/ask-question', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ percentage: percentage, question: question })
        });

        console.log('Response received');  // Debugging statement

        const data = await response.json();

        // Hide the loading message
        loadingElement.style.display = 'none';

        if (response.ok) {
            console.log('Question processed successfully');  // Debugging statement
            answerElement.innerText = data.answer ? data.answer : "No answer returned.";

            // Display the supporting documents
            contextDocs.innerHTML = ''; // Clear any previous documents

            if (data.documents && data.documents.length > 0) {
                data.documents.forEach((doc, index) => {
                    const docWrapper = document.createElement('div');
                    const docTitle = document.createElement('div');
                    const docContent = document.createElement('div');
                    const docPosition = document.createElement('div');

                    docWrapper.classList.add('context-doc-wrapper');
                    docTitle.classList.add('context-doc-title');
                    docContent.classList.add('context-doc-content');
                    docPosition.classList.add('context-doc-position');

                    docTitle.innerText = `Passage ${index + 1}: (click to toggle)`;
                    docContent.innerText = doc.content;  // Insert document content
                    docPosition.innerText = `Position: ${doc.position}`;  // Insert document position

                    docContent.style.display = 'none'; // Start with content hidden

                    // Add toggle functionality with scroll to view
                    docTitle.addEventListener('click', function() {
                        if (docContent.style.display === 'none') {
                            docContent.style.display = 'block';
                            docPosition.style.display = 'block';
                            docTitle.scrollIntoView({ behavior: 'smooth', block: 'start' });
                        } else {
                            docContent.style.display = 'none';
                            docPosition.style.display = 'none';
                        }
                    });

                    docWrapper.appendChild(docTitle);
                    docWrapper.appendChild(docPosition);
                    docWrapper.appendChild(docContent);
                    contextDocs.appendChild(docWrapper);
                });

                contextContainer.style.display = 'block'; // Show the context section

                // Scroll to the top of the second container after loading the context
                setTimeout(() => {
                    questionContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }, 100);
            }
        } else {
            answerElement.innerText = data.error ? data.error : "An error occurred.";
            console.error('Error:', data.error);  // Debugging statement
        }
    } catch (error) {
        console.error('Fetch error:', error);
        answerElement.innerText = "An error occurred during question processing.";
    }
});
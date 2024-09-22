// This file is auto-generated by @hey-api/openapi-ts

export const AnswerSchema = {
    properties: {
        answer: {
            type: 'string',
            title: 'Answer'
        },
        documents: {
            items: {
                '$ref': '#/components/schemas/Document'
            },
            type: 'array',
            title: 'Documents'
        }
    },
    type: 'object',
    required: ['answer', 'documents'],
    title: 'Answer'
} as const;

export const Body_upload_file_upload_file_postSchema = {
    properties: {
        file: {
            type: 'string',
            format: 'binary',
            title: 'File'
        }
    },
    type: 'object',
    required: ['file'],
    title: 'Body_upload_file_upload_file_post'
} as const;

export const BookSchema = {
    properties: {
        title: {
            type: 'string',
            title: 'Title'
        },
        formats: {
            additionalProperties: {
                type: 'string'
            },
            type: 'object',
            title: 'Formats'
        }
    },
    type: 'object',
    required: ['title', 'formats'],
    title: 'Book'
} as const;

export const DocumentSchema = {
    properties: {
        content: {
            type: 'string',
            title: 'Content'
        },
        position: {
            type: 'string',
            title: 'Position'
        }
    },
    type: 'object',
    required: ['content', 'position'],
    title: 'Document'
} as const;

export const HTTPValidationErrorSchema = {
    properties: {
        detail: {
            items: {
                '$ref': '#/components/schemas/ValidationError'
            },
            type: 'array',
            title: 'Detail'
        }
    },
    type: 'object',
    title: 'HTTPValidationError'
} as const;

export const QuestionSchema = {
    properties: {
        question: {
            type: 'string',
            title: 'Question'
        },
        book: {
            type: 'string',
            title: 'Book'
        },
        percentage: {
            type: 'integer',
            title: 'Percentage',
            default: 100
        }
    },
    type: 'object',
    required: ['question', 'book'],
    title: 'Question'
} as const;

export const ValidationErrorSchema = {
    properties: {
        loc: {
            items: {
                anyOf: [
                    {
                        type: 'string'
                    },
                    {
                        type: 'integer'
                    }
                ]
            },
            type: 'array',
            title: 'Location'
        },
        msg: {
            type: 'string',
            title: 'Message'
        },
        type: {
            type: 'string',
            title: 'Error Type'
        }
    },
    type: 'object',
    required: ['loc', 'msg', 'type'],
    title: 'ValidationError'
} as const;
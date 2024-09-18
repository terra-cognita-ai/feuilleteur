export type Author = {
    name: string;
    birth_year: number;
    death_year: number;
}

type Translator = Author;

export type Book = {
    title: string;
    formats: {
        "image/jpeg": string;
        "application/epub+zip": string;
    };
    authors: Author[];
    translators: Translator[];
    subjects: string[];
    bookshelves: string[];
    languages: string[];
    copyright: boolean | null;
}

export type RequestStatus = 'idle' | 'processing' | 'ok' | 'error';

export type SearchRequest = {
    search: string;
    status: RequestStatus;
    results: Book[];
}

export type ImportRequest = {
    status: RequestStatus;
}

export type BookPassage = {
    content: string;
    position: string;
}

export type QuestionAnswer = {
    text: string;
    documents: BookPassage[];
    status: RequestStatus;
}

export type QuestionRequest = {
    question: string;
    book: string;
    percentage: number;
    answer: QuestionAnswer;
}
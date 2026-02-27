import React from "react";
import BookCard from "./BookCard";

interface Book{
    title: string
    authors: string
    thumbnail: string
}


interface BookListProps{
    books: Book[]
}

const BookList: React.FC<BookListProps> = ({books}) => {
    return (
        <div className="book-grid">
            {books.map((book, index)=>(
                <BookCard
                key={index}
                title={book.title}
                authors={book.authors}
                thumbnail={book.thumbnail}
                />
            ))}
        </div>
    )
}

export default BookList
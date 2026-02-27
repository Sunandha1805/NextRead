import React from "react";

interface BookCardProps {
    title: string
    authors: string
    thumbnail: string
}

const BookCard: React.FC<BookCardProps> = ({title, authors, thumbnail}) => {
    return (
        <div className="book-card">
            <img src={thumbnail} alt={title} className="book-cover"/>
            <h3 className="book-title">{title}</h3>
            <p className="book-author">{authors}</p>
        </div>
    )
}

export default BookCard
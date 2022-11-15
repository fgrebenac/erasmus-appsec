export interface PostComment {
    id: string,
    content: string,
    user_id: string,
    username: string,
    post_id: string
}

export interface Post {
    id: string,
    title: string,
    content: string,
    username: string,
    user_id: string
}

export interface PostRequest {
    title: string,
    content: string
}
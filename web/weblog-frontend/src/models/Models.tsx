export interface UserRequest {
    username: string | undefined,
    password: string | undefined
}

export interface PostComment {
    commentId: string,
    content: string,
    userId: string,
    username: string,
    postId: string
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
export type PostType = {
  id: number,
  title: string,
  body: string,
  userId: number,
  tags: string[],
  reactions: number,
}

export type GetPostsType = {
  posts: PostType[],
  total: number,
  skip: number,
  limit: number,
}

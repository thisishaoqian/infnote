import { APIClient } from '.'


class Post {
    static getMembers() {
        return ['post_id', 'date_submitted', 'date_confirmed', 'title', 'content', 'category', 'transaction_id', 'is_confirmed', 'block_height', 'reply_to', 'views', 'likes', 'replies', 'user', 'base_to', 'last_reply']
    }

    static retrieveList(category = '/', page = 1) {
        return APIClient.posts(category, page).then(response => {
            return { 
                count: response.data.count,
                posts: response.data.results.map(data => new Post(data))
            }
        })
    }

    static retrieve(postId) {
        return APIClient.retrievePost(postId).then(response => new Post(response.data))
    }

    constructor(props) {
        if (props) {
            Post.getMembers().forEach(name => this[name] = props[name] )
        }

        Object.defineProperties(this, {
            post_id: { writable: false },
            date_submitted: { writable: false },
            date_confirmed: { writable: false },
            transaction_id: { writable: false },
            is_confirmed: { writable: false },
            block_height: { writable: false },
            public_key: { writable: false },
            views: { writable: false },
            likes: { writable: false },
            replies: { writable: false },
        })

        Object.seal(this)
    }

    submit() {
        return APIClient.sendPost({
            title: this.title,
            content: this.content,
            category: this.category,
            reply_to: this.reply_to,
        }).then(response => new Post(response.data))
    }

    fetchReplies() {
        return APIClient.retrieveReplies(this.post_id).then(response => {
            return {
                count: response.data.count,
                posts: response.data.results.map(item => new Post(item))
            }
        })
    }
}

export default Post
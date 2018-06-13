import React, { Component } from 'react'
import { withStyles } from '@material-ui/core/styles'
import { Paper, Typography } from '@material-ui/core'
import PostItem from './PostItem'
import { Line, FixedSpace } from 'components/Utils'
import { Store } from 'models'


const styles = {
    header: {
        paddingTop: 10,
        paddingBottom: 10,
        paddingLeft: 25,
        paddingRight: 25,
        fontSize: '1.6em',
        fontWeight: 'bold',
        background: '#E9EAEC',
    }
}


class Topic extends Component {
    state = {
        replies: [],
        count: 0,
    }
    componentWillMount() {
        this.props.post.fetchReplies().then(data => {
            this.setState({ count: data.count, replies: data.posts })
        })
        this.unsubscribe = Store.subscribe(() => {
            let replies = this.state.replies
            const post = Store.getState().postEvent
            if (post) {
                replies.push(Store.getState().postEvent)
                this.setState({ replies })
            }
        })
    }
    componentWillUnmount() {
        this.unsubscribe()
    }
    render() {
        const { classes, post } = this.props
        const { replies } = this.state
        if (post) 
            return (
                <Paper className="paper">
                    <Typography className={classes.header}>{post.title}</Typography>
                    <PostItem post={post}/>
                    {replies.map((item, index) => {
                        return (
                            <div key={index}>
                                <Line width={10}/>
                                <PostItem post={item}/>
                            </div>
                        )
                    })}
                </Paper>
            )
        return (
            <Paper className="paper">
                <FixedSpace size="xs3" className="paper-decorator"/>
            </Paper>
        )
    }
}

export default withStyles(styles)(Topic)

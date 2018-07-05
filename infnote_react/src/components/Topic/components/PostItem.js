import React, { Component } from 'react'
import { withStyles } from '@material-ui/core/styles'
import { Typography, Avatar } from '@material-ui/core'
import avatar_placeholder from 'assets/avatar-placeholder.svg'
import { FixedSpace } from 'components/Utils'
import ReactMarkdown from 'react-markdown'
import classNames from 'classnames'

import { formatDate } from 'tools'

const styles = theme => {
    return {
        postItem: {
            display: 'flex',
        },
        userInfo: {
            width: 200,
            minWidth: 200,
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'flex-start',
            textAlign: 'center',
        },
        content: {
            paddingTop: 30,
            paddingBottom: 30,
            paddingLeft: 60,
            paddingRight: 60,
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            overflow: 'scroll',
        },
        avatar: {
            width: 80,
            height: 80,
            margin: '0 auto',
        },
        verticalDivider: {
            width: 3,
            minWidth: 3,
            background: '#E9EAEC',
        },
        contentDivider: {
            height: 4,
            width: 120,
            background: '#E9EAEC',
        },
        ...theme.typography
    }
}


class PostItem extends Component {
    componentDidMount() {
        const items = document
            .getElementById(this.props.post.post_id)
            .getElementsByTagName('pre')
        for (let item of items) {
            window.hljs.highlightBlock(item)
        }
    }

    render() {
        const { classes, post } = this.props
        return (
            <div className={classes.postItem}>
                <div className={classes.userInfo}>
                    <FixedSpace size="md"/>
                    <Avatar src={avatar_placeholder} alt="Avatar" className={classes.avatar}/>
                    <FixedSpace size="sm"/>
                    <Typography>{post.user.nickname}</Typography>
                    <Typography>Post: {post.user.topics}</Typography>
                    <FixedSpace size="md"/>
                </div>
                <div className={classes.verticalDivider}></div>
                <div className={classNames(classes.content, 'full-width')} id={post.post_id}>
                    <ReactMarkdown source={post.content} className={classes.body1}/>
                    <FixedSpace size="lg"/>
                    <div>
                        <div className={classes.contentDivider}></div>
                        <FixedSpace size="sm"/>
                        {(() => {
                            if (post.date_confirmed) {
                                return (<Typography><strong>Confirmed at:</strong> { formatDate(post.date_confirmed) }</Typography>)
                            } else {
                                return (<Typography><strong>Submitted at:</strong> { formatDate(post.date_submitted) }</Typography>)
                            }
                        })()}
                    </div>
                </div>
            </div>
        )
    }
}

export default withStyles(styles)(PostItem)

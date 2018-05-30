import React, { Component } from 'react'
import { withStyles } from '@material-ui/core/styles'
import { Typography, Avatar } from '@material-ui/core'
import avatar_placeholder from 'assets/avatar-placeholder.svg'
import { FixedSpace } from 'components/Utils'

const styles = {
    postItem: {
        display: 'flex',
    },
    userInfo: {
        width: 200,
        minWidth: 200,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
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
    }
}


class PostItem extends Component {
    render() {
        const { classes } = this.props
        return (
            <div className={classes.postItem}>
                <div className={classes.userInfo}>
                    <FixedSpace size="md"/>
                    <Avatar src={avatar_placeholder} alt="Avatar" className={classes.avatar}/>
                    <FixedSpace size="sm"/>
                    <Typography>Vergil</Typography>
                    <Typography>Post: 100</Typography>
                    <FixedSpace size="md"/>
                </div>
                <div className={classes.verticalDivider}></div>
                <div className={classes.content}>
                    <Typography>COOL</Typography>
                    <FixedSpace size="lg"/>
                    <div>
                        <div className={classes.contentDivider}></div>
                        <FixedSpace size="sm"/>
                        <Typography><strong>Posted at:</strong> Today 12:34:56 am</Typography>
                    </div>
                </div>
            </div>
        )
    }
}

export default withStyles(styles)(PostItem)

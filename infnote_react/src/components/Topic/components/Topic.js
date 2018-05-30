import React, { Component } from 'react'
import { withStyles } from '@material-ui/core/styles'
import { Paper, Typography } from '@material-ui/core'
import PostItem from './PostItem'
import { Line, FixedSpace } from 'components/Utils'

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
    render() {
        const { classes } = this.props
        return (
            <Paper className="paper">
                <FixedSpace size="xs3" className="paper-decorator"/>
                <Typography className={classes.header}>Title</Typography>
                <PostItem />
                <Line width={10}/>
                <PostItem />
            </Paper>
        )
    }
}

export default withStyles(styles)(Topic)

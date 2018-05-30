import React, { Component } from 'react'
import { withStyles } from '@material-ui/core/styles'
import { Typography, Button } from '@material-ui/core'

const styles = {
    breadcrumb: {
        display: 'flex',
    }
}

class Breadcrumb extends Component {
    render() {
        const { crumb, classes } = this.props
        return (
            <div className={classes.breadcrumb}>
                <Button size="small">Main</Button>
                { crumb.map((item, index) => {
                    return (
                        <Typography key={index}>>><Button size="small">{item}</Button></Typography>
                    )
                })}
            </div>
        )
    }
}

export default withStyles(styles)(Breadcrumb)
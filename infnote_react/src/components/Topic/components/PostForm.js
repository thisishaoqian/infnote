import React, { Component } from 'react'
import { withStyles } from '@material-ui/core/styles'
import { Paper, TextField, Typography, Button } from '@material-ui/core'
import { FixedSpace } from 'components/Utils'
import classNames from 'classnames'

const styles = theme => {
    const colors = theme.palette
    return {
        paper: {
            paddingLeft: 25,
            paddingRight: 25,
            paddingTop: 15,
            paddingBottom: 15,
        },
        title: {
            color: colors.primary.main,
            fontSize: '1.6em',
            fontWeight: 'bold',
        },
        subtitle: {
            color: colors.primary.main,
            fontSize: '1em',
            fontWeight: 600,
        },
        textField: {
            background: colors.grey[200],
            borderRadius: 5,
            paddingTop: 5,
            paddingBottom: 5,
            paddingLeft: 15,
            paddingRight: 15,
        }
    } 
}

class PostForm extends Component {
    render () {
        const { classes, type } = this.props
        return (
            <Paper className={classNames('paper', classes.paper)}>
                <Typography className={classes.title}>Post a new {type}</Typography>
                <FixedSpace size="sm"/>
                <Typography className={classes.subtitle}>Title</Typography>
                <TextField className={classes.textField} InputProps={{disableUnderline: true}} fullWidth/>
                <FixedSpace size="sm"/>
                <Typography className={classes.subtitle}>Content</Typography>
                <TextField className={classes.textField} InputProps={{disableUnderline: true}} fullWidth multiline rows="10"/>
                <FixedSpace size="sm"/>
                <Button variant="raised" color="secondary" size="large" fullWidth>
                    <Typography color="primary" style={{fontWeight: 'bold'}}>Publish {type}</Typography>
                </Button>
            </Paper>
        )
    }
}

export default withStyles(styles)(PostForm)

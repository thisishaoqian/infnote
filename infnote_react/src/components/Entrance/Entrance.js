import React, { Component } from 'react'
import { withStyles } from '@material-ui/core/styles'
import { Grid } from '@material-ui/core'
import { Route } from 'react-router-dom'
import background from './background.png'
import LoginForm from './LoginForm'
import SignForm from './SignForm'

const styles = {
    background: {
        backgroundImage: 'url(' + background + ')',
        backgroundPosition: '50% 50%',
        backgroundSize: 'cover',
        backgroundRepeat: 'no-repeat',
        position: 'fixed',
        top: 0, left: 0, right: 0, bottom: 0,
        zIndex: -1,
    },
}


class Entrance extends Component {
    render() {
        const { classes } = this.props
        return(
            <Grid container className="full-width full-height" justify="center" alignItems="center">
                <div className={classes.background}></div>
                <Route path="/sign/in/" component={LoginForm}/>
                <Route path="/sign/up/" component={SignForm}/>
            </Grid>
        )
    }
}

export default withStyles(styles)(Entrance)
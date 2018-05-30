import React, { Component } from 'react'
import { withStyles } from '@material-ui/core/styles'
import { AppBar, Toolbar, Button, Avatar, Typography, Grid, IconButton } from '@material-ui/core'
import logo from 'assets/infnote-logo.png'
import avatar_placeholder from 'assets/avatar-placeholder.svg'

const styles = {
    navbar: {
        height: 80,
        backgroundColor: 'white',
    },
    toolbar: {
        height: 80,
        justifyContent: 'space-between'
    },
    name: {
        fontSize: '1.2em',
        fontWeight: 'bold',
        paddingRight: 15,
        paddingLeft: 15,
    }
}


class Navbar extends Component {
    render() {
        const { classes } = this.props
        return (
            <AppBar className={classes.navbar} position="static">
                <Toolbar className={classes.toolbar}>
                    <Button>
                        <img src={logo} alt="" srcSet={logo + ' 2x'} width="80"/>
                    </Button>
                    <Grid container justify="flex-end" alignItems="center">
                        <Typography className={classes.name}>Vergil</Typography>
                        <IconButton><Avatar src={avatar_placeholder} /></IconButton>
                    </Grid>
                </Toolbar>
            </AppBar>
        )
    }
}

export default withStyles(styles)(Navbar)
